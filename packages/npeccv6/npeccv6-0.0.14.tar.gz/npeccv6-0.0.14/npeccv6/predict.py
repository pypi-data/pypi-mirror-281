#!/bin/python3
import argparse
from typing import Tuple

import cv2
import keras
import numpy as np
from keras.models import load_model
from keras.utils import custom_object_scope

try:
    # Attempt relative imports (if run as a package module)
    from .data import load_and_preprocess_image
    from .postprocessing import postprocess_prediction, process_image_for_roots
    from .utils import f1, iou, mean_confidence_score, setup_logger

except ImportError:
    # Fallback to absolute imports (if run as a standalone script)
    from postprocessing import postprocess_prediction, process_image_for_roots
    from utils import f1, iou, mean_confidence_score, setup_logger

    from data import load_and_preprocess_image

logger = setup_logger()


def predict(
    model: keras.models.Model,
    image: np.ndarray = None,
    im_path: str = None,
    # save_path: str = "predictions/image.png",
    patch_size: int = 256,
    threshold: float = 0.8,
    scaling_factor: float = 1,
    num_channels: int = 1,
    segment: bool = False,
    expected_nr_plants: int = 5,
) -> Tuple[np.ndarray[int], float]:
    """
    Predict and post-process the mask for the given image.

    Parameters:
        - model (Model): Trained Keras model for prediction.
        - im_path (str): Path to the input image.
        - save_path (str): Path to save the predicted mask. Default is "Predictions/Image.png".
        - patch_size (int): Size of the patches. Default is 256.
        - threshold (float): Threshold value for binarizing the mask. Default is 0.8.
        - scaling_factor (float): Scaling factor for the image. Default is 1.
        - num_channels (int): Number of channels for the image (1 for grayscale, 3 for color). Default is 1.
        - segment (bool): Wether to segment the roots or not. Default is False.
        - expected_nr_plants (int): The expected number of plants to be found. Default is 5.

    Returns:
        - np.ndarray: Predicted binary mask.
        - float: Mean confidence score of prediction
    """
    # Log if the Image is being Loaded
    if im_path is not None:
        logger.info(f"Loading and preprocessing image from path: {im_path}")

    # Preprocess image
    patches, i, j, im = load_and_preprocess_image(
        image, im_path, patch_size, scaling_factor, num_channels
    )

    logger.info("Starting predicting on patches.")

    # Predict
    preds = model.predict(patches / 255)

    # Calculate mean confidence score
    mean_conf_score = mean_confidence_score(preds, threshold)

    logger.info("Prediction completed. Starting post-processing.")

    # Postprocess prediction
    predicted_mask = postprocess_prediction(
        preds, i, j, im, threshold, patch_size, segment, expected_nr_plants
        )

    # Convert binary mask to uint8 image
    predicted_mask = predicted_mask.astype(np.uint8) * 255

    # Save predicted mask
    # logger.info(f"Saving predicted mask to: {save_path}")
    # cv2.imwrite(save_path, predicted_mask)

    logger.info("Predicted mask saved successfully.")
    return predicted_mask, mean_conf_score


def main():
    parser = argparse.ArgumentParser(
        description="Predict a root mask from an image using a trained model."
    )
    parser.add_argument("--image_path", type=str, help="Path to the input image file.")
    parser.add_argument(
        "--save_path", type=str, help="Where to save the predicted mask."
    )
    parser.add_argument(
        "-m",
        "--model_name",
        type=str,
        default="main",
        action="store",
        help="What model name to use. Default is main.",
    )
    parser.add_argument(
        "-p",
        "--patch_size",
        # dest = "patch_size",
        type=int,
        default=256,
        action="store",
        help="How to patch the images for prediction. Default: 256.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        # dest = "threshold",
        type=float,
        default=0.8,
        action="store",
        help="Threshold for the predicted mask. Defult: 0.8.",
    )
    parser.add_argument(
        "-s",
        "--scaling_factor",
        # dest = "scaling_factor",
        type=int,
        default=1,
        action="store",
        help="Scaling factor for the image. Default: 1",
    )
    parser.add_argument(
        "-n",
        "--num_channels",
        # dest = "num_channels",
        type=int,
        choices=[1, 3],
        default=1,
        action="store",
        help="Number of channels to use with image. Default: 1",
    )
    parser.add_argument(
        "--expected_nr_plants",
        # dest = "expected_nr_plants",
        type=int,
        default=5,
        action="store",
        help="Number of expected plant roots in the image. Default: 5",
    )
    parser.add_argument(
        "--models_path",
        type=str,
        default="./models",
        help="Path to models direcotry. Defautl is './modles'",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Load the pretrained model
    with custom_object_scope({"f1": f1, "iou": iou}):
        model = load_model(f"{args.models_path}/{args.model_name}.keras")

    # Predict the mask
    predicted_mask, mean_conf_score = predict(
        model,
        args.image_path,
        args.save_path,
        args.patch_size,
        args.threshold,
        args.scaling_factor,
        args.num_channels,
        args.model_path,
    )

    # Postprocess the image to get info about roots
    root_lengths, root_tip_coords, marked_image = process_image_for_roots(
        predicted_mask, args.expected_nr_plants
    )
    # Log the details
    logger.info(f"Mean confidence score: {mean_conf_score}")
    logger.info(f"Root lengths: {root_lengths}")
    logger.info(f"Root tips coordinates in image (px): {root_tip_coords}")

    # Save the marked mask
    cv2.imwrite(args.save_path, marked_image)


if __name__ == "__main__":
    main()
