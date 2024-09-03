class simulation_topologyDta:
    def __init__(self,name,n_layer,execution_time):
      self.name = name
      self.n_layer = n_layer
      self.execution_time = execution_time

    def setExecTime(self,execTime):
      self.execution_time = execTime 
    
    def to_dict(self):
       return{
          'nome':self.name,
          'numero di livelli':self.n_layer,
          'tempo di esecuzione':self.execution_time
       }