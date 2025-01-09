import gradio as gr
from utils.ui_testing_tool import main
import os
import time
import configparser
from utils.api_testing_tool import process_json as api_process_json, render_template, get_generated_api_test_code


config = configparser.ConfigParser()
config.read('config.conf')
section = 'LLM'
llm_model = config.get(section, 'llm_model')

global api_all_endpoints
api_all_endpoints = []

gr.set_static_paths(paths=["./assets/"])


def gradio_update_strings(total_count, list_of_trues):
    string_list = total_count*[gr.update(visible=False)]
    for i in list_of_trues:
        string_list[i] = gr.update(visible=True)
    
    return string_list


def go_to_ui_test_page():
    return gradio_update_strings(6, [1])


def go_to_api_test_page():
    return gradio_update_strings(6, [2])


def go_to_synthetic_data_test_page():
    return gradio_update_strings(6, [3])


def go_to_settings_page():
    return gradio_update_strings(6, [4])


def go_to_performance_testing_page():
    return gradio_update_strings(6, [5])


def clear_inputs():
    return gr.update(value=""), gr.update(value=""), gr.update(value="")


refresh_script = """
<div style="display: flex; justify-content: center; align-items: center; height: 50px;">
    <button onclick="location.reload()" 
            style="padding: 10px 20px; font-size: 16px; color: white; background-color: black; border: none; border-radius: 5px; cursor: pointer;">
        Home
    </button>
</div>
"""


def update_llm(model, auth_key): 
    if len(model)>0:
        config.set(section, "llm_model", model)
    if len(auth_key)>0:
        config.set(section, f"{model}_key", auth_key)
    with open('config.conf', 'w') as configfile:
        config.write(configfile)
    time.sleep(1)
    return gr.update(visible=True)


def remove_updated_html():
    return gr.update(visible=False)

                       
def get_all_api_endpoints(swagger_file):
    api_all_endpoints = []
    model_structure_final, swagger_result, swagger_json = api_process_json(swagger_file)
    api_all_endpoints += list(swagger_result.keys())
    return api_all_endpoints, model_structure_final, swagger_result, swagger_json


def get_api_endpoint_selection_page(swagger_file):
    api_all_endpoints, model_structure_final, swagger_result, swagger_json = list(get_all_api_endpoints(swagger_file))
    api_endpoints_dropdown = gr.Dropdown(label="Endpoints (max: 5)", choices=api_all_endpoints, multiselect=True, max_choices=5, elem_classes='custom-dropdown')   
    model_structure_final = gr.Json(model_structure_final)
    swagger_result = gr.Json(swagger_result)
    swagger_json = gr.Json(swagger_json)
    return gr.update(visible=False), api_endpoints_dropdown , gr.update(visible=True), model_structure_final, swagger_result, swagger_json

        
def get_api_test_result_page_1(selected_endpoints, api_additional_inputs, api_test_framework, model_structure_final, swagger_result, swagger_json ):
    time.sleep(5)
    return gr.update(visible=False), gr.update(visible=True)


def get_api_test_result_page_2(selected_endpoints, api_additional_inputs, api_test_framework, model_structure_final, swagger_result, swagger_json ):
    selected_prompt_messages = render_template(selected_endpoints, swagger_result, model_structure_final, api_test_framework, swagger_json, api_additional_inputs)
    resp_list = []
    for each_prompt in selected_prompt_messages:
        resp = get_generated_api_test_code(each_prompt)
        resp_list.append(resp)
    separation_text = "\n\n\n" + "#"*150 + "\n\n\n"
    return gr.Code(separation_text.join(resp_list))


