import os

import cv2
import matplotlib.pyplot as plt
import typer

from data_loading import load_data_generators, validate_dataset
from data_preprocessing import preprocess_images
from instance_segmentation import segment_instances
from landmarks_detection import detect_landmarks
from mask_prediction import predict_mask
from model_creation import build_model, load_pretrained_model
from model_training import hyperparameter_search, save_model, train_model
from root_length_measurement import measure_root_lengths


def train_new_model(
    new_model_name, custom_dataset_path=None, custom_hyperparameters=None
):
    """
    Train a new model using either a custom dataset or a default testing dataset.

    :param new_model_name: Name of the new model to be saved.
    :type new_model_name: str
    :param custom_dataset_path: Path to a custom dataset directory.
    :type custom_dataset_path: str, optional
    :param custom_hyperparameters: Dictionary containing custom hyperparameters for model training.
    :type custom_hyperparameters: dict, optional
    :author: Rens van den Berg

    **Usage:**

    This function allows training a new model either with a custom dataset or a default testing dataset.

    **Example:**

    .. code-block:: python

        from your_module import train_new_model

        train_new_model("my_custom_model", "my_custom_dataset", custom_hyperparameters)

    **Details:**

    - If `custom_dataset_path` is provided, it preprocesses images and loads data generators from the custom dataset.
    - If `custom_hyperparameters` is provided, it trains the model with custom hyperparameters.
    - Otherwise, it performs hyperparameter search to find the best model configuration.

    The trained model is saved in the directory `user_custom_models` with the specified `new_model_name`.
    """

    # If custom dataset path is given, preprocess the images and load the data generators, else load the default dataset
    if custom_dataset_path:
        # preprocess_images(
        #     f"data/user_custom_datasets/{custom_dataset_path}/dataset_raw",
        #     f"data/user_custom_datasets/{custom_dataset_path}/dataset_patched",
        # )
        # print("Images preprocessed successfully")

        (
            (train_generator, train_length),
            (test_generator, test_length),
            (val_generator, val_length),
        ) = load_data_generators(f"data/user_custom_datasets/{custom_dataset_path}")
        print("Data generators loaded successfully")

    else:
        (
            (train_generator, train_length),
            (test_generator, test_length),
            (val_generator, val_length),
        ) = load_data_generators("data/testing_dataset")
        print("Data generators loaded successfully")

    # If no hyperparameters given, train the model with default hyperparameters, else perform hyperparameter search
    if custom_hyperparameters is None:
        print("Performing hyperparameter search")
        model, history, best_hypeparameters = hyperparameter_search(
            train_generator, train_length, val_generator, val_length
        )
        print(
            "Hyperparameter search completed and the best model is trained successfully.",
            "Best hyperparameters:",
            best_hypeparameters,
        )

    else:
        print("Training the model with custom hyperparameters:", custom_hyperparameters)
        model = build_model(
            num_filters=custom_hyperparameters["num_filters"],
            dropout_rate=custom_hyperparameters["dropout_rate"],
            learning_rate=custom_hyperparameters["learning_rate"],
        )
        model, history = train_model(
            model,
            train_generator,
            train_length,
            val_generator,
            val_length,
            epochs=custom_hyperparameters["epochs"],
        )
        print("Model trained successfully")

    print("Evaluating the model")
    # TODO evaluate_model(model, history, validation_data_generator)

    save_model(model, f"user_custom_models/{new_model_name}.h5")
    print("Model saved successfully", f"user_custom_models/{new_model_name}.h5")


def predict_using_custom_model(image_path, custom_model_name):
    
    """
    Perform inference using a custom-trained model on a given image.

    :param image_path: Path to the input image.
    :type image_path: str
    :param custom_model_name: Name of the custom-trained model to load.
    :type custom_model_name: str
    :author: Michal Dziechciarz

    **Usage:**

    This function loads a custom-trained model and performs inference on a specific image.

    **Example:**

    .. code-block:: python

        from your_module import predict_using_custom_model

        predict_using_custom_model("path/to/my_image.png", "my_custom_model")

    **Details:**

    - Loads a pre-trained custom model from the `user_custom_models` directory.
    - Uses the model to predict a segmentation mask, detect landmarks, and measure root lengths from the input image.
    - Displays the original image, segmentation mask, and outputs the detected landmarks and root lengths.

    This function is suitable for deploying and testing custom-trained models on new images.
    """

    # Load the model
    model = load_pretrained_model(f"user_custom_models/{custom_model_name}.h5")

    # Predict the mask
    mask = predict_mask(model, image_path)
    segmentation_mask = segment_instances(mask)
    landmarks = detect_landmarks(mask)
    root_lengths = measure_root_lengths(mask)

    for i, plant in enumerate(landmarks):
        print()
        print(f"Plant {i}:")
        print(f"Primary root start: {plant['primary_root_start']}")
        print(f"Primary root end: {plant['primary_root_end']}")
        print(f"Lateral root tips: {plant['l_root_tips']}")
        print(f"Primary root length: {root_lengths[i]['p_root_length']}")

    cv2.imshow("Original Image", cv2.resize(cv2.imread(image_path), (960, 540)))
    cv2.imshow("Segmentation Mask", cv2.resize(segmentation_mask, (960, 540)))
    cv2.waitKey(0)


