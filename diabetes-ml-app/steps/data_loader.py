from zenml import step
import kagglehub
import os
from zenml.logger import get_logger
import pandas as pd
from typing import Optional
from typing_extensions import Annotated


logger = get_logger(__name__)

url_path = "iammustafatz/diabetes-prediction-dataset"

@step
def load_data(kaggle_path: str = url_path) -> Annotated[Optional[pd.DataFrame], "Data Loading"]:

    data = None
    try:
        # Download latest version
        path = kagglehub.dataset_download(kaggle_path)
        # create a data url
        data_url = os.path.join(path, os.listdir(path)[0])
        # create the pandas dataframe
        data = pd.read_csv(data_url)
        data.head(5)

        logger.info(f"Loaded data successfully from path with shape: {data.shape}")
    except Exception as e:
        logger.error(f"An error occured. Detail: {e}")
    
    return data


if __name__ == "__main__":
    data = load_data()