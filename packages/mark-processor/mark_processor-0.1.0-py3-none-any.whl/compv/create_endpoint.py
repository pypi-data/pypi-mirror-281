import argparse
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint, IdentityConfiguration
from azure.identity import ClientSecretCredential, InteractiveBrowserCredential
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

# Azure ML credentials and workspace details
subscription_id = "0a94de80-6d3b-49f2-b3e9-ec5818862801"
resource_group = "buas-y2"
workspace_name = "CV3"
tenant_id = "0a33589b-0036-4fe8-a829-3ed0926af886"
client_id = "a2230f31-0fda-428d-8c5c-ec79e91a49f5"
client_secret = "Y-q8Q~H63btsUkR7dnmHrUGw2W0gMWjs0MxLKa1C"

def create_endpoint(endpoint_name):
    print("Creating the endpoint")

    credential = ClientSecretCredential(tenant_id, client_id, client_secret)

    # Create an MLClient using the credential and workspace details
    try:
        ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)
        print(f"MLClient created successfully for subscription: {subscription_id}, resource group: {resource_group}, workspace: {workspace_name}")
    except Exception as e:
        print(f"Failed to create MLClient: {e}")
        return

    try:
        # Try to get the existing endpoint
        endpoint = ml_client.online_endpoints.get(name=endpoint_name)
        print(f"Endpoint {endpoint_name} already exists.")
    except ResourceNotFoundError:
        # If not found, create a new endpoint
        print(f"Endpoint {endpoint_name} not found. Creating a new endpoint.")
        try:
            endpoint = ManagedOnlineEndpoint(
                name=endpoint_name,
                auth_mode="key",
                # identity=IdentityConfiguration(type="SystemAssigned")
            )
            endpoint = ml_client.online_endpoints.begin_create_or_update(endpoint).result()
            print(f"Endpoint {endpoint_name} created successfully.")
        except HttpResponseError as e:
            print(f"Failed to create endpoint: {e.message}")
            return
    except HttpResponseError as e:
        print(f"Failed to retrieve endpoint: {e.message}")
        return

    return endpoint

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint-name", type=str, required=True)
    args = parser.parse_args()
    
    create_endpoint(args.endpoint_name)
