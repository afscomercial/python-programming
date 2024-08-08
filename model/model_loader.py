import os
from pathlib import Path
import numpy as np
from dotenv import load_dotenv
import pandas as pd
import pickle

load_dotenv() # take environment variables from .env.

class ModelLoader(object):
    def __init__(self, 
                  path: Path, 
                  name: str, 
                  version: float = 1.0):
        self.path = path
        self.name = name
        self.version = version
        self.model = self.__load_sklearn_model()



    def __load_sklearn_model(self):
        """"
        Load sklearn model from path
        """
        # Load the model from the file
        with open(self.path, 'rb') as file:
            model = pickle.load(file)
         
        return model
    
    

    def predict(self, data: dict) -> np.ndarray:
        """
        Predict data using model
        """
        # make the data a pandas DataFrame
        data_df = pd.DataFrame(data)
        
        # Make prediction
        y_pred = self.model.predict(data_df)
        
        return y_pred
        
model_path = os.getenv('MODEL_PATH')

model_loader = ModelLoader(
        path=model_path,
        name='toronto_rental_price', 
        version=1.0, 

)
