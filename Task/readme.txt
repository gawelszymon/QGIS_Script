Konfiguracja:

Wersja QGIS:
QGIS 3.22.4-Białowieża 'Białowieża'
Program QGIS zainstalowałem na systemie operacyjnym linux mint
_____________________________________________________________________________________________________________________

Oprócz pracy w środowisku QGIS kod pisałem w PyCharm.
Problemem okazała się instalacja wszelakich modułów wymaganych do pracy z narzędziem QGIS,
czy to pip, czy conda nie mogła sobie poradzić z zainstalowaniem wymaganych pakietów, modułów,
ze względu na goniący mnie czas w ostateczności postanowiłem przenieść ręcznie odpowiednie
moduły z QGIS do odpowiedniej biblioteki mojego interpretera, z którego korzystam w PyCharm.

#TODO
TRZEBA PAMIETAĆ ABY W 94 LINIJCE ZMIENIĆ LOKALIZACJE PLIKU  'network_node.csv', niestety nie zdąrzyłem już tego
usprawnić.

#TODO
Skrypt uruchamiamy we consoli python środowiska QGIS za pomocą polecenia:
exec(open('lokalizacjaSkryptuNaKomputerze/task.py').read())

__________________________________________________________________________________________________________________
Wykonanie Projektu:

Poza takimi czynnościami jak wczytanie mapy, obsługa błędów, możliwość wygodnego przybliżenia,
czy niedopracowana jeszcze funkcjonalność bufforwania, W projekcie postanowiłem zaimplementować
uproszczoną topologię- w domyślę sieci światłowodowej, gdzie mamy możliwość pełnego
aktualizowania użytkowników naszej sieci w pliku network_nodes.csv, w pliku tym deklarujemy
współrzędne geograficzne użytkowników sieci, a także ich ilość.

Projekt dostarcza uproszczone narzędzie, które pozwala dostosować optymalną topologię sieci poprzez
zastosowanie w nim algorytmu Held-Karpa rozwiązującego problem Komiwojażera (znajduje cykl hamiltona).
W skrypcie przeprowadzam symulacje, która na podstawie grafu pełnego i losowo przydzielonych kosztów
przesłu między wszystkimi użytkownikami w sieci jest w stanie dobrać najlepszą aktualnie możliwą
implementacje sieci światłowodowej. Za Koszt możemy rozumieć wszystkie czynniki, które wpływają na
rozbudowę sieci światłowodowej na danym terenie. Im niższy koszt, tym dane połączenie jest bardzije preferowane.

W projekcie chciałem też zastosować mechanizm analizowania najlepszej trasy dla wysyłanego pakietu między
użytkownikami(analiza przepustowości łącza), trzeba by skorzystać z algorytmu Dijkstry, brakło już czasu.
Poza tym chciałbym jeszcze więcej popracować z narzędziem QGIS, aby cały czas lepiej je poznawać.

_____________________________________________________________________________________________________________________
Mam nadzieję, że nie będzie żadnych problemów z uruchomieniem skryptu w związku z tym, że zadanie było
wykonywane na linuxie.

Dzięki!