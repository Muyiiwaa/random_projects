from zenml import step
from zenml.logger import get_logger
import pandas as pd
from typing import Optional,Tuple
from typing_extensions import Annotated
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
import joblib


logger = get_logger(__name__)



@step
def model_training(X_train: pd.DataFrame, X_test:pd.DataFrame,
                   y_train:pd.Series, y_test:pd.Series) -> Optional[RandomForestClassifier]:
    """This function trains the base model. """
    model = None
    try:
        model = RandomForestClassifier(random_state= 23)
        model.fit(X_train, y_train)
        train_preds = model.predict(X_train)
        test_preds = model.predict(X_test)

        logger.info(msg = f"""Training completed with the following metrics.
                    train_precision: {precision_score(y_train, train_preds)},
                    test_precision: {precision_score(y_test, test_preds)},
                    train_recall: {recall_score(y_train, train_preds)},
                    test_recall: {recall_score(y_test, test_preds)},
                    train_f1: {f1_score(y_train, train_preds)},
                    test_f1: {f1_score(y_test, test_preds)}""")
        joblib.dump(value=model, filename="base_model.pkl")
    except Exception as e:
        logger.error(f"An error occured. Details: {e}")
    
    return model

if __name__ == "__main__":
    pass
