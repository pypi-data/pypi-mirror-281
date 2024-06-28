import os
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Get environment variables
endpoint_name = os.getenv("ENDPOINT_NAME")
resource_group = os.getenv("RESOURCE_GROUP")
workspace_name = os.getenv("WORKSPACE_NAME")

def get_api_keys(endpoint_name, resource_group, workspace_name):
    # Run the Azure CLI command to get the keys
    result = subprocess.run(
        [
            "az", "ml", "online-endpoint", "get-credentials",
            "--name", endpoint_name,
            "--resource-group", resource_group,
            "--workspace-name", workspace_name
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode != 0:
        print("Error:", result.stderr)
        return None

    # Parse the JSON output
    keys = json.loads(result.stdout)
    return keys

keys = get_api_keys(endpoint_name, resource_group, workspace_name)
if not keys:
    raise RuntimeError("Failed to retrieve API keys")

# Save keys to a file
with open("keys.json", "w") as f:
    json.dump(keys, f)

print("API keys saved to keys.json")
