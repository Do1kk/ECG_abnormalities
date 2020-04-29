# Opis projektu
Nowa metoda wykrywania nieprawidłowości w przebiegach EKG.

Wykożystanie bazy przebiegów arytmii MIT-BIH.

Celem pracy jest projekt i implementacja nowej metody wspomagającej diagnozowanie chorób serca na podstawie EKG. Metoda będzie używała nowatorskiego podejścia wykorzystującego głębokie sieci neuronowe. 

TensorFlow + Keras

# Opis programów

Starałem się używać języka angielskiego, komentarze, zmienne itp.

### folder główny

csv_ann_type.py - wyszukiwanie wzniesień w plikach testowych bazy mit-bih wykożystując adnotacje, 
zapisanie pliku grupując po typach arytmii, nie ma tu odrzucania plików z małą ilością danych;
png_spec.py - tworzenie spektrogramów i zapisywanie ich jako zdjęcia o rozmiarach 220x220 RGB, 
robione jest to tylko dla wygranych (z dużą ilością przedziałów) typów bicia serca;
load_data_train_test.py - tworzenie plików z powstałych wcześniej zdjęć spektrogramów: X_train_test.npz 
i y_train_test.npz, są to pliki zkompresowane numpy, pozwalają znacząco zmniejszyć rozmiar danych 
i nie ma już problemów z dużą ilością zdjęć oraz ich rozmiarem, w jednym pliku są dane treningowe i testowe;
sig_display.py - wyświetlenie subplotów na potrzeby pokazania i zobaczenia jak to wygląda, 
zdjęcia spektrogramów oraz nie przetworzone przebiegi po wycięciu przedziałów;

### OLD/
create_csv_pat.py - wyszukiwanie wzniesień używając biblioteki wfdb bez uwzględnienia adnotacji;
create_csv_ann_pat.py - wyszukiwanie wzniesień w plikach testowych bazy mit-bih wykożystując adnotacje, 
zapisanie pliku grupując po pacjentach;
create_jpg.py - zapisywanie stworzonych plików .CSV w formie zdjęcia by sprawdzić na szybko poprawność wyszukania wzniesień;
OLD_create_png_spectrogram.py - przykładowe tworzenie spektrogramu używając biblioteki "signal";
load_data.py - tworzenie plików z powstałych wcześniej zdjęć spektrogramów: X_train.npz, y_train.npz, 
X_test.npz, y_test.npz są to pliki zkompresowane numpy, pozwalają znacząco zmniejszyć rozmiar danych 
i nie ma już problemów z dużą ilością zdjęć oraz ich rozmiarem;