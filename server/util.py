import json
import pickle
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import numpy as np

# Initialize global variables
__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)


def load_saved_artifacts():
    """Loads the saved model and data columns from artifacts."""
    print("Loading the saved artifacts...start")
    global __data_columns
    global __locations

    # Load data columns
    with open("./artifacts/columns.json", 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # Extract location names

    # Load the model
    global __model
    with open("./artifacts/bangalore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)
    
    print("Loading saved artifacts...done")

def get_location_names():
    """Returns the list of location names."""
    return __locations

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Naar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
    print(get_estimated_price('Ejipura', 1000, 2, 2))
