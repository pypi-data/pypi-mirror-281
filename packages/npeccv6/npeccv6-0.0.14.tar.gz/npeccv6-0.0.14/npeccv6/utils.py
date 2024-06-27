#!/bin/python3
import json
import logging
import os
import shutil
from typing import Dict, Iterable, List

import numpy as np
import tensorflow
import tensorflow.keras.backend as K


def setup_logger(folder: str = "log") -> None:
    """
    Set up a logger that writes log messages to a file and the console.

    This function creates a logger that writes log messages to a specified
    file and the console. The log messages include a timestamp, the logger's
    name, the severity level of the log message, and the message itself.

    Parameters:
        - folder (str): The directory where the log file will be created. Defaults to "log".

    Returns:
        logging.Logger: Configured logger instance.

    Example:
        .. code-block:: python

            logger = setup_logger()
            logger.info("This is an info message.")
    """
    # Check if logger with the same name already exists
    logger = logging.getLogger(__name__)
    if logger.handlers:
        # Logger already configured, return it
        return logger

    filename = "buas_cv6.log"
    path = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)

    # Create a logger object
    logger = logging.getLogger(__name__)

    # Set the logging level
    logger.setLevel(logging.INFO)

    # Create a handler for writing to a file
    file_handler = logging.FileHandler(path)

    # Create a handler for writing to the console
    console_handler = logging.StreamHandler()

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Set up the logger
logger = setup_logger()