def predict_using_primary_model(image_path):
    """
    Perform inference using the primary pre-trained model on a given image.

    :param image_path: Path to the input image.
    :type image_path: str
    :author: Michal Dziechciarz

    **Usage:**

    This function loads the primary pre-trained model and performs inference on a specific image.

    **Example:**

    .. code-block:: python

        from your_module import predict_using_primary_model

        predict_using_primary_model("path/to/my_image.png")

    **Details:**

    - Loads the pre-trained primary model from the `models` directory.
    - Uses the model to predict a segmentation mask, detect landmarks, and measure root lengths from the input image.
    - Displays the original image, segmentation mask, and outputs the detected landmarks and root lengths.

    This function is suitable for deploying and testing the primary model on new images.
    """

    # Load the model
    model = load_pretrained_model("models/primary.h5")

    # Predict the mask
    mask = predict_mask(model, image_path)
    segmentation_mask = segment_instances(mask)
    landmarks = detect_landmarks(mask)
    root_lengths = measure_root_lengths(mask)

    for i, plant in enumerate(landmarks):
        print()
        print(f"Plant {i}:")
        print(f"Primary root start: {plant['primary_root_start']}")
        print(f"Primary root end: {plant['primary_root_end']}")
        print(f"Lateral root tips: {plant['l_root_tips']}")
        print(f"Primary root length: {root_lengths[i]['p_root_length']}")

    cv2.imshow("Original Image", cv2.resize(cv2.imread(image_path), (960, 540)))
    cv2.imshow("Segmentation Mask", cv2.resize(segmentation_mask, (960, 540)))
    cv2.waitKey(0)


app = typer.Typer()


@app.command()
def infer(img_path: str, custom_model_name: str = typer.Argument(default=None)):
    """
    Perform inference on an image using a specified custom model or the primary model if no custom model is specified.

    :param img_path: Path to the input image.
    :type img_path: str
    :param custom_model_name: Name of the custom-trained model to load.
    :type custom_model_name: str, optional
    :author: Michal Dziechciarz

    **Usage:**

    This function allows performing inference using either a custom model or the primary pre-trained model.

    **Example:**

    .. code-block:: python

        from your_module import infer

        infer("path/to/my_image.png", "my_custom_model")

    **Details:**

    - If `custom_model_name` is provided and the model exists, it uses the custom model for inference.
    - If `custom_model_name` is not provided, it uses the primary model for inference.
    - Displays the original image and segmentation mask, and outputs the detected landmarks and root lengths.

    This function provides flexibility in deploying both custom-trained and primary models for inference.
    """

    if custom_model_name:
        # Check if the user custom model exists
        if os.path.exists(f"models/user_custom_models/{custom_model_name}.h5"):
            predict_using_custom_model(img_path, custom_model_name)
        else:
            print("Model does not exist.")
    else:
        predict_using_primary_model(img_path)


@app.command()
def train(
    new_model_name: str,
    custom_dataset_path: str = typer.Option(None, help="Path to the custom dataset"),
    learning_rate: float = typer.Option(None, help="Learning rate for training"),
    batch_size: int = typer.Option(None, help="Batch size for training"),
    dropout_rate: str = typer.Option(
        None, help="Dropout rates for training, comma-separated"
    ),
    num_filters: str = typer.Option(
        None, help="Number of filters for each layer, comma-separated"
    ),
    epochs: int = typer.Option(None, help="Number of epochs for training"),
):
    """
    Train a new model with optional custom dataset and hyperparameters.

    :param new_model_name: Name of the new model to be saved.
    :type new_model_name: str
    :param custom_dataset_path: Path to a custom dataset directory.
    :type custom_dataset_path: str, optional
    :param learning_rate: Learning rate for training.
    :type learning_rate: float, optional
    :param batch_size: Batch size for training.
    :type batch_size: int, optional
    :param dropout_rate: Dropout rates for training, comma-separated.
    :type dropout_rate: str, optional
    :param num_filters: Number of filters for each layer, comma-separated.
    :type num_filters: str, optional
    :param epochs: Number of epochs for training.
    :type epochs: int, optional
    :author: Michal Dziechciarz

    **Usage:**

    This function trains a new model with specified custom dataset and hyperparameters, if provided.

    **Example:**

    .. code-block:: python

        from your_module import train

        train(
            new_model_name="my_custom_model",
            custom_dataset_path="my_custom_dataset",
            learning_rate=0.001,
            batch_size=32,
            dropout_rate="0.3,0.3,0.3",
            num_filters="64,128,256",
            epochs=50
        )

    **Details:**

    - Checks if the new model name is available.
    - If `custom_dataset_path` is provided, validates the dataset and preprocesses the images.
    - If no hyperparameters are provided, performs hyperparameter search.
    - Otherwise, trains the model with the provided custom hyperparameters.

    The trained model is saved in the directory `user_custom_models` with the specified `new_model_name`.
    """

     # Check if new_model_name is free
    if os.path.exists(f"user_custom_models/{new_model_name}.h5"):
        print("Model name already exists.")
        return

    # # Check if the user custom dataset exists, if not exit
    # if custom_dataset_path and not os.path.exists(f"{custom_dataset_path}"):
    #     print("Dataset does not exist.")
    #     return

    # # Validate the dataset
    # if custom_dataset_path:
    #     print("Validating the dataset")
    #     validate_dataset(custom_dataset_path)

    # if none hyperparameters are given, hyperparameters = None
     # if none hyperparameters are given, hyperparameters = None
    if not any([learning_rate, batch_size, dropout_rate, num_filters, epochs]):
        custom_hyperparameters = None
    else:
        custom_hyperparameters = {
            "learning_rate": learning_rate,
            "batch_size": batch_size,
            "dropout_rate": (
                [float(x) for x in dropout_rate.split(",")] if dropout_rate else None
            ),
            "num_filters": (
                [int(x) for x in num_filters.split(",")] if num_filters else None
            ),
            "epochs": epochs,
        }

    train_new_model(new_model_name, custom_dataset_path, custom_hyperparameters)


if __name__ == "__main__":
    app()
