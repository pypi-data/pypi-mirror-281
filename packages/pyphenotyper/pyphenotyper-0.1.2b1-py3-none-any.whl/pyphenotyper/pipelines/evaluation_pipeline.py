import os
import logging
import typer
from pathlib import Path
from keras.models import load_model

from pyphenotyper.pipelines.data_generators import create_generators
from pyphenotyper.utils.metrics import f1, iou

from azure.ai.ml import MLClient
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Model
from azure.identity import ClientSecretCredential

# Create a Typer app
app = typer.Typer()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.command()
def main(
        patch_size: int = typer.Option(256, help="Patch size for image segmentation"),
        patch_dir: str = typer.Option(..., help="Directory containing the data patches"),
        batch_size: int = typer.Option(32, help="Batch size for data generators"),
        model_path: str = typer.Option(..., help="Path to the trained model"),
        cloud: bool = typer.Option(False, help="Flag to indicate cloud environment"),

) -> None:
    """
    Evaluate UNet model on test data using specified model parameters.

    Authors: Francisco Ribeiro Mansilha, 220387@buas.nl

    :param patch_size: Size of patches for training.
    :param patch_dir: Directory containing the patched data for the test.
    :param batch_size: Batch size for training.
    :param model_path: Path to save the trained model.
    :param cloud: Flag to use cloud storage.
    """
    # Set TensorFlow log level to minimize logs
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # Create data generators
    logger.info("\nCreating data generators...")
    _, _, test_gen, (_, _, test_count) = create_generators(patch_dir, patch_size, batch_size)
    logger.info("Data generators created successfully.")

    # Load the model
    logger.info("\nLoading model...")
    if cloud and os.path.isdir(model_path):
        model_path += '/' + os.listdir(Path(model_path))[0]
    if model_path.endswith('.h5'):
        model = load_model(model_path, custom_objects={'f1': f1, 'iou': iou})
    else:
        model = load_model(model_path)
    logger.info(f"Model loaded from {model_path}.")

    # Evaluate the model
    logger.info("\nEvaluating model on test data...")
    score = model.evaluate(test_gen, steps=test_count)
    logger.info("\nModel evaluation completed.")

    # Log evaluation metrics
    logger.info(f'\nTest Loss: {score[0]}')
    logger.info(f'Test Accuracy: {score[1]}')
    logger.info(f'Test F1 Score: {score[2]}')
    logger.info(f'Test IoU: {score[3]}')

    f1_score, iou_score = score[2], score[3]

    threshold_f1 = 0.82
    thresholded_iou = 0.81

    # Register the model if accuracy is above threshold
    if cloud:
        if f1_score > threshold_f1 or iou_score > thresholded_iou:

            logger.info("Model accuracy is above threshold, registering model.")

            # Define your Azure ML settings
            subscription_id = "0a94de80-6d3b-49f2-b3e9-ec5818862801"
            resource_group = "buas-y2"
            workspace_name = "CV2"
            tenant_id = "0a33589b-0036-4fe8-a829-3ed0926af886"
            client_id = "a2230f31-0fda-428d-8c5c-ec79e91a49f5"
            client_secret = "Y-q8Q~H63btsUkR7dnmHrUGw2W0gMWjs0MxLKa1C"

            credential = ClientSecretCredential(tenant_id, client_id, client_secret)

            ml_client = MLClient(
                credential, subscription_id, resource_group, workspace_name
            )

            model = Model(
                path=model_path,
                type=AssetTypes.CUSTOM_MODEL,
                name=f"CostumModel-f1-{f1_score}-iou{iou_score}",
                description="Model created from pipeline",
            )

            # Register the model
            model = ml_client.models.create_or_update(model)
            logger.info("Model registered.")
        else:
            logger.info("Model metrics are not above threshold, not registering model.")


if __name__ == "__main__":
    app()
