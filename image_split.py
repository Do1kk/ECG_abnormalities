import split_folders

input_folder = "images/"
split_folders.ratio(
    input_folder, output=input_folder + "train_val_test", seed=1, ratio=(0.8, 0.1, 0.1)
)
