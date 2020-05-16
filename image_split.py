import split_folders

input_folder = "images/"

# split_folders.ratio(
#     input_folder, output=input_folder + "train_val_test", seed=1, ratio=(0.8, 0.1, 0.1)
# )

# Split val/test with a fixed number of items e.g. 100 for each set.
# oversample <- można użyć gdy dane nie są zrównoważone
split_folders.fixed(
    input_folder,
    output=input_folder + "train_val_test",
    seed=1,
    fixed=(150, 100),
    oversample=True,
)
