# read the config file and start the experiment
# depending on the settings call the relevant functions
from lab import *
import json
from uv_vis.save_spectra import *
from uv_vis.get_responses import *


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

def start_closed_loop(experiment_counter):
    # this command will start the experiment with the given conditions
    start_experiment(pump_rate_A=None, pump_rate_B=flow_rate_B, pump_rate_C=None, temperature=None, sampling_time=10, com_A=None, com_B=com_B)
    
    # this command will save the absorption spectra in the data file 
    get_absorption(experiment_counter)

    # this command will save the emission spectra in the data file 
    get_emmision(experiment_counter)
    
    # this command will save the desired responces in a csv file
    #abs_max_intensity(dataset, range)


# Shared dropbox folder
#file_path = 'onedrive_folder' 

#experiment_counter = 0

# Start recording the temperature
#printit()

#while True:
#    experiment_counter += 1    
#    while not os.path.exists(f'{file_path}\\{experiment_counter}_params.csv'):
#        time.sleep(5)             
    
#    params_dataset = pd.read_csv(f'{file_path}\\{experiment_counter}_params.csv')
#    pump_rate_A = params_dataset.pump_rate_A.values[0]
#    pump_rate_B = params_dataset.pump_rate_B.values[0]
#    pump_rate_C = params_dataset.pump_rate_C.values[0]
#    temperature = int(params_dataset.temperature.values[0])
    
#    start_experiment(pump_rate_A=pump_rate_A, pump_rate_B=pump_rate_B, pump_rate_C=pump_rate_C, temperature=temperature)
    
#    response_dataset = response_generator(params_dataset)
#    response_dataset.to_csv(f'{file_path}\\{experiment_counter}_response.csv', index=None)

#    if experiment_counter >= 3:
#        print('Process finished after 3 iterations!')
#        try:
#            stop_milligat_A()
#            stop_milligat_B()
#            stop_milligat_C()
#        except:
#            break