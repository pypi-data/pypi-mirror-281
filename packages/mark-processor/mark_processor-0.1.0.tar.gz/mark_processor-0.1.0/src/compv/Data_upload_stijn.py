import os
from azureml.core import Workspace, Datastore
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.data import FileDataset

subscription_id = "0a94de80-6d3b-49f2-b3e9-ec5818862801"
resource_group = "buas-y2"
workspace_name = "CV3"

# Log in using interactive Auth
auth = InteractiveLoginAuthentication()

# Declare workspace & datastore.
workspace = Workspace(
    subscription_id=subscription_id,
    resource_group=resource_group,
    workspace_name=workspace_name,
    auth=auth,
)

# List all datastores registered in the current workspace
datastores = workspace.datastores
for name, datastore in datastores.items():
    print(name, datastore.datastore_type)

# Create a datastore object from the existing datastore named "workspaceblobstore".
datastore = Datastore.get(workspace, datastore_name="workspaceblobstore")

# Define the source directory using an absolute path
src_dir = "C:/Users/stijn/Desktop/New folder/MNIST-Data-main.zip/MNIST-Data-main"

# Check if the source directory exists and is a directory
if not os.path.isdir(src_dir):
    raise ValueError(f"The src_dir path {src_dir} is not a valid directory.")

# Upload the data to the path target_path in datastore and create a FileDataset
target_path = "mnist"
file_dataset = FileDataset.upload_directory(
    src_dir=src_dir,
    target=(datastore, target_path),
    overwrite=True,
    show_progress=True,
)

# Register the FileDataset
file_dataset = file_dataset.register(
    workspace=workspace,
    name="Nmist8_stijn",
    description="MNIST dataset uploaded by Stijn",
    create_new_version=True,
)

# Create a FileDataset from a path to a directory for the training data
train_set = Dataset.File.from_files(path=(datastore, f"{target_path}/train"))

# Split the dataset into train and validation sets
train_set, val_set = train_set.random_split(0.8, seed=123)

# Create a FileDataset from a path to a directory for the test data
test_set = Dataset.File.from_files(path=(datastore, f"{target_path}/test"))

# Register the datasets
train_reg = train_set.register(workspace=workspace, name='digits_train', description='training data', create_new_version=True)
val_reg = val_set.register(workspace=workspace, name='digits_val', description='validation data', create_new_version=True)
test_reg = test_set.register(workspace=workspace, name='digits_test', description='test data', create_new_version=True)

# List all datasets registered in the current workspace and print their versions
datasets = workspace.datasets
for name, dataset in datasets.items():
    print(f"Name: {name}, Version: {dataset.version}")
