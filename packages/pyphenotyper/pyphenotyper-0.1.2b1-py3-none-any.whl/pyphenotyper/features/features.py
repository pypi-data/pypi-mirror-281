import os

import cv2
import numpy as np
import pandas as pd
from patchify import unpatchify
from rich.progress import track

from pyphenotyper.data.data_processing import padder, roi_extraction_coords_direct, patch_image, \
    set_outside_pixels_to_zero
from pyphenotyper.logger_config import logger
from pyphenotyper.utils.helpers import load_image, create_folder, structure_folders, load_images_from_folder


def model_predict_image(image_path: str, patch_size: int, model) -> np.ndarray:
    """
    Create mask by using provided model to predict the input image.

    Authors: Vlad Matache, 224108@buas.nl
             Francisco Ribeiro Mansilha, 220387@buas.nl

    :param image_path: Path to the image.
    :param patch_size: Size of the patch.
    :param model: Model to use for prediction.
    :return: Predicted mask.
    """

    # Load the image
    image = load_image(image_path)
    image = padder(image, patch_size)
    # Extracting coordinates for ROI
    min_x, max_x, min_y, max_y = roi_extraction_coords_direct(image)

    # Preparing patches for prediction
    patches, shape = patch_image(image, patch_size)

    # Predict with the root model (segmentation_model)
    predictions = model.predict(patches / 255.0, verbose=0)
    predictions = predictions.reshape(
        shape[0], shape[1], patch_size, patch_size)
    predictions = unpatchify(predictions, image.shape)
    predictions = (predictions > 0.5).astype(np.uint8)
    predictions = set_outside_pixels_to_zero(
        predictions, min_x, max_x, min_y, max_y)
    return predictions


def model_fix_occlusion(root_mask: np.ndarray, patch_size: int, model, refinement_steps: int = 10,
                        verbose: bool = True) -> np.ndarray:
    """
    Fix occlusion in the mask by using provided model to predict the input image.

    Authors: Vlad Matache, 224108@buas.nl
             Francisco Ribeiro Mansilha, 220387@buas.nl

    :param image_path: Path to the image.
    :param patch_size: Size of the patch.
    :param model: Model to use for prediction.
    :param refinement_steps: Number of refinement steps.
    :param verbose: Print additional information.
    :return: Fixed mask.
    """
    logger.info("Fixing occlusion in the mask...")
    for i in range(refinement_steps + 1):
        logger.info(f"Refinement step: {i} / {refinement_steps}")
        # Preparing patches for prediction
        patches, shape = patch_image(root_mask, patch_size)

        # Predict with the root model (segmentation_model)
        predictions = model.predict(patches / 255.0, verbose=0)
        predictions = predictions.reshape(
            shape[0], shape[1], patch_size, patch_size)
        predictions = unpatchify(predictions, root_mask.shape)
        predictions = (predictions > 0.5).astype(np.uint8)
        # Calculate the occlusion mask
    logger.info("Occlusion fixed...")
    return predictions


