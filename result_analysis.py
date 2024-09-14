# -*- coding: utf-8 -*-
"""result_analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/166_RC5sB8sa3pCyEUm_MIvDbYs2YoLiE

In questo colab plottiamo i dati relativi ai tempi di esecuzione di vari modelli testati con ScaleSim
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df1 = pd.read_csv('exec_time_SS1.csv').sort_values(by='numero di livelli')
df2 = pd.read_csv('exec_time_SS2.csv').sort_values(by='numero di livelli')

df2.head()

exec_time_log_1 = np.log(df1["tempo di esecuzione"])
exec_time_log_2 = np.log(df2["tempo di esecuzione"])

plt.bar(df1['nome'], exec_time_log_1, color='skyblue')
plt.yscale('log')
plt.xticks(rotation=45, ha='right')
plt.title("Tempi di Esecuzione per Modello in log-scale")
plt.xlabel("Model")
plt.ylabel("Tempo di Esecuzione (s)")

plt.show()

plt.bar(df2['nome'], exec_time_log_2, color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.yscale('log')
plt.title("Tempi di Esecuzione per Modello in log-scale")
plt.xlabel("Model")
plt.ylabel("Tempo di Esecuzione (s)")

plt.show()

plt.plot(df1['numero di livelli'][:-1], df1['tempo di esecuzione'][:-1], marker='o', linestyle='-', color='blue')
plt.plot(df2['numero di livelli'][:-1], df2['tempo di esecuzione'][:-1], marker='o', linestyle='-', color='red')

plt.title("Tempi di esecuzione in funzione del numero di livelli")
plt.xlabel("Livelli")
plt.ylabel("T_execuzione")

# Mostra il grafico
plt.show()

#np.log10()
max_f_weight_1 = df1["Grandezza massima file generato"]
max_f_weight_2 = df2["Grandezza massima file generato"]
avg_f_weight_1 = df1["Grandezza massima file generato"]
avg_f_weight_2 = df2["Grandezza massima file generato"]

n = len(df2['nome'])
ind = np.arange(n)
width = 0.35
fig, ax = plt.subplots()

plt.bar(df2['nome'], max_f_weight_1, color='skyblue')
bar1 = ax.bar(ind - width/2, avg_f_weight_1, width, label='ScaleSimV1', color='skyblue')

# Barre del secondo dataset
bar2 = ax.bar(ind + width/2, avg_f_weight_2, width, label='ScaleSimV2', color='lightgreen')

ax.set_xticks(ind)
ax.set_yscale('log')
ax.set_xticklabels(df2['nome'], rotation=45, ha='right')
plt.title("Grandezza massima file generato")
plt.xlabel("Model")
plt.ylabel("grandezza KB")

plt.legend()

plt.show()

n = len(df2['nome'])
ind = np.arange(n)
width = 0.35
fig, ax = plt.subplots()

plt.bar(df2['nome'], max_f_weight_1, color='skyblue')
bar1 = ax.bar(ind - width/2, max_f_weight_1, width, label='ScaleSimV1', color='skyblue')

# Barre del secondo dataset
bar2 = ax.bar(ind + width/2, max_f_weight_2, width, label='ScaleSimV2', color='lightgreen')

ax.set_xticks(ind)
ax.set_yscale('log')
ax.set_xticklabels(df2['nome'], rotation=45, ha='right')
plt.title("Grandezza massima file generato")
plt.xlabel("Model")
plt.ylabel("grandezza KB")

plt.legend()

plt.show()

"""Plotto l'andamento solo della grandezza media al variare dei livelli"""

plt.plot(df1['numero di livelli'][:-1], avg_f_weight_1[:-1], marker='o', linestyle='-', color='blue')
plt.plot(df2['numero di livelli'][:-1], avg_f_weight_2[:-1], marker='o', linestyle='-', color='red')

plt.title("Grandezza media file generati")
plt.xlabel("Livelli")
plt.ylabel("grandezza kb")

# Mostra il grafico
plt.show()