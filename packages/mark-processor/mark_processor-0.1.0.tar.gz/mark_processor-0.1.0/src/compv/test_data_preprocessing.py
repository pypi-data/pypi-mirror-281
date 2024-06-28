import os
import pytest
import cv2
import numpy as np
from data_preprocessing import preprocess_images, get_mask_type


# Mock the padder function from the utils module
@pytest.fixture
# Test preprocess_images function
def test_preprocess_images(tmpdir):
    input_dataset_path = "path/to/input/dataset"
    output_dataset_path = tmpdir.mkdir("output_dataset")

    preprocess_images(input_dataset_path, output_dataset_path)

    # Check if output directory and files are created
    assert os.path.exists(output_dataset_path)
    assert os.path.exists(os.path.join(output_dataset_path, "images", "train"))
    assert os.path.exists(os.path.join(output_dataset_path, "images", "val"))
    assert os.path.exists(os.path.join(output_dataset_path, "images", "test"))

    # Check if the number of output files matches the expected number
    expected_output_files = 0  # Update this with the expected number of output files
    assert (
        len(os.listdir(os.path.join(output_dataset_path, "images", "train")))
        == expected_output_files
    )
    assert (
        len(os.listdir(os.path.join(output_dataset_path, "images", "val")))
        == expected_output_files
    )
    assert (
        len(os.listdir(os.path.join(output_dataset_path, "images", "test")))
        == expected_output_files
    )


# Test get_mask_type function
def test_get_mask_type():
    # Test with valid filename
    filename = "image_root_mask.tif"
    assert get_mask_type(filename) == "root"

    # Test with invalid filename
    filename = "image_invalid_mask.tif"
    assert get_mask_type(filename) == None


if __name__ == "__main__":
    pytest.main()
