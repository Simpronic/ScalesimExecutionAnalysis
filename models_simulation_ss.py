import sys
import os
import shutil
import time
import pandas as pd 
from simulationTopologyData import simulation_topologyDta
from scaleSimV2.scalesim.scale_sim import scalesim
from DRAMA_ScaleSim.scale import scale

# SS1 -> ScaleSim 1 (+drama)
# SS2 -> Scalesim 2
def deleteAllCSV(folder,exlusion_list):
   files = os.listdir(folder)
   for file in files:
      if file.endswith(".csv") and file not in exlusion_list:
         path = os.path.join(folder,file)
         try:
            os.remove(path)
         except Exception as e:
            print(e)

def getLayerNumber(file):
    df = pd.read_csv(file)
    return len(df)
def writeDataOnCSV(data,r_file):
    lista = [obj.to_dict() for obj in data]
    df = pd.DataFrame(lista)
    df.to_csv(r_file,index=False)

def startSimulation_SS2(cfg_path,topologyFolder,result_file):
    files = [file for file in os.listdir(topologyFolder) if file.endswith('.csv')]
    n_iteration = len(files)
    data_array = []
    if(n_iteration < 0):
       print("Error, no file in folder....")
       exit()
    for i in range(0,n_iteration):
       s = scalesim(save_disk_space=False, verbose=True, config=cfg_path,topology=topologyFolder+'\\'+files[0])
       top_module_name = "test_run"+str(i)
       topologyFileRun = files[i] 
       layers = getLayerNumber(topologyFolder+'\\'+topologyFileRun)
       data_array.append(simulation_topologyDta(name = files[i].split('.')[0],n_layer= layers,execution_time=0))
       s.set_params(config_filename=cfg_path,topology_filename=topologyFolder+'\\'+topologyFileRun)
       start_time = time.time()
       s.run_scale(top_path=top_module_name)
       end_time = time.time()
       if os.path.exists(top_module_name): 
        shutil.rmtree(top_module_name)
       data_array[i].setExecTime(end_time-start_time)
       del s
    writeDataOnCSV(data_array,result_file+"_SS2.csv")
          


def startSimulation_SS1(cfg_path,topologyFolder,result_file):
    files = [file for file in os.listdir(topologyFolder) if file.endswith('.csv')]
    n_iteration = len(files)
    data_array = []
    if(n_iteration < 0):
       print("Error, no file in folder....")
       exit()
    for i in range(0,n_iteration):
       s = scale(save = False, sweep = False)
       topologyFileRun = files[i] 
       s.setFlagsByFunc(cfg_path,topologyFolder+'\\'+topologyFileRun)
       layers = getLayerNumber(topologyFolder+'\\'+topologyFileRun)
       data_array.append(simulation_topologyDta(name = files[i].split('.')[0],n_layer= layers,execution_time=0))
       start_time = time.time()
       s.run_scaleForMisuration()
       end_time = time.time()
       data_array[i].setExecTime(end_time-start_time)
       deleteAllCSV("Models",files)
       del s
    writeDataOnCSV(data_array,result_file+"_SS1.csv")

if __name__ == "__main__":
    if(len(sys.argv)-1 < 2): 
        print("HELP: type python model_simulation val1 val2")
        exit()
    ss_version = sys.argv[1]
    topology_f = sys.argv[2]
    if(ss_version == 'SS1'):
     startSimulation_SS1("cfg/ss1/scale_config_64x64_os.cfg",topology_f,"exec_time")
    elif(ss_version == 'SS2'):
     startSimulation_SS2("cfg/ss2/scale_config_64x64_os.cfg",topology_f,"exec_time")