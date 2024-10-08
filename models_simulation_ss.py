import sys
import os
import shutil
import time
import pandas as pd 
from simulationTopologyData import simulation_topologyDta
from scaleSimV2.scalesim.scale_sim import scalesim
import configparser as cp
from DRAMA_ScaleSim.scale import scale

# SS1 -> ScaleSim 1 (+drama)
# SS2 -> Scalesim 2

def getRunName(cfg_file_path):
    config = cp.ConfigParser()
    config.read(cfg_file_path)
    return config.get("general", 'run_name')

def getMaxAndAvgFileWeight_SS1(folder,exlusion_list):
 max = -1
 sum = 0
 n_files = 0
 files = os.listdir(folder)
 for file in files:
   if file.endswith(".csv") and file not in exlusion_list:
         size = os.path.getsize(os.path.join(folder,file))
         sum += size
         n_files += 1
         if size > max:
            max = size
 return sum,n_files,sum/n_files,max,(n_files-5)/6

def getMaxAndAvgFileWeight_SS2(folder):
   layers_f= [nome for nome in os.listdir(folder) if os.path.isdir(os.path.join(folder,nome))]
   max_find = -1
   totalSum = 0
   total_n_file = 0
   for layer in layers_f:
       files = [file for file in os.listdir(folder+'\\'+layer)]
       max_f_w = max(os.path.getsize(folder+'\\'+layer+'\\'+file) for file in files )
       total_size = sum(os.path.getsize(folder+'\\'+layer+'\\'+file) for file in files )
       n_files = len(files)
       totalSum += total_size
       total_n_file += n_files
       if max_f_w > max_find:
          max_find = max_f_w
   print("Il numero totale di file generati sono: "+str(total_n_file))
   return totalSum,n_files,totalSum/total_n_file,max_find,total_n_file/6

def deleteAllCSV(folder,exlusion_list):
   files = os.listdir(folder)
   for file in files:
      if file.endswith(".csv") and file not in exlusion_list:
         path = os.path.join(folder,file)
         try:
            os.remove(path)
         except Exception as e:
            print(e)


def writeDataOnCSV(data,r_file):
    lista = [obj.to_dict() for obj in data]
    df = pd.DataFrame(lista)
    print(df)
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
       data_array.append(simulation_topologyDta(name = files[i].split('.')[0],n_layer= 0,execution_time=0,avg_file_weight=0,max_file_weight=0,weight=0,n_files=0))
       s.set_params(config_filename=cfg_path,topology_filename=topologyFolder+'\\'+topologyFileRun)
       start_time = time.time()
       s.run_scale(top_path=top_module_name)
       end_time = time.time()
       weight,number_of_files,avg_f_w,max_f_w,n_layers = getMaxAndAvgFileWeight_SS2(top_module_name+'\\'+getRunName(cfg_path))
       data_array[i].setAvgFweight(avg_f_w)
       data_array[i].setMaxFweight(max_f_w)
       data_array[i].setLayerNumbers(n_layers)
       data_array[i].setWeight(weight)
       data_array[i].setNumberOfFile(number_of_files)
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
       data_array.append(simulation_topologyDta(name = files[i].split('.')[0],n_layer= 0,execution_time=0,avg_file_weight=0,max_file_weight=0,weight=0,n_files=0))
       start_time = time.time()
       s.run_scaleForMisuration()
       end_time = time.time()
       data_array[i].setExecTime(end_time-start_time)
       weight,number_of_files,avg_f_w,max_f_w,n_layers =  getMaxAndAvgFileWeight_SS1("Models",files)
       data_array[i].setAvgFweight(avg_f_w)
       data_array[i].setMaxFweight(max_f_w)
       data_array[i].setLayerNumbers(n_layers)
       data_array[i].setWeight(weight)
       data_array[i].setNumberOfFile(number_of_files)
       deleteAllCSV("Models",files)
       del s
    writeDataOnCSV(data_array,result_file+"_SS1.csv")

if __name__ == "__main__":
    if(len(sys.argv)-1 < 3): 
        print("HELP: type python model_simulation val1 val2 val3")
        exit()
    ss_version = sys.argv[1]
    topology_f = sys.argv[2]
    cfg_path = sys.argv[3]
    if(ss_version == 'SS1'):
     startSimulation_SS1(cfg_path,topology_f,"exec_time")
    elif(ss_version == 'SS2'):
     startSimulation_SS2(cfg_path,topology_f,"exec_time")
