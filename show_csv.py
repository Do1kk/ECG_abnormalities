# Sprawdzenie czy dobrze wyszukuje wzniesienia.
from numpy import genfromtxt
import imageio

my_data = genfromtxt("pliki_csv/108.csv", delimiter=";")
imageio.imwrite("obraz_csv/outfile.jpg", my_data)
