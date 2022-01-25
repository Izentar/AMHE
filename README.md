# AMHE

## Wymagania

1. Wymagany jest Python w wersji 3.
2. Do uruchomienia zautomatyzowanych testów niezbędna jest możliwość uruchomienia skryptu w języku `bash`
Na windowsie można to zrobić np. za pomocą:

- konsoli Ubuntu: https://ubuntu.com/tutorials/ubuntu-on-windows
- konsoli Git Bash (instalowanej wraz z klientem Gita): https://git-scm.com/download/win

## Instalacja

1. Należy zainstalować wymagane biblioteki za pomocą:

```sh
pip install -r requirements.txt
```

## Uruchamianie

### Pojedynczy test za pomocą Pythona

Pojedynczy test można uruchomić za pomocą polecenia:

```sh
python tests.py --sigma 0.3 --dim 10 --xstart gauss --xsgm 0 --xsgstd 1 --estart gauss --esgm 0 --esgstd 1 --xsumin 0 --xsumax 1 --esumin 0 --esumax 1 --esexpl 1 --xsexpl 1 -r 1 --testf elli -o test.csv
```

Wynikiem działania będzie plik `csv` o nazwie `out.csv`. Więcej informacji o argumentach można znaleźć pod `python test.py --help`.
Program z automatu dodaje kolejne wiersze w pliku wynikowym. Jeśli chcemy zresetować wyniki przed kolejnym uruchomieniem, należy wybrać inny plik wyjściowy lub usunąć istniejący.

### Zautomatyzowana seria testów

Serię testów wykonanych w ramach projektu można powtórzyć uruchamiając:

```sh
bash runTests.sh -r 20 -f elli,rosen,sphere,hyperelli,rastrigin,schwefel,bukin,schaffer -o out
```

Wynikiem będzie plik `out.csv`, który może posłużyć do dalszych analiz lub narysowania wykresów przez `plotResults.py`.

### Rysowanie wykresów

Wykresy na podstawie pliku wynikowego csv można narysować za pomocą:

```sh
python plotResults.py -i out.csv -eps 0.5 0.25 0.1 0.01 0.001 0.0001 -o processed.csv
```

Wynikiem będą wykresy poszczególnych testów w folderze \imgs oraz uśrednione wartości iteracji względem funkcji dull w folderze \imgs2.
