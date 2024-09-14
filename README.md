# ScalesimExecutionAnalysis
Analisi dei tempi di esecuzioni di vari modelli di reti IA con il simulatore ScaleSim nella sua versione 1 (unito a DRAMA) e alla sua versione 2


USAGE

py models_simulation_ss <SCALESIM_VERSION> <MODELS_FOLDER> <CFG_PATH>

CHANGES

In DRAMA_ScaleSim/Scale.py from 16 to 20 and from 92 to 99
Deleted Flags machanism

NOTE

- results is the result folder where we can find csv files with the execution time
- To recreate graphs we can use result_analysis.py
- to reproduce the experiments change the scale.py file with my scale.py in DRAMA_ScaleSim/
