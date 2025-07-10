from zenml import pipeline
from steps.data_loader import load_data
from steps.data_preprocessing import encode_categoricals,scale_dataset,split_dataset
from steps.trainer import model_training
from zenml.logger import get_logger


logger = get_logger(__name__)


@pipeline(enable_cache=False)
def diabetes_pipeline():
    data = load_data()
    data = encode_categoricals(data=data)
    X_train, X_test, y_train, y_test = split_dataset(data)
    X_train, X_test = scale_dataset(X_train, X_test)
    model = model_training(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    diabetes_pipeline()

