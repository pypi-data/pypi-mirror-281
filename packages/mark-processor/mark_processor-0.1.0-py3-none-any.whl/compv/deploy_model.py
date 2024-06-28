from azure.ai.ml import MLClient
from azure.identity import ClientSecretCredential
from azure.ai.ml.entities import ManagedOnlineDeployment, CodeConfiguration

# Azure ML credentials and workspace details
subscription_id = "0a94de80-6d3b-49f2-b3e9-ec5818862801"
resource_group = "buas-y2"
workspace_name = "CV3"
tenant_id = "0a33589b-0036-4fe8-a829-3ed0926af886"
client_id = "a2230f31-0fda-428d-8c5c-ec79e91a49f5"
client_secret = "Y-q8Q~H63btsUkR7dnmHrUGw2W0gMWjs0MxLKa1C"

# Authenticate and create an MLClient
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)

# Get the endpoint details
endpoint_name = "modelprimary06121627240351"
endpoint = ml_client.online_endpoints.get(endpoint_name)
print(f"Endpoint {endpoint_name} exists with ARM ID: {endpoint.id}")

# Define the deployment
deployment_name = "deployment1"  # The name of the deployment you want to create/update

deployment = ManagedOnlineDeployment(
    name=deployment_name,
    endpoint_name=endpoint_name,  # Use the existing endpoint name
    model="/subscriptions/0a94de80-6d3b-49f2-b3e9-ec5818862801/resourceGroups/buas-y2/providers/Microsoft.MachineLearningServices/workspaces/CV3/models/primary_model/versions/1", # Use the existing model version
    environment="/subscriptions/0a94de80-6d3b-49f2-b3e9-ec5818862801/resourceGroups/buas-y2/providers/Microsoft.MachineLearningServices/workspaces/CV3/environments/newCV3environment4/versions/3", # Use the existing environment version
    code_configuration=CodeConfiguration(
        code="./src",  # Path to the scoring script
        scoring_script="score.py"  # The scoring script file
    ),
    instance_type="Standard_DS3_v2",
    instance_count=1
)

# Create or update the deployment
deployment = ml_client.online_deployments.begin_create_or_update(deployment).result()

# Optionally set the new deployment as the default if it's a new deployment
endpoint = ml_client.online_endpoints.get(endpoint_name)
if not endpoint.default_deployment or endpoint.default_deployment != deployment_name:
    endpoint.default_deployment = deployment_name
    ml_client.online_endpoints.begin_create_or_update(endpoint).result()

print(f"Deployment {deployment_name} is ready on endpoint {endpoint_name}")
