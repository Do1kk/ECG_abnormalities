import split_folders
import shutil
import os
import csv

input_folder = "images/"
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

# Ustawione by nie wykonywać tego co w if gdy wczytuje zmienne.
if __name__ == "__main__":
    # Przed podzieleniem przenieść zdjęcia z type_F które będą tylko w test set.
    #######################
    test_im_type_F = "test_type_F/"
    im_type_F = "images/type_F/"
    type_F = "csv_type_files/type_F.csv"

    # Pobranie długości całego pliku.
    with open(type_F, "r", newline="") as f:
        length = len(
            list(csv.reader(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL))
        )

    files = [f for f in sorted(os.listdir(im_type_F)) if f[-5:] == "F.png"]
    print(files[:10])
    # im_test_set = data[: int(test_ratio * length)]

    ################################
    # split_folders.ratio(
    #     input_folder,
    #     output="train_val_test",
    #     seed=43,
    #     ratio=(train_ratio, val_ratio, test_ratio),
    # )

# Po podzieleniu przenieść zdjęcia z type_F które są w test set, dzieląc je na
# train i val a te nie zmienione przed podzieleniem przenieść do test set.
