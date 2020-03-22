# Sprawdzenie czy dobrze wyszukuje wzniesienia.
from numpy import genfromtxt
import imageio

nazwa_pliku = 100
my_data = genfromtxt("pliki_csv/" + str(nazwa_pliku) + ".csv", delimiter=";")
imageio.imwrite("obraz_csv/outfile.jpg", my_data)
