import split_folders

input_folder = "images/"

split_folders.ratio(
    input_folder,
    output=input_folder + "train_val_test",
    seed=43,
    ratio=(0.7, 0.15, 0.15),
)

# Split val/test with a fixed number of items e.g. 100 for each set.
# oversample <- można użyć gdy dane nie są zrównoważone
# split_folders.fixed(
#     input_folder,
#     output=input_folder + "train_val_test",
#     seed=43,
#     fixed=(400, 400),
#     oversample=False,
# )
