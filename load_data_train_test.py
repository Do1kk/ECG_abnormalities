import numpy as np
import imageio
from numpy import savez_compressed


num_per_type = 2540
numpy_file_dir = "NN_files/"
images_f = "images/"
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
beat_ann_value = (0, 1, 2, 3, 4, 5)
beat_ann_y = dict(zip(beat_ann_file, beat_ann_value))

X_train_test = np.array(np.empty((0, 220, 220, 3), dtype="uint8"))
y_train_test = np.array(np.empty((0,), dtype="uint8"))
for k, v in beat_ann_y.items():
    image_f_name = "type_" + k + "/"
    print(image_f_name)
    for num in range(num_per_type):
        im = imageio.imread(images_f + image_f_name + str(num) + ".png")[:, :, :3]
        X_train_test = np.append(X_train_test, [im], axis=0)
        y_train_test = np.append(
            y_train_test, v
        )  # bardzo mało optymalne, pewnie dobrze by było to o jeden poziom niżej dać i zapisywać ciąg liczb dla każdego typu

        if num % 100 == 99:
            print(X_train_test.shape)
            # Rozmiar zajmowany przez zmienną.
            print(
                "%d megabytes" % (X_train_test.size * X_train_test.itemsize / 1048000)
            )

# save to npy file # dane są dopisywane jak pliki już istnieją
savez_compressed(numpy_file_dir + "X_train_test.npz", X_train_test)
savez_compressed(numpy_file_dir + "y_train_test.npz", y_train_test)
