from numpy import genfromtxt
import imageio

record_name = "type_S"

# Reading all record names from the file.
# with open(record_names) as file:
#     for line in file:
#         record_name = str(line.strip())
#         data_array = genfromtxt("csv_files/" + record_name + ".csv", delimiter=";")
#         imageio.imwrite("images_from_csv/" + record_name + ".jpg", data_array)
#         print(f"Create image from csv file: {record_name}.jpg")

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


data_array = genfromtxt("csv_type_files/" + record_name + ".csv", delimiter=";")
figure(num=None, figsize=(8, 6), dpi=100)
fig = plt.plot(data_array[0])
plt.axis("off")
plt.axis("tight")

# plt.axis("image")
plt.show()
# plt.savefig(
#     "output.png",
#     # dpi=None,
#     # facecolor="w",
#     # edgecolor="w",
#     orientation="portrait",
#     format="png",
#     # transparent=True,
#     # bbox_inches=0,
#     # pad_inches=0,
#     # frameon=False,
# )
