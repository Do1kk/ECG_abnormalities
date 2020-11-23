import tkinter as tk
import os


def handle_click1(event):
    os.system("python csv_ann_type.py")
    print("Zrobione!!!")


def handle_click2(event):
    os.system("python mod_csv_ann.py")
    print("Zrobione!!!")


def handle_click3(event):
    os.system("python png_spec.py")
    print("Zrobione!!!")


def handle_click4(event):
    os.system("python image_split.py")
    print("Zrobione!!!")


window = tk.Tk()
window.title("Kolejne kroki przetwarzania")
label = tk.Label(
    text="Kolejne kroki przetwarzania prowadzące do powstania zdjęć zasilających klasyfikator. \n\nNaciśnij tylko raz!!!",
    width=90,
    height=4,
)
label.pack()

frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=5)
frame.pack()
button1 = tk.Button(
    master=frame,
    text="Podział przebiegów na przedziały",
    width=35,
    height=5,
    bg="green",
    fg="yellow",
)
button1.bind("<Button-1>", handle_click1)
button1.pack()

button2 = tk.Button(
    master=frame,
    text="Powielenie przez modyfikację",
    width=35,
    height=5,
    bg="green",
    fg="yellow",
)
button2.bind("<Button-1>", handle_click2)
button2.pack()

button3 = tk.Button(
    master=frame,
    text="Ekstrakcja i zapis końcowych zdjęć",
    width=35,
    height=5,
    bg="green",
    fg="yellow",
)
button3.bind("<Button-1>", handle_click3)
button3.pack()

button4 = tk.Button(
    master=frame,
    text="Podział zjęć na zbiory",
    width=35,
    height=5,
    bg="green",
    fg="yellow",
)
button4.bind("<Button-1>", handle_click4)
button4.pack()

window.mainloop()
