import pickle

def predict(data):
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    
    data = data[['temperature', 'relative_humidity', 'is_day', 'surface_pressure',
       'snowfall', 'cloud_cover', 'wind_speed', 'wind_direction', 'day',
       'hour']]
    predictions = model.predict(data)
    return predictions
