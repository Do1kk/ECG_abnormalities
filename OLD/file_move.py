"""
Przenosi nadmiar zdjęć grupy N, zostawiając tylko 9k zdjęć (po 3k z każdego typu 
należącego do tej grupy).
"""
import random
import shutil
import os
from image_split import files_move

root = "images/type_N/"
destination = "rejected_type_N/"
num_per_type = 4000

if __name__ == "__main__":
    files = [f for f in sorted(os.listdir(root))]

    files_type_N = [file_name for file_name in files if file_name[-5] == "N"]
    files_type_L = [file_name for file_name in files if file_name[-5] == "L"]
    files_type_R = [file_name for file_name in files if file_name[-5] == "R"]
    random.shuffle(files_type_N)
    random.shuffle(files_type_L)
    random.shuffle(files_type_R)

    files_after = [
        files_type_N[num_per_type:],
        files_type_L[num_per_type:],
        files_type_R[num_per_type:],
    ]
    for type_x in files_after:
        files_move(type_x, root, destination)

    check_after = [f for f in sorted(os.listdir(root))]
    num_type_N = len([file_name for file_name in check_after if file_name[-5] == "N"])
    num_type_L = len([file_name for file_name in check_after if file_name[-5] == "L"])
    num_type_R = len([file_name for file_name in check_after if file_name[-5] == "R"])

    print(f"Zostało {num_type_N} type_N, {num_type_L} type_L i {num_type_R} type_R.")
