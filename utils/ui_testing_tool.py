import os
from openai import OpenAI
import google.generativeai as genai
import configparser

config = configparser.ConfigParser()
config.read('config.conf')

section = 'LLM'
llm_model = config.get(section, 'llm_model')
openai_key = config.get(section, 'openai_key')
gemini_key = config.get(section, 'gemini_key')


def generate_resp_from_llm(model, prompt):
    f = open('prompt.txt','w')
    f.write(prompt)
    f.close()
    if model == 'LLAMA2':
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

    elif model == 'Gemini':
        return gemini_responsee(prompt)

    elif model == 'OpenAI':
        return gpt_response(prompt)


def gemini_responsee(prompt):
    genai.configure(api_key=gemini_key)

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    return response.text


def gpt_response(prompt):
    messages = [{"role": "system",
                 "content": " Generate programming code. Dont give explanation"}]

    messages.append({"role": "system",
                     "content": "Generate test automation code"})
    if prompt:
        messages.append({"role": "user", "content": f"{prompt}"})

    try:
        client = OpenAI(api_key=openai_key)
        # print("client",client)

        response = client.chat.completions.create(
            model='gpt-4o',
            messages=messages,
            max_tokens=int(2048),
        )
        # print("responser", response)
        # print(f"Tokens Used for Generating Code: {response.usage.completion_tokens}")

        # print(f"Response: {response.json()}")

        return response.choices[0].message.content
    except Exception as e:
        print(f'Exception Occurred On generating code : {e}')
        return None


def main(acceptance_criteria, locator, ui_test_framework, prog_language, additional_details):
    prompt_template = f"""
    Generate detailed test cases for a UI test scenario. Here are the inputs:
    1. Acceptance Criteria: f{acceptance_criteria}
    2. Locator: f{locator}
    3. UI Test Framework: f{ui_test_framework}
    4. Programming Language: f{prog_language}
    5. Additional Details: f{additional_details}
    """


    resp = generate_resp_from_llm(model=llm_model,
                                    prompt=prompt_template)

    return resp
