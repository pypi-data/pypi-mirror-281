import os
from azure.ai.ml import MLClient, load_component
from azure.identity import InteractiveBrowserCredential

# Create a browser credential
credential = InteractiveBrowserCredential()

# Define your Azure subscription details
subscription_id = "0a94de80-6d3b-49f2-b3e9-ec5818862801"
resource_group = "buas-y2"
workspace_name = "CV3"

# Create an MLClient using the credential and workspace details
ml_client = MLClient(
    credential=credential,
    subscription_id=subscription_id,
    resource_group_name=resource_group,
    workspace_name=workspace_name,
)

# Load the component from YAML
eval_component = load_component(source="C:/Users/stijn/Documents/GitHub/2023-24d-fai2-adsai-group-cv-3/src/evaluation.yml")

# Register the component in the ML workspace
ml_client.components.create_or_update(eval_component)
