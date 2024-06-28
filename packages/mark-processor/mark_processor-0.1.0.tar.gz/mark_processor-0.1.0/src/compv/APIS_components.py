import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey
from dotenv import load_dotenv
from azureml.core import Workspace
from azureml.core.webservice import Webservice

# Load environment variables from .env file
load_dotenv()

# FastAPI instance
app = FastAPI()

# API Key security
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == os.getenv("API_KEY"):
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

# Connect to Azure ML Workspace
ws = Workspace.get(
    name=os.getenv("WORKSPACE_NAME"),
    subscription_id=os.getenv("SUBSCRIPTION_ID"),
    resource_group=os.getenv("RESOURCE_GROUP")
)

# List of webservice names (replace these with actual names from your workspace)
component_names = {
    "root_length_measurement": "root_length_measurement_service_name",
    "landmarks_detection": "landmarks_detection_service_name",
    "mask_prediction": "mask_prediction_service_name",
    "data_preprocessing": "data_preprocessing_service_name",
    "model_registration": "model_registration_service_name",
    "model_evaluation": "model_evaluation_service_name",
    "model_training": "model_training_service_name"
}

# Function to call Azure ML component
def call_azure_ml_component(component_name: str):
    """
    Call an Azure ML component by its name and handle the response.

    :param component_name: The name of the Azure ML component to be called.
    :type component_name: str
    :return: A dictionary containing the status of the call and the response data.
    :rtype: dict
    :raises HTTPException: If there is an error in calling the Azure ML component.
    :author: Lea Bancovac

    **Usage:**

    This function can be used to call an Azure ML component by its name and retrieve the response.

    **Example:**

    .. code-block:: python

        from your_module import call_azure_ml_component

        # Call the Azure ML component
        try:
            result = call_azure_ml_component("my_ml_component")
            print(result["status"])  # Should print 'success'
            print(result["data"])  # The response data from the component
        except HTTPException as e:
            print(f"Error: {e.detail}")

    **Details:**

    This function attempts to call an Azure ML component identified by `component_name`. It uses the Azure ML SDK's `Webservice` class to access the service and execute the run. If successful, it returns a dictionary with a status of "success" and the response data. If an error occurs, an `HTTPException` with a status code of 500 is raised, containing the error details.

    """

    try:
        service = Webservice(ws, name=component_name)
        response = service.run()
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to call specific component by name
@app.get("/call_component/{component_name}")
async def call_component(component_name: str, api_key: APIKey = Depends(get_api_key)):
    if component_name not in component_names:
        raise HTTPException(status_code=404, detail="Component not found")
    return call_azure_ml_component(component_names[component_name])

# Example endpoints for each component
@app.get("/root_length_measurement")
async def root_length_measurement(api_key: APIKey = Depends(get_api_key)):
    return await call_component("root_length_measurement", api_key)

@app.get("/landmarks_detection")
async def landmarks_detection(api_key: APIKey = Depends(get_api_key)):
    return await call_component("landmarks_detection", api_key)

@app.get("/mask_prediction")
async def mask_prediction(api_key: APIKey = Depends(get_api_key)):
    return await call_component("mask_prediction", api_key)

@app.get("/data_preprocessing")
async def data_preprocessing(api_key: APIKey = Depends(get_api_key)):
    return await call_component("data_preprocessing", api_key)

@app.get("/model_registration")
async def model_registration(api_key: APIKey = Depends(get_api_key)):
    return await call_component("model_registration", api_key)

@app.get("/model_evaluation")
async def model_evaluation(api_key: APIKey = Depends(get_api_key)):
    return await call_component("model_evaluation", api_key)

@app.get("/model_training")
async def model_training(api_key: APIKey = Depends(get_api_key)):
    return await call_component("model_training", api_key)


# Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)