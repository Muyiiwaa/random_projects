from zenml import step
from zenml.logger import get_logger
import pandas as pd
from typing import Optional,Tuple
from typing_extensions import Annotated
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib

logger = get_logger(__name__)


@step
def encode_categoricals(data: pd.DataFrame) -> Annotated[pd.DataFrame, "Encoded DataFrame"]:
    try:
        label_encoders = {}
        categorical_columns = list(data.select_dtypes(include ="object").columns)
        for column in categorical_columns:
            encoder = LabelEncoder()
            data[column] = encoder.fit_transform(data[column])
            label_encoders[column] = encoder
        joblib.dump(value=label_encoders, filename="label_encoder.pkl")
        logger.info(f'Encoded the categorical columns successfully')
    except Exception as err:
        logger.error(f'Encountered some error {err} while encoding')

    return data


# split the dataset
@step
def split_dataset(data: pd.DataFrame) -> Tuple[
    Annotated[Optional[pd.DataFrame], "X_train"],
    Annotated[Optional[pd.DataFrame], "X_test"],
    Annotated[Optional[pd.Series], "y_train"],
    Annotated[Optional[pd.Series], "y_test"]]:
    """this function returns the splitted version of the dataset
    ready for training."""
    X_train, X_test, y_train, y_test = None,None,None,None
    try:
        X = data.drop(columns=['diabetes'])
        y = data['diabetes']
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2,
                                                            random_state=23, stratify=y)
        logger.info(f'Splitted the dataframe successfully')
    except Exception as e:
        logger.error(f'An error occured. Details: {e}')
    
    return X_train, X_test, y_train, y_test


@step
def scale_dataset(X_train:pd.DataFrame, X_test:pd.DataFrame) -> Tuple[
    Annotated[Optional[pd.DataFrame], "Scaled X_train"],
    Annotated[Optional[pd.DataFrame], "Scaled X_test"]]:
    """scale the features of the splitted dataset using standard scaler"""
    X_train, X_test
    try:
        scaler = StandardScaler()
        columns = X_train.columns
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        X_train = pd.DataFrame(data = X_train, columns=columns)
        X_test = pd.DataFrame(data=X_test, columns = columns)

        logger.info('Completed scaling X_train and X_test')
        joblib.dump(value=scaler, filename="scaler.pkl")
    except Exception as e:
        X_train, X_test = None, None
        logger.error(f'An error occured. Details: {e}')
    
    return X_train, X_test  


if __name__ == "__main__":
    pass