def home_page():
    with gr.Blocks(css="./assets/styles.css", fill_width=True) as application:
        
        with gr.Column(visible=True, elem_id="HomePage") as home_page:
            with gr.Row(visible=True, elem_id="Logos") as logos:
                with gr.Column(scale=1, min_width=0):
                    with gr.Row(): pass
                    with gr.Row():
                        gr.HTML("""<div style="display: flex; align-items: value; justify-content: left;">
                                <img src='file/assets/accion.png' style="height: 30px; width: auto;" alt="Left Logo">
                                </div>
                                """)
                                
                with gr.Column(scale=8, min_width=30):
                    gr.Markdown("""
                                    <h1 style="display: flex; justify-content: center;">
                                        Custom Copilots
                                    </h1>
                                """)


                with gr.Column(scale=1, min_width=0):
                    gr.HTML("""<div style="display: flex; justify-content: right;">
                            <img src='file/assets/client.png' style="height: 60px; width: auto;" alt="Right Logo">
                            </div>
                            """)
            
            with gr.Row() as main_body:
                with gr.Column(visible=True):
                    with gr.Row(): pass
                    with gr.Row(): pass
                    with gr.Row(): pass
                    with gr.Row(): pass
                    with gr.Row(visible=True) as image_box:
                                    
                        gr.HTML("""
                        <div class="slider">
                            <div class="slides">
                                <img src="file/assets/main_page_logo.png" alt="Image 1">
                            </div>
                        </div>
                            """)

                    with gr.Row(visible=True) as description_box: pass
                    #     gr.HTML("""
                    #     <h2 >
                    #         <strong style="font-weight: 700;"> Customization Per Needs: </strong> Custom Copilots are built per customer specific requirements, ensuring relevance and precision. <br>

                    #             <strong style="font-weight: 700;"> LLM-Powered Test Generation: </strong> Automatically generates manual test cases from user stories, ensuring comprehensive coverage of functional requirements & Converts manual test scripts into automation scripts
                    #             <br> <br>
                    #             <strong style="font-weight: 700;"> Benefits: </strong> <br>
                    #             Reduces test creation and maintenance effort with intelligent automation. <br>
                    #             Accelerates defect resolution by providing intelligent triaging and analysis. <br>
                    #             Aligns with client-specific goals to deliver maximum efficiency and quality improvements.
                    #     </h2>
                    # """)
                    
                    with gr.Row(visible=True) as page_redirect_buttons:
                        with gr.Column(visible=True, scale=3, min_width=0): pass
                        with gr.Column(visible=True, scale=1, min_width=60):
                            ui_page_button = gr.Button("UI Testing", scale=1, elem_classes="custombutton1")
                        with gr.Column(visible=True, scale=1, min_width=60):
                            api_page_button = gr.Button("API Testing", scale=1, elem_classes="custombutton1")  
                        with gr.Column(visible=True, scale=1, min_width=60):
                            synthetic_data_page_button = gr.Button("Synthetic Data", scale=1, elem_classes="custombutton1")
                        with gr.Column(visible=True, scale=1, min_width=60):
                            settings_page_button = gr.Button("Settings", scale=1, elem_classes="custombutton1")
                        with gr.Column(visible=True, scale=1, min_width=60):
                            performance_page_button = gr.Button("Performance Testing", scale=1, elem_classes="custombutton1")
                        with gr.Column(visible=True, scale=3, min_width=0): pass

        with gr.Column(visible=False) as ui_test_page:
            with gr.Row(visible=True, elem_id="Logos", variant='panel') as ui_test_page_logos:
                with gr.Column(scale=1, min_width=0):
                    with gr.Row(): pass
                    with gr.Row():
                        gr.HTML("""<div style="display: flex; justify-content: left;">
                                <img src='file/assets/accion.png' style="height: 30px; width: auto;" alt="Left Logo">
                                </div>
                                """)                       
                                
                with gr.Column(scale=8, min_width=30):
                    gr.Markdown("""
                                    <h4 style="display: flex; justify-content: center;">
                                        UI Testing
                                    </h4>
                                """)

                with gr.Column(scale=1, min_width=0):
                    gr.HTML("""<div style="display: flex; justify-content: right;">
                            <img src='file/assets/client.png' style="height: 60px; width: auto;" alt="Right Logo">
                            </div>
                            """)
            
            with gr.Row(visible=False) as ui_test_page_result_load_screen:
                with gr.Column():
                    with gr.Row():
                        gr.Markdown("""
                                        <h2 style="display: flex; justify-content: center;">
                                            Generating Test Code...
                                        </h2>
                                    """)
                        
                    with gr.Row():
                        gr.HTML(refresh_script)
                    
            with gr.Row(visible=False) as ui_test_page_result:
                with gr.Column():
                    with gr.Row():
                        with gr.Column():
                            output = gr.Code(label="Output", interactive=False)
                    with gr.Row():
                        with gr.Column(scale=4, min_width=0): pass
                        with gr.Column(scale=1, min_width=0): 
                            back_button = gr.Button("Back", scale=1)
                        with gr.Column(scale=4, min_width=0): pass    
                    with gr.Row():
                        gr.HTML(refresh_script)

            with gr.Row() as ui_test_page_main_content:
                with gr.Column():
                    with gr.Row():
                        with gr.Column(visible=True, scale=5, min_width=0) as ui_test_page_column_one:
                            with gr.Row():
                                acceptance_criteria = gr.Textbox(label="Acceptance Criteria", placeholder="Enter Acceptance Criteria", lines=3, elem_classes="custom-textbox")

                            with gr.Row():
                                locators = gr.Textbox(label="Locators", placeholder="Enter Locators", lines=3, elem_classes="custom-textbox")
                            with gr.Row(): pass
                            with gr.Row():
                                additional_details = gr.Textbox(label="Additional Details", placeholder="Enter any additional details", lines=3, elem_classes="custom-textbox")
                        
                        with gr.Column(visible=True, scale=5) as ui_test_page_column_two:
                            with gr.Row():
                                test_framework = gr.Dropdown(choices=["Selenium", "Cypress", "Playwright"], label="Test Framework (Default: Selenium)", value="Selenium", elem_classes='custom-dropdown')
                            with gr.Row():
                                language = gr.Dropdown(choices=["Python", "JavaScript", "Java", 'TypeScript'], label="Language (Default: Python)", value="Python", elem_classes='custom-dropdown')
                            with gr.Row():
                                with gr.Column(scale=2, min_width=0): pass
                                with gr.Column(scale=1, min_width=3):
                                    reset_button = gr.Button("Reset", scale=0, min_width=3)
                                    
                                with gr.Column(scale=1, min_width=3):
                                    submit_button = gr.Button("Submit", scale=0, min_width=3)
                                with gr.Column(scale=2, min_width=0): pass
                            with gr.Row():
                                gr.HTML(refresh_script)    
         

            def on_submit(acceptance_criteria, locators, test_framework, language, additional_details):
                time.sleep(2)
                return main(acceptance_criteria, locators, test_framework.lower(), language.lower(), additional_details), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
        

            def get_loading_page():
                return gradio_update_strings(2, [0])
            

            reset_button.click(clear_inputs,  
                    outputs=[acceptance_criteria, locators, additional_details])

            submit_button.click(fn=get_loading_page, 
                                outputs=[ui_test_page_result_load_screen, ui_test_page_main_content],
                                show_progress='full')   

            submit_button.click(fn=on_submit, inputs=[acceptance_criteria, locators, test_framework, language, additional_details], 
                                outputs=[output, ui_test_page_result, ui_test_page_main_content, ui_test_page_result_load_screen],
                                show_progress='full')
            
            def go_back_to_ui_test_page():
                return gradio_update_strings(3, [0])

            back_button.click(fn=go_back_to_ui_test_page,
                                outputs=[ui_test_page_main_content, ui_test_page_result, ui_test_page_result_load_screen])                    
        
        with gr.Column(visible=False) as api_test_page:
            
            with gr.Row(visible=True, elem_id="Logos", variant='panel') as api_test_page_logos:
                with gr.Column(scale=1, min_width=0):
                    with gr.Row(): pass
                    with gr.Row():
                        gr.HTML("""<div style="display: flex; justify-content: left;">
                                <img src='file/assets/accion.png' style="height: 30px; width: auto;" alt="Left Logo">
                                </div>
                                """)                       
                                
                with gr.Column(scale=8, min_width=30):
                    gr.Markdown("""
                                    <h4 style="display: flex; justify-content: center;">
                                        API Testing
                                    </h4>
                                """)

                with gr.Column(scale=1, min_width=0):
                    gr.HTML("""<div style="display: flex; justify-content: right;">
                            <img src='file/assets/client.png' style="height: 60px; width: auto;" alt="Right Logo">
                            </div>
                            """)

            with gr.Row(visible=False) as api_api_result_page:
                with gr.Column(min_width=0, scale=1): pass
                with gr.Column(scale=8):
                    api_output_code = gr.Code("")
                with gr.Column(min_width=0, scale=1): pass

            with gr.Row(visible=False) as api_endpoint_selection_page:
                with gr.Column(min_width=0, scale=1): pass
                with gr.Column(visible=True, scale=5):
                    gr.HTML("<h2> Select the endpoints to generate API Tests </h2>")
                    with gr.Row():
                        with gr.Column(min_width=0, scale=1): pass
                        with gr.Column(min_width=0, scale=18):
                            all_endpoints = gr.Dropdown("", multiselect=True)
                            api_test_framework = gr.Dropdown(label="Framework", choices=["Python Pytest", "Python Robot", "Karate", "Cypress", "K6", "Test NG"], elem_classes='custom-dropdown')
                            model_structure_final = gr.Json(visible=False) 
                            swagger_result = gr.Json(visible=False)
                            swagger_json = gr.Json(visible=False)
                            api_additional_inputs = gr.Textbox(label="Additional Inputs: ", lines=3, elem_classes="custom-textbox")
                        with gr.Column(min_width=0, scale=1): pass

                    with gr.Row():
                        with gr.Column(min_width=0, scale=3): pass
                        with gr.Column(min_width=0, scale=2):
                            api_endpoints_submit_button = gr.Button("Submit", scale=1, elem_classes="custom-button")
                        with gr.Column(min_width=0, scale=3): pass

                    

                    api_endpoints_submit_button.click(fn=get_api_test_result_page_2,
                                                    inputs=[all_endpoints, api_additional_inputs, api_test_framework, model_structure_final, swagger_result, swagger_json ],
                                                    outputs=api_output_code)

                    api_endpoints_submit_button.click(fn=get_api_test_result_page_1,
                                                    inputs=[all_endpoints, api_additional_inputs, api_test_framework, model_structure_final, swagger_result, swagger_json ],
                                                    outputs=[api_endpoint_selection_page, api_api_result_page])
                    
                with gr.Column(min_width=0, scale=1): pass 

            with gr.Row(visible=True) as api_testing_home_screen:
                with gr.Column(min_width=0): pass
                with gr.Column():
                    with gr.Row():
                        swagger_file = gr.File(label="Upload API Definitions")
                    with gr.Row():
                        with gr.Column(min_width=0, scale=3): pass
                        with gr.Column(min_width=0, scale=2):
                            submit_swagger_file = gr.Button("Submit", scale=1, elem_classes="custom-button")
                        with gr.Column(min_width=0, scale=3): pass
                with gr.Column(min_width=0): pass

            submit_swagger_file.click(fn=get_api_endpoint_selection_page,
                                    inputs=[swagger_file],
                                    outputs=[api_testing_home_screen, all_endpoints, api_endpoint_selection_page, model_structure_final, swagger_result, swagger_json ])
                

            
                
            with gr.Row() as home_button:
                gr.HTML(refresh_script)

        with gr.Column(visible=False) as synthetic_data_test_page:
            with gr.Row(visible=True):
                pass

            with gr.Row():
                gr.HTML(refresh_script)

        with gr.Column(visible=False) as settings_page:
            with gr.Row(visible=True, elem_id="Logos") as logos:
                with gr.Column(scale=1, min_width=0):
                    with gr.Row(): pass
                    with gr.Row():
                        gr.HTML("""<div style="display: flex; align-items: value; justify-content: left;">
                                <img src='file/assets/accion.png' style="height: 30px; width: auto;" alt="Left Logo">
                                </div>
                                """)
                                
                with gr.Column(scale=8, min_width=30):
                    gr.Markdown("""
                                    <h1 style="display: flex; justify-content: center;">
                                        Settings
                                    </h1>
                                """)


                with gr.Column(scale=1, min_width=0):
                    gr.HTML("""<div style="display: flex; justify-content: right;">
                            <img src='file/assets/client.png' style="height: 60px; width: auto;" alt="Right Logo">
                            </div>
                            """)


            with gr.Row():
                with gr.Column(scale=1, min_width=0): pass
                with gr.Column(scale=2, min_width=0): 
                    radio = gr.Radio(
                        choices=["OpenAI", "Gemini", "LLama2"], 
                        label="Choose Model Of Interest",
                        value=llm_model,
                        elem_classes='custom-radio',    
                    )
                    llm_auth_key = gr.Textbox(label="Enter LLM Auth Key", scale=0, lines=3, elem_classes="custom-textbox")
                with gr.Column(scale=1, min_width=0): pass
            
            # with gr.Row():
            #     with gr.Column(scale=2, min_width=0): pass
            #     with gr.Column(min_width=10, scale=3):
            #         llm_auth_key = gr.Textbox(label="Enter LLM Auth Key", scale=0, lines=3, elem_classes="custom-textbox")
            #     with gr.Column(scale=2, min_width=0): pass
            
            with gr.Row(visible=False) as acknowledge_llm_update:
                gr.Markdown("""
                                    <h2 style="display: flex; justify-content: center;">
                                        Updated model!
                                    </h2>
                                """)

            with gr.Row():
                with gr.Column(scale=6, min_width=0): pass
                with gr.Column(scale=1, min_width=60):
                    llm_submit_button = gr.Button("Submit", scale=1, elem_classes="custom-button")
                    llm_submit_button.click(fn=remove_updated_html,
                                            outputs=acknowledge_llm_update
                                            )
                    
                    llm_submit_button.click(fn=update_llm,
                                            inputs=[radio, llm_auth_key],
                                            outputs=acknowledge_llm_update)
                with gr.Column(scale=6, min_width=0): pass
            
            with gr.Row():
                gr.HTML(refresh_script)

        with gr.Column(visible=False) as performance_test_page: 
            with gr.Row():
                gr.HTML(refresh_script)
        
        ui_page_button.click(go_to_ui_test_page, 
                      outputs=[home_page, ui_test_page, api_test_page, synthetic_data_test_page, settings_page, performance_test_page])
        
        api_page_button.click(go_to_api_test_page, 
                      outputs=[home_page, ui_test_page, api_test_page, synthetic_data_test_page, settings_page, performance_test_page])
        
        synthetic_data_page_button.click(go_to_synthetic_data_test_page, 
                      outputs=[home_page, ui_test_page, api_test_page, synthetic_data_test_page, settings_page, performance_test_page])
        
        settings_page_button.click(go_to_settings_page, 
                      outputs=[home_page, ui_test_page, api_test_page, synthetic_data_test_page, settings_page, performance_test_page])
        
        performance_page_button.click(go_to_performance_testing_page, 
                      outputs=[home_page, ui_test_page, api_test_page, synthetic_data_test_page, settings_page, performance_test_page])

    return application


with gr.Blocks(css="./assets/styles.css", fill_width=True) as demo:
    home = home_page()


demo.launch()
