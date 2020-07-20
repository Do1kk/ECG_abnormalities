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
    for name in files:
        shutil.move(im_type_F + name, test_im_type_F + name)
    print(f"Przeniesiono {len(files)} plików.")

    split_folders.ratio(
        input_folder,
        output="train_val_test",
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
    for name in train_files:
        shutil.move(test_split_type_F + name, train_split_type_F + name)
    for name in val_files:
        shutil.move(test_split_type_F + name, val_split_type_F + name)
    print(f"Przeniesiono {len(train_files)} plików do type_F/train.")
    print(f"Przeniesiono {len(val_files)} plików do type_F/val.")

    # A te nie zmienione przed podzieleniem przenieść do test set.
    files = [f for f in os.listdir(test_im_type_F)]
    for name in files:
        shutil.move(test_im_type_F + name, test_split_type_F + name)
    print(f"Przeniesiono {len(files)} plików.")
