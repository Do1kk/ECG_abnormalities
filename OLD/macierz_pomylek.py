"""
Macierz pomyłek ale z możliwością ustawienia zakresu koloru, przydatne gdy 
liczba danych w konkretnych klasach jest zróżnicowana.
"""

import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

array = [
    [151, 44, 0, 0, 5],
    [4, 17828, 9, 52, 41],
    [0, 0, 1597, 0, 0],
    [0, 176, 0, 549, 1],
    [5, 14, 1, 5, 1401],
]
target_names = ["klasa F", "klasa N", "klasa Q", "klasa S", "klasa V"]

df_cm = pd.DataFrame(array, index=target_names, columns=target_names,)
plt.figure(figsize=(10, 7))

sn.heatmap(df_cm, annot=True, cmap="Greens_r", vmax=160, fmt="d")
plt.xlabel("Klasa predykowana")
plt.ylabel("Klasa rzeczywista")
plt.show()

