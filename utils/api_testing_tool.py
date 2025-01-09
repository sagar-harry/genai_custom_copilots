import replicate
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import os
from langchain_openai import OpenAI
import openai
from openai import OpenAI
import os
import logging
import json
import copy
import time
from glom import glom, PathAccessError
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader, select_autoescape
import html2text
import configparser


_logger = logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read("config.conf")
section = 'LLM'
llm_model = config.get(section, 'llm_model')
openai_key = config.get(section, 'openai_key')
gemini_key = config.get(section, 'gemini_key')
llama2_key = config.get(section, 'llama2_key')


max_tokens = int(os.environ.get('OPENAI_MAX_TOKENS', '4000'))
model = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')


def gpt_response(prompt):
    messages = [{"role": "system",
                 "content": " Generate programming code. Dont give explanation"}]

    messages.append({"role": "system",
                     "content": "Generate test automation code"})
    if prompt:
        messages.append({"role": "user", "content": f"{prompt}"})

    try:
        client = OpenAI(api_key=openai_key)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=int(max_tokens),
        )
        print(f"Tokens Used for Generating Code: {response.usage.completion_tokens}")

        print(f"GPT Response: {response.json()}")

        return response.choices[0].message.content
    except Exception as e:
        print(f'Exception Occurred On GPT API: {e}')
        return None


def gemini_response(prompt):
    genai.configure(api_key=gemini_key)
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text


def generate_resp_from_llm(prompt):
    if llm_model == 'LLAMA2':
        output = replicate.run(
            "replicate/llama-7b:ac808388e2e9d8ed35a5bf2eaa7d83f0ad53f9e3df31a42e4eb0a0c3249b3165",
            input={
                "debug": False,
                "top_p": 0.95,
                "prompt": prompt,
                "max_length": 500,
                "temperature": 0.8,
                "repetition_penalty": 1
            }
        )

        return "".join(output)

    elif llm_model == 'Gemini':

        return gemini_response(prompt)

    elif llm_model == 'OpenAI':
        return gpt_response(prompt)


def process_swagger_json(swagger_json):
    swagger_result = {}
    for path, path_values in swagger_json.get('paths').items():
        if path not in swagger_result:
            swagger_result[path] = []
        for each_method, method_value in path_values.items():

            try:
                schema = glom(method_value, 'requestBody.content.application/json.schema.$ref')
                model = schema.split('/')[-1] if schema else None
            except PathAccessError:
                schema = None
                model = None

            swagger_result[path].append({'method': each_method,
                                         'parameters':
                                             [each_param['name'] for each_param in method_value['parameters'] if
                                              each_param['in'] == 'query'],
                                         'schema': schema,
                                         'model': model,
                                         'response_codes': list(method_value.get('responses').keys())
                                         })
    model_structure_temp = {}
    swagger_components = swagger_json['components'] if 'components' in swagger_json else ''
    model_schemas = swagger_json.get('components')['schemas'] if swagger_components else None
    if model_schemas:
        for model_name, model_body in model_schemas.items():
            if model_name not in model_structure_temp:
                model_structure_temp[model_name] = {}
            if 'enum' in model_body:
                model_structure_temp[model_name] = model_body
                continue
            if 'properties' in model_body:
                for property_name, property_body in model_body.get('properties').items():
                    if 'type' in property_body:
                        if property_body['type'] == 'array' and '$ref' in property_body['items']:
                            sub_model = property_body['items']['$ref'].split('/')[-1]
                            model_structure_temp[model_name][property_name] = {"type": "sub_model",
                                                                               "model_name": sub_model}
                            continue
                    if '$ref' in property_body:
                        sub_model = property_body['$ref'].split('/')[-1]
                        model_structure_temp[model_name][property_name] = {"type": "sub_model",
                                                                           "model_name": sub_model}

                    else:
                        model_structure_temp[model_name][property_name] = property_body

    model_structure_final = copy.deepcopy(model_structure_temp)

    for model_name, model_body in model_structure_final.items():
        for property_name, property_body in model_body.items():
            if 'type' in property_body and property_body['type'] == "sub_model":
                model_structure_final[model_name][property_name]['details'] = model_structure_temp[
                    property_body['model_name']]

    return model_structure_final, swagger_result


def render_template(api_endpoint_choices, swagger_result, model_structure_final, framework, swagger_json, api_additional_inputs):
    selected_prompts = {}
    response_codes = None
    request_body = None
    selected_prompt_messages = []
    for each_endpoint in api_endpoint_choices:
        data = []
        for each_method in swagger_result[each_endpoint]:
            if 'schema' in each_method and each_method['schema']:
                schema_name = each_method['schema'].split('/')[-1]
                request_body = model_structure_final[schema_name]
                response_codes = [c for c in each_method['response_codes'] if c != 'default']
            temp_dict = {'method': each_method['method'],
                         'response_codes': response_codes,
                         'request_body': request_body,
                         'endpoint': each_endpoint,
                         'additional_inputs': api_additional_inputs}
            data.append(temp_dict)
        selected_prompts.update({each_endpoint: data})

    for each_url, each_prompt in selected_prompts.items():
        # breakpoint()
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html'])
        )
        template = env.get_template('prompt_template.html')
        context = {
            'framework': framework,
            'end_point': each_url,
            'prompts': each_prompt,
            'base_url': swagger_json["host"],
            'additional_inputs': api_additional_inputs
        }

        rendered_html = template.render(context)

        html_string = html2text.html2text(rendered_html)
        selected_prompt_messages.append(html_string)

    return selected_prompt_messages


def process_json(uploaded_file):
    try:
        with open(uploaded_file, 'r') as file_reader:
            output = json.load(file_reader)
        model_structure_final, swagger_result = process_swagger_json(output)
        return model_structure_final, swagger_result, output
    except Exception:
        raise Exception('There was an error processing the uploaded JSON. Please upload a valid JSON')


def get_generated_api_test_code(prompt):
    resp = generate_resp_from_llm(prompt=prompt)
    return resp


# def main():
#     json_read = process_json(None)
#     api_endpoint_choices = []
#     model_structure_final, swagger_result = process_swagger_json(json_read)
#     selected_api_endpoint_choices = []

#     selected_prompt_messages = render_template(api_endpoint_choices)


# if __name__ == "__main__":
#     main()