def f1(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
    """
    Calculate the F1 score.

    F1 score is the harmonic mean of precision and recall.
    It's a commonly used metric in binary classification tasks.

    Parameters:
        - y_true (Iterable[float]): True labels.
        - y_pred (Iterable[float]): Predicted labels.

    Returns:
        float: The F1 score.
    """

    def recall_m(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_true = tensorflow.cast(y_true, tensorflow.float32)
        y_pred = tensorflow.cast(y_pred, tensorflow.float32)
        TP = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        Positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = TP / (Positives + K.epsilon())
        return recall

    def precision_m(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_true = tensorflow.cast(y_true, tensorflow.float32)
        y_pred = tensorflow.cast(y_pred, tensorflow.float32)
        TP = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        Pred_Positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = TP / (Pred_Positives + K.epsilon())
        return precision

    try:
        precision, recall = precision_m(y_true, y_pred), recall_m(y_true, y_pred)
    except ValueError:
        logger.error(
            f"An ValueError occurred while calculating precision and recall due to mismatched shapes between {y_true.shape = } and {y_pred.shape =}."
        )

    f1_score = 2 * ((precision * recall) / (precision + recall + K.epsilon()))
    return f1_score


def iou(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
    """
    Calculate the Intersection over Union (IoU) score.

    Intersection over Union (IoU) is a measure used to evaluate the
    overlap between two boundaries. In the context of object detection
    or segmentation, it's used to evaluate the accuracy of predicted
    bounding boxes or segmentations against the ground truth.

    Parameters:
        - y_true (Iterable[float]): True labels.
        - y_pred (Iterable[float]): Predicted labels.

    Returns:
        float: The IoU score.
    """

    def f(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_true = tensorflow.cast(y_true, tensorflow.float32)
        y_pred = tensorflow.cast(y_pred, tensorflow.float32)
        intersection = K.sum(K.abs(y_true * y_pred), axis=[1, 2, 3])
        total = K.sum(K.square(y_true), [1, 2, 3]) + K.sum(K.square(y_pred), [1, 2, 3])
        union = total - intersection
        return (intersection + K.epsilon()) / (union + K.epsilon())

    # Default value
    iou_score = 0.0
    try:
        iou_score = K.mean(f(y_true, y_pred), axis=-1)
        logger.debug(f"iou return value - {iou_score}")
    except ValueError:
        logger.error(
            f"An ValueError occurred while calculating iou due to mismatched shapes between {y_true.shape = } and {y_pred.shape = }."
        )
    return iou_score


def clear_destination_folder(image_patch_path: str) -> None:
    """
    Clears the destination folder where the image patch is located. If the folder exists,
    it is removed along with its contents. A new empty folder is then created in the same location.

    Parameters:
        - image_patch_path (str): The file path to the image patch. The folder containing this file will be cleared.

    Returns:
        None
    """
    folder_path = os.path.dirname(image_patch_path)
    if os.path.exists(folder_path):
        logger.info("Clearing destination folder")
        shutil.rmtree(folder_path)
        logger.debug(f"clear_destination_folder - Removing folder: {folder_path}")
    # Create the folder if it doesn't exist
    os.makedirs(folder_path)
    # print(f'Creating folder: {folder_path}')


def mean_confidence_score(predicted_probs: np.ndarray, threshold: float = 0.5) -> float:
    """
    Calculates the mean confidence score of the predicted probabilities that exceed a given threshold.

    Parameters:
        - predicted_probs (Union[np.ndarray, Any]): A numpy array or similar structure containing the predicted probabilities.
        - threshold (float, optional): The threshold above which the predicted probabilities are considered. Default is 0.5.

    Returns:
        - np.ndarray: The mean confidence score of the pixels above the threshold.
    """
    root_pixels = predicted_probs[predicted_probs > threshold]
    return float(np.mean(root_pixels)) if root_pixels.size > 0 else float(0)


def create_config_json(
    model_name: str,         
    input_shape: List[int] = [256, 256, 1],
    output_classes: int = 1,
    optimizer: str = "adam",
    loss: str = "binary_crossentropy",
    output_activation: str = "sigmoid",
    dropout_1: float = 0.1,
    dropout_2: float = 0.2,
    dropout_3: float = 0.3,
    learning_rate: float = 0.001,
    model_path: str = "./models"
) -> None:
    """
    Create or update a JSON configuration file with model parameters.

    Parameters:
        - model_name (str): The name of the model to be added or updated.
        - input_shape (List[int], optional): Input shape of the model. Default is [256, 256, 1].
        - output_classes (int, optional): Number of output classes. Default is 1.
        - optimizer (str, optional): Optimizer for training. Default is "adam".
        - loss (str, optional): Loss function for training. Default is "binary_crossentropy".
        - output_activation (str, optional): Activation function for output layer. Default is "sigmoid".
        - dropout_1 (float, optional): Dropout rate for layer 1. Default is 0.1.
        - dropout_2 (float, optional): Dropout rate for layer 2. Default is 0.2.
        - dropout_3 (float, optional): Dropout rate for layer 3. Default is 0.3.
        - learning_rate (float, optional): Learning rate for model
        - model_path (str): Path to models directory.

    Returns:
        - None
    """
    params = {
        "input_shape": input_shape,
        "output_classes": output_classes,
        "optimizer": optimizer,
        "loss": loss,
        "output_activation": output_activation,
        "dropout_1": dropout_1,
        "dropout_2": dropout_2,
        "dropout_3": dropout_3,
        "learning_rate": learning_rate,
    }
    
    # Log the action of writing parameters to the JSON file
    logger.info(
        f"main - Writing parameters to model_config.json - {model_name}: {params}"
    )

    # Define the path to the configuration JSON file
    path_config_json = f"{model_path}/model_config.json"

    try:
        # Try load existing parameters from the JSON file if it exists
        with open(path_config_json, "r", encoding="utf-8") as json_load:
            config_dict = json.load(json_load)

        # Check if the model name already exists in the configuration
        if model_name in config_dict:
            # Log an error if the model name already exists
            logger.error(f"main - Model with name: {model_name} already exists.")
        else:
            # Add the new model parameters to the configuration dictionary
            config_dict[model_name] = params

        # Write the updated configuration back to the JSON file
        with open(path_config_json, "w", encoding="utf-8") as json_dump:
            json.dump(config_dict, json_dump, indent=4)
            logger.info(f"main - Updated config file and added model: {model_name}.")

    except FileNotFoundError:
        # If the JSON file does not exist, create a new dictionary with the model name as the key and parameters as values
        config_dict = {model_name: params}

        # Write the new configuration dictionary to a new JSON file
        with open(path_config_json, "w", encoding="utf-8") as json_file:
            json.dump(config_dict, json_file)

    except json.JSONDecodeError:
        # Handle JSON decoding error if the file is not properly formatted
        logger.error(
            f"main - JSON decode error while reading the file {path_config_json}."
        )


def read_config(model_name: str, model_path: str = "./models"):
    """
    Reads the configuration for the specified model from a JSON file.

    Parameters:
        model_name (str): The name of the model whose configuration is to be read.
        model_path (str): Path to models directory.

    Returns:
        dict: The configuration dictionary for the specified model.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        KeyError: If the specified model name is not found in the configuration.
        json.JSONDecodeError: If there is an error decoding the JSON file.
    """
    try:
        logger.info("Loading config file.")
        with open(f"{model_path}/model_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        if model_name not in config:
            raise KeyError(
                f"Model '{model_name}' not found in the configuration. You may need to first initialize the model."
            )

        return config[model_name]
    except FileNotFoundError as fnf_error:
        logger.info(f"Error: The configuration file was not found. {fnf_error}")
        raise
    except KeyError as key_error:
        logger.info(f"Error: {key_error}")
        raise
    except json.JSONDecodeError as json_error:
        logger.info(f"Error: Failed to decode JSON. {json_error}")
        raise
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        raise
