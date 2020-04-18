from numpy import genfromtxt
import matplotlib.pyplot as plt
import imageio


beat_ann = (
    "N",  # Normal beat.
    "L",  # Left bundle branch block beat.
    "R",  # Right bundle branch block beat.
    "A",  # Atrial premature beat.
    "V",  # Premature ventricular contraction.
    "/",  # Paced beat.
)
beat_ann_file = ("N", "L", "R", "A", "V", "Pe")
beat_ann = dict(zip(beat_ann, beat_ann_file))
record_name = "type_"
images_f = "images/"
how_many = 10


fig, axs = plt.subplots(2, 6, figsize=(14, 5), constrained_layout=True)
axs[0, 0].set_ylabel("10 przykładowych przebiegów")
for index, name in enumerate(beat_ann_file):
    all_data = genfromtxt(
        "csv_type_files/" + record_name + name + ".csv", delimiter=";", max_rows=100
    )
    some_data = all_data[:how_many]
    image_f_name = "type_" + name + "/"
    im = imageio.imread(images_f + image_f_name + "0.png")[:, :, :3]
    axs[0, index].set_title(name)

    for i in range(how_many):
        axs[0, index].plot(some_data[i])
    axs[1, index].axis("off")
    axs[1, index].set_title("przykł. spektrogram")
    axs[1, index].imshow(im)
plt.show()
