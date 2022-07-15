# read the config file and start the experiment
# depending on the settings call the relevant functions
from lab import *
import json
from uv_vis.save_spectra import *
#from uv_vis.get_responses import *

#pumpA=COM6
# Opening JSON file
f = open('qd_lab/config.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

for i in data['equipment']:
    pump_name = (i['pump_name'])
    com_B = (i['com_channel'])

for i in data['parameters']:
    flow_rate_B = i['flow_rate_pump_A']['values']


def start_closed_loop():
    print('start')
    
    # Shared dropbox folder where the files will be exchanged
    file_path = 'C:/Users/kvriz/Dropbox/Leeds_Sheffield/food_dye' 
    experiment_counter = 0
    
    
    # Start recording the temperature
    #printit()

    while True:
        experiment_counter += 1  
        while not os.path.exists(f'{file_path}/{experiment_counter}_param.csv'):
            time.sleep(5)             
    
        params_dataset = pd.read_csv(f'{file_path}/{experiment_counter}_param.csv')
        #print(params_dataset.pump_rate_A)
        flow_rate_A = params_dataset.pump_rate_A.values[0]
        flow_rate_B = params_dataset.pump_rate_B.values[0]
        flow_rates = flow_rate_A + flow_rate_B
        sampling_time = 1/(flow_rate_A + flow_rate_B)
        #temperature = int(params_dataset.temperature.values[0])
    
        # this command will start the experiment with the given conditions
        start_experiment(pump_rate_A=flow_rate_A, pump_rate_B=flow_rate_B, pump_rate_C=None, temperature=None, sampling_time=2*sampling_time, com_A='COM8', com_B='COM5')
    
        # this command will save the absorption spectra in the data file 
        response_dataset = get_absorption() # response_generator(params_dataset)
        response_dataset.to_csv(f'{file_path}/{experiment_counter}_spectra.csv', index=None)
        max_red = response_dataset.intensities.values[472:817].max()
        #print(max_red)
        max_blue = response_dataset.intensities.values[935:1700].max()
        #print(max_blue)
        diff = abs(max_red -max_blue)
        params_dataset['abs'] = diff
        params_dataset.to_csv(f'{file_path}/{experiment_counter}_response.csv', index=None)

        #if experiment_counter >= 3:
        #    print('Process finished after 3 iterations!')
        #    try:
        #        start_experiment(pump_rate_A=0, pump_rate_B=0, pump_rate_C=None, temperature=None, sampling_time=2*sampling_time, com_A='COM8', com_B='COM5')
        #    except:
        #        pass

start_closed_loop()