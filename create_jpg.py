from numpy import genfromtxt
import imageio

record_names = "mit-bih/RECORDS"

# Reading all record names from the file.
with open(record_names) as file:
    for line in file:
        record_name = str(line.strip())
        data_array = genfromtxt("csv_files/" + record_name + ".csv", delimiter=";")
        imageio.imwrite("images_from_csv/" + record_name + ".jpg", data_array)
        print(f"Create image from csv file: {record_name}.jpg")
