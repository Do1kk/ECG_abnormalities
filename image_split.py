import split_folders

input_folder = "images/"

# Przed podzieleniem przenieść zdjęcia z type_F które będą tylko w test set.

split_folders.ratio(
    input_folder, output="train_val_test", seed=43, ratio=(0.7, 0.15, 0.15),
)

# Po podzieleniu przenieść zdjęcia z type_F które są w test set, dzieląc je na
# train i val a te nie zmienione przed podzieleniem przenieść do test set.