def model_create_masks(image_path: str, patch_size: int, segmentation_model, occlusion_inpainter, shoot_model,
                       refinement_steps: int = 10, verbose: bool = True) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Predict root and shoot masks for the given image using segmentation models.

    Authors: Vlad Matache 224108@buas.nl
             Francisco Ribeiro Mansilha 220387@buas.nl


    :param image_path: Image path.
    :param patch_size: Size of the patch.
    :param segmentation_model: Pre-loaded segmentation model.
    :param patching_model: Model or function for handling image patching.
    :param shoot_model: Pre-loaded shoot model.
    :return: Root and shoot masks.
    """
    # Load the image
    image = load_image(image_path)
    original_image = image.copy()
    image = padder(image, patch_size)
    difference_x = image.shape[0] - original_image.shape[0]
    difference_y = image.shape[1] - original_image.shape[1]
    difference_x = difference_x // 2
    difference_y = difference_y // 2

    logger.info("Creating masks...")
    root_mask = model_predict_image(image_path, patch_size, segmentation_model)
    logger.info("Created root mask...")
    shoot_mask = model_predict_image(image_path, patch_size, shoot_model)
    shoot_mask = shoot_mask[difference_x: -difference_x, difference_y: -difference_y]
    logger.info("Created shoot mask...")
    occlusion_mask = model_fix_occlusion(
        root_mask, patch_size, occlusion_inpainter, refinement_steps)
    occlusion_mask = occlusion_mask[difference_x: -difference_x, difference_y: -difference_y]
    root_mask = root_mask[difference_x: -difference_x, difference_y: -difference_y]
    logger.info("Created occlusion mask...")

    return root_mask, shoot_mask, occlusion_mask


def shorten_petri_dish_filename(filename: str) -> str:
    return filename.split('-')[0] + '-' + filename.split('-')[1]


def save_prediction_for_image(image_path: str, filename: str, root_segmentation_model, occlusion_inpainter,
                              shoot_segmentation_model, padder, refinement_steps: int = 10,
                              verbose: bool = True, timeline_folder: str = "") -> None:
    """
    Saves predictions from root and shoot segmentation models for each image in the specified input folder.

    Author: Francisco Ribeiro Mansilha 220387@buas.nl


    :param image_path: Path to the image.
    :param filename: Name of the image file(used for output).
    :param root_segmentation_model: Pre-loaded root segmentation model.
    :param patching_model: Model or function for handling image patching.
    :param shoot_segmentation_model: Pre-loaded shoot segmentation model.
    :param padder: Function to pad images to the required size.
    """
    # Load image
    image = load_image(image_path)
    if verbose:
        logger.info(f"Loaded image: {filename} with shape: {image.shape}")

    # Predict the root, shoot, and occlusion masks
    root_mask, shoot_mask, occlusion_mask = model_create_masks(image_path, 256, root_segmentation_model,
                                                               occlusion_inpainter,
                                                               shoot_model=shoot_segmentation_model,
                                                               refinement_steps=refinement_steps)

    full_root_mask = root_mask + occlusion_mask
    folder_name = timeline_folder + "/" + filename.replace('.png', '')
    create_folder(f"timeseries/{folder_name}")
    # Save the root mask
    cv2.imwrite(f"timeseries/{folder_name}/root_mask.png", root_mask * 255)
    if verbose:
        logger.info(f"Root mask saved for: {filename}")

    # Save the shoot mask
    cv2.imwrite(f"timeseries/{folder_name}/shoot_mask.png", shoot_mask * 255)
    if verbose:
        logger.info(f"Shoot mask saved for: {filename}")

    # Save the occlusion mask
    cv2.imwrite(f"timeseries/{folder_name}/occlusion_mask.png", occlusion_mask * 255)
    if verbose:
        logger.info(f"Occlusion mask saved for: {filename}")

    # Save the full root mask
    cv2.imwrite(f"timeseries/{folder_name}/root_mask_fixed.png", full_root_mask * 255)
    if verbose:
        logger.info(f"Full root mask saved for: {filename}")


def save_prediction_for_folder(input_folder: str, root_segmentation_model, occlusion_inpainter,
                               shoot_segmentation_model, padder, refinement_steps: int = 10,
                               verbose: bool = True) -> None:
    """
    Saves predictions from root and shoot segmentation models for each image in the specified input folder.

    Authors: Vlad Matache, 224108@buas.nl

    :param input_folder: Path to the input folder containing images.
    :param root_segmentation_model: Pre-loaded root segmentation model.
    :param patching_model: Model or function for handling image patching.
    :param shoot_segmentation_model: Pre-loaded shoot segmentation model.
    :param padder: Function to pad images to the required size.
    :param refinement_steps: Number of refinement steps.
    :param verbose:  logger.info additional information.
    """
    input_folder = structure_folders(input_folder)
    for timeline_folder in os.listdir(input_folder):
        logger.info(f"Saving predictions for images in the {timeline_folder}...")
        timeline_folder_path = os.path.join(input_folder, timeline_folder)
        _, filenames, image_paths = load_images_from_folder(timeline_folder_path, verbose)
        # Using tqdm to add a progress bar

        for i in track(range(len(image_paths)), description=f' Processing images for petri dish - {timeline_folder}:'):
            save_prediction_for_image(image_paths[i], filenames[i], root_segmentation_model, occlusion_inpainter,
                                      shoot_segmentation_model, padder, refinement_steps, verbose, timeline_folder)


def overlay_masks_on_image(input_folder: str) -> None:
    """
    Overlay root and shoot masks on original images in the specified input folder.

    Author: Francisco Ribeiro Mansilha 220387@buas.nl


    :param input_folder (str): Path to the input folder containing original images and masks.
    """
    logger.info(f"Overlaying masks on images in the {input_folder}...")
    # Iterate through each subfolder in the input folder
    for root, dirs, files in os.walk(input_folder):
        for subdir in dirs:
            folder_path = os.path.join(root, subdir)
            original_image_path = None
            root_mask_path = None
            shoot_mask_path = None
            occlusion_mask_path = None

            # Identify the required files in each subfolder
            for file in os.listdir(folder_path):
                if file.endswith("_original_padded.png"):
                    original_image_path = os.path.join(folder_path, file)
                elif file.endswith("_root_mask.png"):
                    root_mask_path = os.path.join(folder_path, file)
                elif file.endswith("_shoot_mask.png"):
                    shoot_mask_path = os.path.join(folder_path, file)
                elif file.endswith("_occlusion_mask.png"):
                    occlusion_mask_path = os.path.join(folder_path, file)

            if original_image_path and root_mask_path and shoot_mask_path and occlusion_mask_path:
                # Load the original image
                original_image = load_image(original_image_path)
                original_colored = cv2.cvtColor(
                    original_image, cv2.COLOR_GRAY2BGR)  # Convert to BGR for overlay

                # Load masks
                root_mask = load_image(root_mask_path)
                shoot_mask = load_image(shoot_mask_path)
                occlusion_mask = load_image(occlusion_mask_path)

                # Create colored overlays
                red_overlay = np.zeros_like(original_colored)
                green_overlay = np.zeros_like(original_colored)
                blue_overlay = np.zeros_like(original_colored)

                # Assign colors to the masks (Red for root, Green for shoot, Blue for occlusion)
                red_overlay[root_mask == 255] = [0, 0, 255]
                green_overlay[shoot_mask == 255] = [0, 255, 0]
                blue_overlay[occlusion_mask == 255] = [255, 255, 0]

                # Combine overlays with the original image
                combined_overlay = cv2.addWeighted(
                    original_colored, 1, red_overlay, 0.5, 0)
                combined_overlay = cv2.addWeighted(
                    combined_overlay, 1, green_overlay, 0.5, 0)
                combined_overlay = cv2.addWeighted(
                    combined_overlay, 1, blue_overlay, 0.5, 0)

                # Save the overlayed image
                overlayed_image_path = os.path.join(
                    folder_path, f"{subdir}_overlayed.png")
                cv2.imwrite(overlayed_image_path, combined_overlay)


def get_landmark_data(folder: str) -> pd.DataFrame:
    """This function takes the landmark positions of all plants in an image and concatenates them into a single dataframe; adds a column with the plant number.

    Author: Matache Vlad, 224108@buas.nl
    :return: A dataframe with the landmark positions of all plants in an image and a column with the plant number.
    :rtype: pd.DataFrame
    """
    dataframe_list = []
    for root, _, _ in os.walk(folder):
        plant_nr = root[-7:]
        if 'plant' in plant_nr:
            print(os.path.join(root, 'landmarks.xlsx'))
            landmarks = pd.read_excel(os.path.join(root, 'landmarks.xlsx'), index_col=0)
            landmarks['plant_nr'] = plant_nr
            dataframe_list.append(landmarks)
    return pd.concat(dataframe_list)
