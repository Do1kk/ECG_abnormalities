from tkinter import *
from tkinter import ttk
from wfdb import rdrecord, rdann, plot_wfdb


def wyswietl_przebiegi(*args):
    try:
        folder = "mit-bih/"
        nazwa_pliku_str = nazwa_pliku.get()
        path = folder + nazwa_pliku_str
        pocz = int(przedzial_pocz.get())
        kon = int(przedzial_kon.get())
        record = rdrecord(path, smooth_frames=True, sampfrom=pocz, sampto=kon,)
        # Jest problem z adnotacją gdy nie wczyta się jej od początku.
        annotation = rdann(path, "atr", sampfrom=pocz, sampto=kon)
        plot_wfdb(
            record=record,
            annotation=annotation,
            plot_sym=True,
            time_units="seconds",
            title="MIT-BIH Record " + nazwa_pliku_str,
            figsize=(8, 6),
        )
    except ValueError:
        pass


root = Tk()
root.title("Wczytanie rekordu")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# Jeśli jest taka potrzeba, rozszerz pole.
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

nazwa_pliku = StringVar()
przedzial_pocz = StringVar()
przedzial_kon = StringVar()

name_entry = ttk.Entry(mainframe, width=10, textvariable=nazwa_pliku)
name_entry.grid(column=2, row=1, sticky=(W, E))
pocz_entry = ttk.Entry(mainframe, width=10, textvariable=przedzial_pocz)
pocz_entry.grid(column=2, row=2, sticky=(W, E))
kon_entry = ttk.Entry(mainframe, width=10, textvariable=przedzial_kon)
kon_entry.grid(column=3, row=2, sticky=(W, E))

# ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Wczytaj", command=wyswietl_przebiegi).grid(
    column=3, row=3, sticky=W
)

ttk.Label(mainframe, text=".*").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Nazwa pliku").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Przedział przebiegów").grid(column=1, row=2, sticky=E)

# Małe odstępy między wigetami.
for child in mainframe.winfo_children():
    child.grid_configure(padx=15, pady=10)

# Ustawienie kursora w polu do wpisania.
name_entry.focus()
# Wciśnięcie przycisku również przy pomocy "enter".
root.bind("<Return>", wyswietl_przebiegi)

# Automatyczna aktualizacja wyniku.
root.mainloop()
