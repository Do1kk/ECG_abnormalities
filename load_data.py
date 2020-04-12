import numpy as np
import imageio
from numpy import savez_compressed


train = 50
test = 10
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
images_f = "images/"

X_train = np.array(np.empty((0, 512, 512, 3), dtype="uint8"))
y_train = np.array(np.empty((0,), dtype="uint8"))
X_test = np.array(np.empty((0, 512, 512, 3), dtype="uint8"))
y_test = np.array(np.empty((0,), dtype="uint8"))

for k, v in beat_ann_y.items():
    image_f_name = "type_" + k + "/"
    print(image_f_name)
    for num in range(train):
        im = imageio.imread(images_f + image_f_name + str(num) + ".png")[:, :, :3]
        X_train = np.append(X_train, [im], axis=0)
        y_train = np.append(y_train, v)

        if num == train - 1:
            for num_test in range(train, train + test):
                im_test = imageio.imread(
                    images_f + image_f_name + str(num_test) + ".png"
                )[:, :, :3]
                X_test = np.append(X_test, [im_test], axis=0)
                y_test = np.append(y_test, v)

        if num % 100 == 99:
            print(X_train.shape)
            # Rozmiar zajmowany przez zmienną.
            print("%d megabytes" % (X_train.size * X_train.itemsize / 1048000))

# save to npy file
savez_compressed(numpy_file_dir + "X_train.npz", X_train)
savez_compressed(numpy_file_dir + "y_train.npz", y_train)

savez_compressed(numpy_file_dir + "X_test.npz", X_test)
savez_compressed(numpy_file_dir + "y_test.npz", y_test)
