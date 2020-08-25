import split_folders
import shutil
import os
import csv
import shutil
from csv_ann_type import csv_folder


def files_move(files, dir_from, dir_to):
    for name in files:
        shutil.move(dir_from + name, dir_to + name)
    print(f"Moved {len(files)} files from directory: {dir_from} to: {dir_to}.")


train_ratio = 0.6
val_ratio = 0.2
test_ratio = 0.2
input_folder = "images/"
output_folder = "train_val_test"
test_im_group_F = "test_group_F/"
im_group_F = input_folder + "group_F/"
type_F = csv_folder + "type_F.csv"
test_split_group_F = output_folder + "/test/group_F/"
train_split_group_F = output_folder + "/train/group_F/"
val_split_group_F = output_folder + "/val/group_F/"


if __name__ == "__main__":
    # Delete folder if it already exists.
    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    # Create folder if it doesn't exist.
    if not os.path.isdir(test_im_group_F):
        os.makedirs(test_im_group_F)
    # Getting the number of vectors of the whole file.
    with open(type_F, "r", newline="") as f:
        length = len(
            list(csv.reader(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL))
        )
    # Before splitting, transfer photos from group_F which will only be in the test set.
    length = int(test_ratio * length)  # Number of test files.
    test_files = [
        f for f in os.listdir(im_group_F) if f[-8:-5] != "mod" and int(f[:-5]) < length
    ]
    files_move(test_files, im_group_F, test_im_group_F)
    # The division of data into three sets: training, validation and test.
    split_folders.ratio(
        input_folder,
        output=output_folder,
        seed=43,
        ratio=(train_ratio, val_ratio, test_ratio),
    )
    # After splitting, transfer and dividing photos from group_F test set to train and val.
    files = [f for f in os.listdir(test_split_group_F)]
    split_val = int(len(files) * val_ratio / train_ratio)
    train_files = files[split_val:]
    val_files = files[:split_val]
    files_move(train_files, test_split_group_F, train_split_group_F)
    files_move(val_files, test_split_group_F, val_split_group_F)
    # Copy photos back to original directory.
    for name in test_files:
        shutil.copy(test_im_group_F + name, im_group_F + name)
    # Transfer not modified photos to the test set.
    files_move(test_files, test_im_group_F, test_split_group_F)
    # Delete folder temporary exists.
    if os.path.isdir(test_im_group_F):
        shutil.rmtree(test_im_group_F)
