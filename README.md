# Systemy operacyjne 2

## Projekt pierwszy - Problem jedzących filozofów

### Opis problemu

Problem jedzących filozofów to klasyczny problem synchronizacji procesów, zaproponowany przez Edsgera Dijkstrę w 1965
roku. Problem ten polega na stworzeniu modelu, w którym filozofowie siedzą przy okrągłym stole, a między każdą parą
sąsiadujących filozofów znajduje się widelec. Filozof może albo jeść, albo myśleć. Aby zjeść posiłek, musi podnieść dwa
widelce znajdujące się po jego lewej i prawej stronie. Po zakończeniu posiłku odkłada widelce i zaczyna myśleć. Problem
polega na zaprojektowaniu algorytmu, który zapewni, że żaden z filozofów nie umrze z głodu, a także że nie wystąpi
zablokowania wątków (ang. Deadlock).

### Rozwiązanie

### Synchronizacja dostępu do widelców za pomocą semaforów

Problem został rozwiązany za pomocą **semaforów** z biblioteki `<semaphore>`, które zapewniają synchronizację dostępu do
współdzielonych zasobów – w tym przypadku **widelców** (warto by było nazwać to pałeczki (ang. chopstick)).

Każdy widelec jest reprezentowany przez **semafor binarny** (`std::counting_semaphore<1>`), który może przyjmować dwa
stany:

- **wolny** (`1`) – dostępny do podniesienia przez filozofa,
- **zajęty** (`0`) – używany przez jednego z filozofów.

#### Mechanizm działania:

1. **Filozof myśli**, co symuluje 1 sekundowe opóźnienie w działaniu.
2. **Próbuje podnieść dwa widelce** – najpierw ten po swojej lewej stronie, potem po prawej.

   - Jeśli oba są dostępne, filozof przechodzi do jedzenia.
   - Jeśli choć jeden jest zajęty, filozof czeka na jego zwolnienie.

3. **Filozof zaczyna jeść**, trzymając w rękach oba widelce. Symuluje to 5 sekundowe opóźnienie w działaniu.
4. **Po zakończeniu jedzenia odkłada widelce**, czyli zwalnia semafory, aby inne wątki mogły z nich skorzystać.
5. **Cykl się powtarza** – filozof wraca do myślenia.

Te rozwiązanie wygląda jest proste i zrozumiałe, jednoczenie zapewnia bezpieczeństwo dostępu do widelców, eliminując
zablokowania i zagłodzenie filozofów.

### Synchronizacja dostępu do standardowego wyjścia

Aby zapewnić czytelne i zrozumiałe wyprowadzanie informacji na ekran, użyto **mutexów** (`<mutex>`) do
synchronizacji dostępu do standardowego wyjścia (`std::cout`).

W kodzie zastosowano `std::mutex coutMutex`, który jest blokowany za pomocą `std::lock_guard<std::mutex>` w krytycznych
sekcjach kodu, gdzie następuje wypisywanie do konsoli.

### Główne klasy

#### Klasa `Philosopher`

Klasa `Philosopher` reprezentuje filozofa w problemie jedzących filozofów. Każdy filozof ma unikalne ID oraz referencję
do wektora widelców (semaforów). Klasa zawiera metody symulujące filozofa w problemnie jedzących filozofów.

- **Konstruktor**: Inicjalizuje filozofa z ID i referencją do widelców.
- **Operator wywołania funkcji**: Rozpoczyna nieskończoną pętlę, w której filozof myśli, podnosi widelce, je i odkłada
  widelce.
- **thinking()**: Symuluje myślenie filozofa przez 1 sekundę.
- **eating()**: Symuluje jedzenie filozofa przez 5 sekund.
- **pickUp()**: Filozof podnosi dwa widelce (zajmuje 2 semafory po lewej i prawej).
- **putDown()**: Filozof odkłada dwa widelce (zwalnia 2 semafory semafory po lewej i prawej).

### Plik główny

#### Plik `main.cpp`

- **main()**: Główna funkcja programu. Pobiera liczbę filozofów z argumentu wiersza poleceń, tworzy wektor wątków
  filozofów oraz wektor widelców (semaforów). Inicjalizuje widelce, tworzy i uruchamia wątki filozofów, a następnie
  dołącza wątki.

### Kompilacja i uruchomienie

Aby skompilować i uruchomić program, użyj następujących poleceń:

```sh
make
```

```sh
./dining_philosophers <liczba_filozofów>
```

### Usuwanie plików wykonywalnych
```sh
make clean
```