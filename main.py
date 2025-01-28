from flask import Flask, request, jsonify
from utils.ui_testing_tool import main
from utils.api_testing_tool import process_json as api_process_json, render_template, get_generated_api_test_code
import os
import configparser
import base64


config = configparser.ConfigParser()
config.read('config.conf')
section = 'LLM'
llm_model = config.get(section, 'llm_model')


app = Flask(__name__)


@app.route("/uitesting/submit", methods=["POST"])
def ui_testing_request():
    if request.method=="POST":
        if "acceptance_criteria" not in request.form:
            return jsonify({"status": "failed",
                           "message": "Acceptance criteria is a mandatory field"}), 400
        acceptance_criteria = request.form["acceptance_criteria"]
        locators = request.form["locators"]
        additional_details = request.form["additional_details"]
        test_framework = request.form["test_framework"]
        language = request.form["language"]
        try:        
            code_output = main(acceptance_criteria, locators, test_framework.lower(), language.lower(), additional_details)
            return jsonify({"status": "success", 
                        "message": code_output}), 200
        except:
            return jsonify({"status": "failed",
                            "message": """Generating code failed, 
                                        Possible issue: Invalid llm model or auth keys in config file"""})
    else:
        return jsonify({"status": "failed", 
                        "message": "Only post requests accepted"}), 405


def get_all_api_endpoints(swagger_file):
    api_all_endpoints = []
    model_structure_final, swagger_result, swagger_json = api_process_json(swagger_file)
    api_all_endpoints += list(swagger_result.keys())
    return api_all_endpoints, model_structure_final, swagger_result, swagger_json


@app.route("/apitesting/apidefinitions/submit", methods=["POST"])
def api_endpoints_extraction():
    if request.method=="POST":
        if request.files:
            swagger_file = request.files['api_definitions_file']
            swagger_file.save(os.path.join(os.getcwd(), "api_endpoints_folder", swagger_file.filename))
            try:
                api_all_endpoints, model_structure_final, swagger_result, swagger_json = list(get_all_api_endpoints(os.path.join(os.getcwd(), "api_endpoints_folder", swagger_file.filename)))
                return jsonify({"file_name": swagger_file.filename,
                            "api_endpoints": api_all_endpoints,
                            "status": "success"}), 200
            except:
                return jsonify({"status": "failed",
                            "message": """Failed to get the endpoints list
                                          Please check the get endpoints functionality"""}), 400
        else:
            return jsonify({"status": "failed",
                           "message": "API definition file is mandatory"}), 400
    else:
        return jsonify({"status": "failed", 
                        "message": "Only post requests accepted"}), 405


def get_api_test_result(selected_endpoints, swagger_result, model_structure_final, api_test_framework, swagger_json, api_additional_inputs):
    selected_prompt_messages = render_template(selected_endpoints, swagger_result, model_structure_final, api_test_framework, swagger_json, api_additional_inputs)
    resp_list = []
    for each_prompt in selected_prompt_messages:
        resp = get_generated_api_test_code(each_prompt)
        resp_list.append(resp)
    separation_text = "\n\n\n" + "#"*150 + "\n\n\n"
    return separation_text.join(resp_list)


@app.route("/apitesting/submit", methods=["POST"])
def api_testing_request():
    if request.method=="POST":
        if request.files:
            swagger_file = request.files['api_definitions_file']
            swagger_file.save(os.path.join(os.getcwd(), "api_endpoints_folder", swagger_file.filename))
            api_all_endpoints, model_structure_final, swagger_result, swagger_json = list(get_all_api_endpoints(os.path.join(os.getcwd(), "api_endpoints_folder", swagger_file.filename)))
            selected_endpoints = request.form.getlist("selected_endpoints")
            framework = request.form["framework"]
            additional_inputs = request.form["additional_inputs"]
            try:
                code_output = get_api_test_result(selected_endpoints, swagger_result, model_structure_final, framework, swagger_json, additional_inputs)
                return jsonify({"status": "success",
                            "message": code_output}), 200
            except:
                return jsonify({"status": "failed",
                                "message": "Check the get api test result function"}), 400
        else:
            return jsonify({"status": "failed",
                           "message": "API definition file is mandatory"}), 400
    else:
        return jsonify({"status": "failed", 
                        "message": "Only post requests accepted"}), 405  


def update_config_file(model="", auth_key=""): 
    if len(model)>0:
        config.set(section, "llm_model", model)
    if len(auth_key)>0:
        config.set(section, f"{model}_key", auth_key)
    with open('config.conf', 'w') as configfile:
        config.write(configfile)


@app.route("/", methods=["POST"])
def update_llm():
    if request.method=="POST":
        model = request.form["llm_model"]
        auth_key = request.form["auth_key"]
        try:
            decoded_key = base64.b64decode(auth_key).decode('utf-8')
        except Exception as e:
            return jsonify({"error": "Invalid encoding"}), 400
        try:
            update_config_file(model, decoded_key)
            return jsonify({"status":"success",
                        "message": "Updated the llm and auth key"}), 200
        except:
            jsonify({"status": "failed",
                     "message": "Updating the config file failed, please refer to update config file functionality"})

    else:
        return jsonify({"status": "failed", 
                        "message": "Only post requests accepted"}), 405     

if __name__=="__main__":
    app.run(debug=True)