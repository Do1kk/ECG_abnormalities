import split_folders
import shutil
import os
import csv


def files_move(files, dir_from, dir_to):
    for name in files:
        shutil.move(dir_from + name, dir_to + name)
    print(
        f"Przeniesiono {len(files)} plików z katalogu: {dir_from} do katalogu: {dir_to}."
    )


input_folder = "images/"
output_folder = "train_val_test"
train_ratio = 0.6
val_ratio = 0.2
test_ratio = 0.2

# Ustawione by nie wykonywać tego co w if gdy wczytuje zmienne.
if __name__ == "__main__":
    # Przed podzieleniem przenieść zdjęcia z type_F które będą tylko w test set.
    test_im_type_F = "test_type_F/"
    im_type_F = "images/type_F/"
    type_F = "csv_type_files/type_F.csv"

    # Pobranie ilości przedziałów całego pliku.
    with open(type_F, "r", newline="") as f:
        length = len(
            list(csv.reader(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL))
        )
    # Ilość plików testowych.
    length = int(test_ratio * length)

    files = [
        f for f in os.listdir(im_type_F) if f[-8:-5] != "mod" and int(f[:-5]) < length
    ]
    files_move(files, im_type_F, test_im_type_F)

    split_folders.ratio(
        input_folder,
        output=output_folder,
        seed=43,
        ratio=(train_ratio, val_ratio, test_ratio),
    )

    # Po podzieleniu przenieść zdjęcia z type_F które są w test set, dzieląc je na train i val.
    test_split_type_F = "train_val_test/test/type_F/"
    train_split_type_F = "train_val_test/train/type_F/"
    val_split_type_F = "train_val_test/val/type_F/"
    files = [f for f in os.listdir(test_split_type_F)]
    split_val = int(len(files) * val_ratio / train_ratio)
    train_files = files[split_val:]
    val_files = files[:split_val]

    files_move(train_files, test_split_type_F, train_split_type_F)
    files_move(val_files, test_split_type_F, val_split_type_F)

    # A te nie zmienione przed podzieleniem przenieść do test set.
    files = [f for f in os.listdir(test_im_type_F)]
    files_move(files, test_im_type_F, test_split_type_F)
