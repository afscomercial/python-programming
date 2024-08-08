from typing import Dict, Union

PREDICTIONS = []


def read_prediction(prediction_id: str) -> Union[Dict, None]:
    for prediction in PREDICTIONS:
        if prediction["id"] == prediction_id:
            return prediction
    return None

def create_prediction(new_prediction: Dict):
    PREDICTIONS.append(new_prediction)

def update_prediction(updated_prediction: Dict):
    for i in range(len(PREDICTIONS)):
        if PREDICTIONS[i]["id"] == updated_prediction["id"]:
            PREDICTIONS[i] = updated_prediction
            return

def delete_prediction(prediction_id: str):
    global PREDICTIONS
    index_to_remove = None
    # Find the index of the item to be removed
    for index, prediction in enumerate(PREDICTIONS):
        if prediction["id"] == prediction_id:
            index_to_remove = index
            break
    print("Index to remove:", index_to_remove)
    # If found, remove the item
    if index_to_remove is not None:
        PREDICTIONS.pop(index_to_remove)
    else:
        raise ValueError("Prediction with the given ID not found")