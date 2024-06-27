[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/N8yudTb1)

[![Unit Test Check](https://github.com/BorislavNachev220472/GAction/actions/workflows/dev_deployment.yml/badge.svg?branch=main)](https://github.com/BorislavNachev220472/GAction/actions/workflows/dev_deployment.yml) [![Test Environment Check](https://github.com/BorislavNachev220472/GAction/actions/workflows/main_deployment.yml/badge.svg)](https://github.com/BorislavNachev220472/GAction/actions/workflows/main_deployment.yml)

## pyphenotyper

---
PyPhenotyper is a Python library and command-line tool hosted on GitHub, specializing in high throughput phenotyping of
Arabidopsis plants. It automates the measurement of various morphological traits, offering a user-friendly interface for
both novice and advanced users. With its capability to handle large datasets and customizable analysis options,
PyPhenotyper facilitates comprehensive studies of plant growth and development.

## Getting Started

---

### Installing

The pyphenotyper package can be installed using [pip](https://pypi.org/project/pip/):

```sh
pip install pyphenotyper
```

## Usage

pyphenotyper can be used both from the command line and as a Python library.

### Command line usage

The interactive CLI prompts(check below) eliminate the need for command line arguments:

```sh
poetry run python main.py
```

#### CLI interaction

#### 1. Inference Pipeline

----
Starting Pyphenotyper

#### First Prompt

![first_prompt](readme_cli_usage/first_prompt.png)

The first prompt is used as confirmation to ensure that the used put all of the images that they want to analyze in the
folder called 'input'.

#### Second Prompt

![first_prompt](readme_cli_usage/second_prompt.png)

The second prompt gives the user the possibility to either use the pre-trained models or choose their own ones. If **'n'
**
was indicated a third prompt will appear asking the user to provide the full path to the model.

![first_prompt](readme_cli_usage/third_prompt.png)

#### Output

The output of the pipeline is saved in the newly created **timeseries** folder.

The output for each image follows the structure below.

### **./timeseries/**

* **{IMAGE NAME}**
    * **{IMAGE NAME}**
        * **plant_{n}**
            * landmarked_image.png
            * landmarks.xlsx
            * plant_data.xlsx
            * plant_measurements.xlsx
            * root_mask.png
            * shoot_mask.png
            * shoot_root_mask.png
        * image_mask.png
        * measurements.xlsx
        * occlusion_mask.png
        * root_mask.png
        * root_mask_fixed.png
        * root_structure.rsml
        * shoot_structure.rsml
    * **assets**
        * lateral_length.png
        * plant_{n}.png
        * primary_length.png
        * total_length.png
    * {IMAGE NAME}.png

#### 2. Data Preparation Pipeline

#### Requirements

The only extra module it uses is shuttle

from data.data_processing import import padder, patch_image, roi_extraction_coords_direct

#### Usage

To run the script, use the following command in your terminal:

```bash
python data_prep_pipeline.py <image_folder> <masks_folder>
```

- `image_folder`: Path to the folder containing images.
- `masks_folder`: Path to the folder containing masks.

#### Ensure that:

- masks and images are both be in .png format
- there should be at least 10 images (and respective masks) otherwise you won't be able to prepare the data
- the mask of an image should have the exact same name as its corresponding image
- the masks don't have to be normalized (their values between 0 and 1) but it is reccomended as if you don't the script
  will take more time to run

#### Example

```bash
python data_prep_pipeline.py personal_data/images personal_data/masks
```

#### Steps

1. **Validation**: The script checks if the specified folders exist and contain `.png` files. It also ensures that the
   filenames in both folders match and that there are at least 10 images for the split.

2. **Cropping (Optional)**: The script prompts the user to decide whether to crop the images and masks. If cropping is
   chosen, it creates new folders with the cropped images and masks.

3. **Folder Structure Creation**: The script creates the following folder structure in the base directory of the
   provided image and mask folders:
    ```
    train_images/train
    train_masks/train
    val_images/val
    val_masks/val
    test_images/test
    test_masks/test
    ```

4. **Data Splitting**: The script splits the images and masks into training (60%), validation (20%), and test (20%)
   sets, and copies them to the respective folders.

5. **Padding**: The script prompts the user to input a patch size (256 or 512). It pads all the images and masks in the
   created folders to match the specified patch size.

6. **Patching**: The script divides each padded image and mask into smaller patches and saves them with a naming
   convention indicating the original image and patch number.

7. **Cleanup**: The script ensures all files in the matching folders (e.g., `train_images/train`
   and `train_masks/train`) have the same names and deletes the original padded images, keeping only the patches.

#### Functions

- `validate_folder(folder: str, folder_type: str)`: Validates if the folder exists and contains `.png` files.
- `create_folder_structure(base_path: str)`: Creates the required folder structure.
- `split_data(files: list, train_ratio: float, val_ratio: float)`: Splits data into training, validation, and test sets.
- `copy_files(files: list, src_folder: str, dest_folder: str)`: Copies files from the source folder to the destination
  folder.
- `normalize_masks(mask_folder: str)`: Normalizes mask files to be binary (0 and 1). If they are between 0 and 255, they
  are divided by 255.
- `pad_and_save(folder: str, patch_size: int)`: Pads images to the specified patch size and saves them.
- `patch_and_save(folder: str, patch_size: int)`: Patches images into smaller patches and saves the patches.
- `validate_and_cleanup(images_folder: str, masks_folder: str)`: Validates and cleans up the padded images, keeping only
  the patches.
- `main(image_folder: str, masks_folder: str)`: Main function to process images and masks, including validation,
  optional cropping, folder structure creation, data splitting, normalization, padding, patching, and cleanup.

#### Notes

- The cropping functionality is optional and can be skipped.
- The patch size can be specified as either 256 or 512.

#### Purpose

The overall use and purpose of this script is to streamline and automate the preprocessing of image and mask data,
ensuring that they are properly validated, optionally cropped, padded to match patch sizes, divided into patches, and
organized into training, validation, and test sets.

#### Server usage

#### Requirements

The sever usage requires Docker environment.

### Library usage

For more information check out our official [Sphinx documentation](https://probable-umbrella-lnv1ne6.pages.github.io/).

## Versioning

We use [Docker Hub](https://hub.docker.com/) for versioning.

