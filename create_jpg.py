from numpy import genfromtxt
import imageio

file_name = 100
data_array = genfromtxt("csv_files/" + str(file_name) + ".csv", delimiter=";")
imageio.imwrite("images_from_csv/outfile.jpg", data_array)
