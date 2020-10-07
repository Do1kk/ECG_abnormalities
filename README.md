# Opis projektu
Metoda klasyfikacji cykli pracy serca wykorzystująca spektrogram wielosygnałowego zapisu EKG oraz sieci konwolucyjne z blokami rezydualnymi

Wykorzystanie bazy przebiegów arytmii MIT-BIH.

TensorFlow + Keras

# Kolejność uruchamiania
Zainstalować niezbędne biblioteki z requirements.txt
Wystarczy użyć "make".
    1. csv_ann_type.py
    2. mod_csv_ann.py
    3. png_spec.py 
    4. image_split.py
5. wstawienie spakowanych zdjęć (.zip) na "Google Drive"
6. podłączenie dysku w "Colab" i uruchomienie najnowszego Jupyter Notebook z folderu /classification

# Wyniki
Tabela 1. Wyniki dotyczą prac, które implementują grupowanie AMII oraz wykorzystują wyłącznie bazę danych arytmii MIT-BIH.
![Alt text](results/wyniki.png?raw=true "wyniki.png")

[13] S. Chen, W. Hua, Z. Li, J. Li and X. Gao, “Heartbeat classification using projected and dynamic features of ECG signal,” Biomedical Signal Processing and Control, pp. 165-173, 2017.

[18] S. Mousavi, F. Afghah, F. Khadem and U. R. Acharya, “ECG Language Processing (ELP): a New Technique to Analyze ECG Signals,” 13 Czerwiec 2020.

[20] C. Ye, B. V. K. V. Kumar and M. T. Coimbra, “Heartbeat classification using morphological and dynamic features of ECG signals,” IEEE Transactions on Biomedical Engineering, vol. 59, no. 10, pp. 2930-2941, 2012.

[22] P. de Chazal, M. O'Dwyer and R. B. Railly, “Automatic classification of heartbeats using ECG morphology and heartbeat interval features,” IEEE Transactions on Biomedical Engineering, pp. 1196-1206, Lipiec 2004.

[37] Z. Zhang, J. Dong, X. Luo, K.-S. Choi and X. Wu, “Heartbeat classification using disease-specific feature selection,” Computers in Biology and Medicine, pp. 79-89, 1 Marzec 2014.

[38] T. Ince, S. Kiranyaz, L. Eren, M. Askar and M. Gabbouj, “Real-Time Motor Fault Detection by 1-D Convolutional Neural Networks,” IEEE Transactions on Industrial Electronics, pp. 7067 - 7075, 28 Maj 2016.

[39] Y. Xia, N. Wulan, K. Wang and H. Zhang, “Detecting atrial fibrillation by deep convolutional neural networks,” Computers in biology and medicine,, pp. 84-92, 2018.

[40] S. M. Mathews, C. Kambhamettu and K. E. Barner, “A novel application of deep learning for single-lead ECG classification,” Computers in Biology and Medicine, pp. 53-62, 2018.

[41] K. N. V. P. S. Rajesh and R. Dhuli, “Classification of imbalanced ECG beats using re-sampling techniques and AdaBoost ensemble classifier,” Biomedical Signal Processing and Control, p. 242–254, 2018.

Trochę lepsze wyniki niż przedstawione w tabeli można uzyskać dzięki zastosowaniu transformaty falkowej podczas ekstrakcji cech. Wykorzystanie jednak tego kroku wydłuża w znacznym stopniu czas przetwarzania danych. Metoda ta została zaimplementowana jako funkcja "save_image2" w pliku "png_spec.py".

# Opis programów

### /

csv_ann_type.py - wyszukiwanie wzniesień w plikach testowych bazy mit-bih wykorzystując adnotacje, 
zapisanie pliku grupując po typach arytmii, nie ma tu odrzucania plików z małą ilością danych;

mod_csv_ann.py - korzysta na zrobionym wcześniej pliku csv wycinków sygnału, by przetworzyć sygnał
i stworzyć nowe wycinki, stworzony w celu zwiększenia ilości zdjęć spektrogramów typu_F i grupy_F;

png_spec.py - tworzenie spektrogramów i zapisywanie ich jako zdjęcia o rozmiarach 220 x 220 RGB, 
robione jest to tylko dla wygranych (z dużą ilością przedziałów) typów bicia serca;

image_split.py - pozwala na podzielenie zdjęć na sety (train/dev/test) do późniejszego trenowania sieci 
neuronowej;

### OLD/

macierz_pomylek.py - Macierz pomyłek, ale z możliwością ustawienia zakresu koloru, przydatne gdy 
liczba danych w konkretnych klasach jest zróżnicowana;

file_move.py - Przenosi nadmiar zdjęć grupy N, zostawiając tylko 9k zdjęć (po 3k z każdego typu 
należącego do tej grupy);

sig_display.py - wyświetlenie subplotów na potrzeby pokazania i zobaczenia jak to wygląda, 
zdjęcia spektrogramów oraz nieprzetworzone przebiegi po wycięciu przedziałów;

load_data_train_test.py - tworzenie plików z powstałych wcześniej zdjęć spektrogramów: X_train_test.npz 
i y_train_test.npz, są to pliki skompresowane NumPy, pozwalają znacząco zmniejszyć rozmiar danych 
i nie ma już problemów z dużą ilością zdjęć oraz ich rozmiarem, w jednym pliku są dane treningowe i testowe;

create_csv_pat.py - wyszukiwanie wzniesień używając biblioteki WFDB bez uwzględnienia adnotacji;

create_csv_ann_pat.py - wyszukiwanie wzniesień w plikach testowych bazy mit-bih wykorzystując adnotacje, 
zapisanie pliku grupując po pacjentach;

create_jpg.py - zapisywanie stworzonych plików .CSV w formie zdjęcia, by sprawdzić na szybko poprawność wyszukania wzniesień;

OLD_create_png_spectrogram.py - przykładowe tworzenie spektrogramu używając biblioteki "signal";

load_data.py - tworzenie plików z powstałych wcześniej zdjęć spektrogramów: X_train.npz, y_train.npz, 
X_test.npz, y_test.npz są to pliki skompresowane NumPy, pozwalają znacząco zmniejszyć rozmiar danych 
i nie ma już problemów z dużą ilością zdjęć oraz ich rozmiarem;