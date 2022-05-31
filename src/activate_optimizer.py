import os.path
import time
from urllib import response
import pandas as pd
import numpy as np

# Shared dropbox folder
file_path = 'C:\\Users\\kvriz\\Desktop\\Leeds\\scripts\\test_folder\\' 

# Propose initial parameters and upload to shared folder the 1_params.csv file
pump_rate = [20000, 25000, 30000, 35000, 40000]
temperature=[240, 250, 260]

def param_generator(response_dataset):
    df = pd.DataFrame([[np.random.choice(pump_rate), np.random.choice(pump_rate),
    np.random.choice(pump_rate), np.random.choice(temperature)]],
                   columns=['pump_rate_A', 'pump_rate_B', 'pump_rate_C', 'temperature'])
    return df

experiment_counter = 0
while True:
    experiment_counter += 1
    while not os.path.exists(f'{file_path}\\{experiment_counter}_response.csv'):
        time.sleep(10)

    response_dataset = pd.read_csv(f'{file_path}\\{experiment_counter}_response.csv')
    
    if os.path.exists(f'{file_path}\\success.csv'):
        print('Optimization successfully terminated with a conversion > 0.8')
        break
    
    print('Response file was detected:', f'{file_path}\\{experiment_counter}_response.csv')
    # update acquisition function and generate params_dataset
    # here using a random params generator
    params_dataset = param_generator(response_dataset)
    print(f'New parameters file {experiment_counter+1} is generated')
    #print('Time: ', params_dataset.time.values,  'Temperature: ', params_dataset.temperature.values )
    params_dataset.to_csv(f'{file_path}\\{experiment_counter+1}_params.csv', index=None)

