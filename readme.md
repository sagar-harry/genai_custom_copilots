First time setup:
python -m venv genai_venv
cd genai_venv/Scripts
activate
cd ..
cd ..
pip install -r requirements.txt
python main.py

<br>
<br>


Normal run:
cd genai_venv/Scripts
activate
cd ..
cd ..
python main.py

<br>
<br>

# Simplified Documentation for API Endpoints

## 1. UI Testing Endpoint
**URL**: `/uitesting/submit`
**Method**: POST

**Description**: Generates UI test code based on input criteria.

**Required Inputs**:
- `acceptance_criteria`: The criteria for validating the UI.
- `locators`, `additional_details`, `test_framework`, `language`: Optional details for generating tests.

**Responses**:
- **200**: Success with generated code.
- **400**: Missing `acceptance_criteria`.
- **405**: Only POST method is allowed.

---

## 2. API Definitions Endpoint
**URL**: `/apitesting/apidefinitions/submit`
**Method**: POST

**Description**: Extracts API endpoints from a Swagger file.

**Required Inputs**:
- `api_definitions_file`: The Swagger file to process.

**Responses**:
- **200**: Success with extracted endpoints.
- **400**: Missing file.
- **405**: Only POST method is allowed.

---

## 3. API Testing Endpoint
**URL**: `/apitesting/submit`
**Method**: POST

**Description**: Generates API test code based on selected endpoints.

**Required Inputs**:
- `api_definitions_file`: Swagger file for API definitions.
- `selected_endpoints`, `framework`, `additional_inputs`: Details for test generation.

**Responses**:
- **200**: Success with generated code.
- **400**: Missing file or inputs.
- **405**: Only POST method is allowed.

---

## 4. Update LLM Settings Endpoint
**URL**: `/settings/submit`
**Method**: POST

**Description**: Updates the LLM model and authentication key.

**Required Inputs**:
- `llm_model`: Name of the LLM model.
- `auth_key`: Base64-encoded authentication key.

**Responses**:
- **200**: Success.
- **400**: Invalid or missing inputs.
- **405**: Only POST method is allowed.

---

## General Notes
- All endpoints require POST requests.
- Missing required inputs return a **400 Bad Request**.
- Unsupported methods return a **405 Method Not Allowed**.
