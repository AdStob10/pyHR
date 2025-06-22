## pyHR - HR mangament application

Główną funkcją aplikacji jest obsługa wniosków urlopowych pracowników.

Zwykły pracownik może:
- Dodać nowy wniosek urlopowy (określony typ urlopu i zakres) 
- Przeglądać swoje istniejące wnioski urlopowe (filtrowanie i sortowanie)
- Oglądać statystyki urlopów w formie wykresów
- Przeglądać informacje na temat swojego konta

W aplikacji istnieje też rola przełożonego:
- Ma on dostęp do wszystkich funkcjonalności zwykłego pracownika
- Może przeglądać listę swoich podwładnych i przeglądać informacje na ich temat (filtrowanie i sortowanie)
- Może dodawać nowych pracowników
- Może przeglądać wnioski urlopowe swoich podwładnych (filtrowaie i sortowanie)
- Może akceptować lub odrzucać wnioski urlopowe swoich podwładnych

Aplikacja składa się z trzech komponentów
 - API zrealizowane w Pythonie z wykorzytaniem FastAPI i SQLModel (port: 8000)
 - Interfejsu webowego wykonanego w Javascript z wykorzystaniem SvelteKit (port: 3000)
 - Bazy danych PostgreSQL (port: 5432)


Do uruchomienia aplikacji potrzebny jest docker.
Wersje produkcyjną uruchamia się poniższym poleceniem
 ```
docker compose --profile production up
 ```

 W aplikacji zdefiniowanych jest trzech testowych użytkowników o poniższych loginach:
 - `test_emp` - testowe konto zwykłego pracownika
 - `test_man` - testowe konto przełożonego
 - `admin` - testowe konto admina

 Wszystkie konta używają tego samego hasła `test123`

