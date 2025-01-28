import os
from openai import OpenAI
import google.generativeai as genai
import configparser
from groq import Groq


config = configparser.ConfigParser()
config.read('config.conf')

section = 'LLM'
llm_model = config.get(section, 'llm_model')
openai_key = config.get(section, 'openai_key')
gemini_key = config.get(section, 'gemini_key')
groq_api_key = config.get('LLM', 'groq_key')


def generate_resp_from_llm(model, prompt):
    if model == 'LLAMA2':
        client = Groq(
                api_key= groq_api_key,
            )
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192",
        )

        return chat_completion.choices[0].message.content

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
    Generate detailed test cases code for a UI test scenario. Here are the inputs:
    1. Acceptance Criteria: f{acceptance_criteria}
    2. Locator: f{locator}
    3. UI Test Framework: f{ui_test_framework}
    4. Programming Language: f{prog_language}
    5. Additional Details: f{additional_details}
    """


    resp = generate_resp_from_llm(model=llm_model,
                                    prompt=prompt_template)

    return resp
