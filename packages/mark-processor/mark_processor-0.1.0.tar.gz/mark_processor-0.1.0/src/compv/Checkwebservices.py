from azureml.core import Workspace, Webservice
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to Azure ML Workspace
ws = Workspace.get(
    name=os.getenv("WORKSPACE_NAME"),
    subscription_id=os.getenv("SUBSCRIPTION_ID"),
    resource_group=os.getenv("RESOURCE_GROUP")
)

# List all webservices in the workspace
services = Webservice.list(ws)
for service in services:
    if isinstance(service, Webservice):
        print(f"Name: {service.name}, Type: {service.compute_type}")
    else:
        print("Found an unknown or invalid webservice entry.")
