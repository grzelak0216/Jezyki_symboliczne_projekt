# Jezyki_symboliczne_projekt
# 15. Generator labiryntów
  ###    Lak Grzegorz 134120 GL04

## Opis zadania 

  * Główne okno programu zawiera kontrolki pozwalające na wybór wielkości labiryntu (liczba pól N na M; para liczb całkowitych nie większych niż 30), wizualizację labiryntu (na przykład jako siatka kolorowych przycisków) oraz przycisk "generuj". 
<<<<<<< HEAD
  * Labirynt składa się z pól będących korytarzem lub ścianą.
=======
  * Labirynt składa się z pól będących korytarzem lub ścianą. 
>>>>>>> 49434ca03e84ee452bfde30c2db537086e326b0b
  * Dla każdej pary pól będących korytarzem powinna istnieć ścieżka je łącząca (brak pól odłączonych od reszty labiryntu). Przechodzenie możliwe jest tylko na pola będące korytarzem które sąsiadują krawędzią z danym polem. 
  * Wygenerowany labirynt powinien posiadać ścieżkę od wejścia do wyjścia, która nie będzie linią prostą (poziomą lub pionową) i która powinna być zaznaczona na wizualizacji. 
  * Przechowywana jest lista punktów pośrednich ścieżki prowadzącej od wejścia do wyjścia. 
  * Po wybraniu dowolnego pola będącego korytarzem, dodawane jest ono na koniec listy punktów pośrednich. Następnie powinna zostać znaleziona i zaznaczona najkrótsza ścieżka prowadząca z wejścia do wyjścia przez wszystkie punkty pośrednie. 
  * Wybranie pola będącego punktem pośrednim powoduje usunięcie danego punktu pośredniego.
  * Labirynt nie może posiadać żadnego pokoju': obszar 2 na 2 pola korytarza (lub większy).
  * Labirynt nie może posiadać żadnych obszarów 3 na 3 pola ściany (lub większych). 
    
## Testy 

  1. Wygenerowanie labiryntu o wymiarach 11 na 13 pól. 
  2. Wygenerowanie labiryntu o wymiarach 21 na 11 pól. 
  3. Wygenerowanie labiryntu o wymiarach 11 na 11 z testem sprawdzającym wejście i wyjście. 
  4. Próba wygenerowania labiryntu z dwoma błędnymi wymiarami - oczekiwana informacja o błędzie.
  5. Próba wygenerowania labiryntu którego przynajmniej jeden z wymiarów wynosi 0 lub jest liczbą ujemną - oczekiwana informacja o błędzie. 
  6. Próba wygenerowania za dużego labiryntu - oczekiwana informacja o błędzie. 
  7. Wygenerowanie labiryntu o wymiarach 13 na 17, wygenerowanie najkrótszej drogi. 
  8. Próba wyszukania ścieżki przez pole będące ścianą - oczekiwane niepowodzenie przy próbie dodania punktu pośredniego 
