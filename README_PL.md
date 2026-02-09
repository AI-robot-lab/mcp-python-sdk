# MCP Python SDK

<div align="center">

<strong>Pythonowa implementacja Model Context Protocol (MCP)</strong>

[![PyPI][pypi-badge]][pypi-url]
[![MIT licensed][mit-badge]][mit-url]
[![Python Version][python-badge]][python-url]
[![Documentation][docs-badge]][docs-url]
[![Protocol][protocol-badge]][protocol-url]
[![Specification][spec-badge]][spec-url]

</div>

> [!IMPORTANT]
> **To jest gałąź `main`, która zawiera wersję v2 SDK (obecnie w fazie rozwoju, pre-alpha).**
>
> Przewidujemy stabilne wydanie v2 w Q1 2026. Do tego czasu **wersja v1.x pozostaje zalecaną wersją** do zastosowań produkcyjnych. Wersja v1.x będzie nadal otrzymywać poprawki błędów i aktualizacje bezpieczeństwa przez co najmniej 6 miesięcy po wydaniu v2, aby dać ludziom czas na aktualizację.
>
> Dokumentację i kod v1 znajdziesz w gałęzi [`v1.x` branch](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x).

<!-- omit in toc -->
## Spis treści

- [MCP Python SDK](#mcp-python-sdk)
  - [Przegląd](#przegląd)
  - [Instalacja](#instalacja)
    - [Dodawanie MCP do projektu Python](#dodawanie-mcp-do-projektu-python)
    - [Uruchamianie narzędzi deweloperskich MCP](#uruchamianie-narzędzi-deweloperskich-mcp)
  - [Szybki start](#szybki-start)
  - [Czym jest MCP?](#czym-jest-mcp)
  - [Podstawowe koncepcje](#podstawowe-koncepcje)
    - [Server - Serwer](#server---serwer)
    - [Resources - Zasoby](#resources---zasoby)
    - [Tools - Narzędzia](#tools---narzędzia)
    - [Prompts - Szablony](#prompts---szablony)
    - [Context - Kontekst](#context---kontekst)
  - [Uruchamianie serwera](#uruchamianie-serwera)
  - [Zastosowanie w robotyce - Robot Unitree G1](#zastosowanie-w-robotyce---robot-unitree-g1)
  - [Dokumentacja](#dokumentacja)
  - [Licencja](#licencja)

[pypi-badge]: https://img.shields.io/pypi/v/mcp.svg
[pypi-url]: https://pypi.org/project/mcp/
[mit-badge]: https://img.shields.io/pypi/l/mcp.svg
[mit-url]: https://github.com/modelcontextprotocol/python-sdk/blob/main/LICENSE
[python-badge]: https://img.shields.io/pypi/pyversions/mcp.svg
[python-url]: https://www.python.org/downloads/
[docs-badge]: https://img.shields.io/badge/docs-python--sdk-blue.svg
[docs-url]: https://modelcontextprotocol.github.io/python-sdk/
[protocol-badge]: https://img.shields.io/badge/protocol-modelcontextprotocol.io-blue.svg
[protocol-url]: https://modelcontextprotocol.io
[spec-badge]: https://img.shields.io/badge/spec-spec.modelcontextprotocol.io-blue.svg
[spec-url]: https://modelcontextprotocol.io/specification/latest

## 🚀 Szybki start dla studentów

**Dla studentów Politechniki Rzeszowskiej:** Zobacz [SZYBKI_START.md](./SZYBKI_START.md) - wprowadzenie w 5 minut!

**Pełna dokumentacja po polsku:**
- 📖 [SZYBKI_START.md](./SZYBKI_START.md) - Start w 5 minut
- 📚 [PRZEWODNIK_STUDENTA.md](./PRZEWODNIK_STUDENTA.md) - Kompletny przewodnik
- 🤖 [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md) - Robot Unitree G1
- 🎓 [docs/tutorial_pl.md](./docs/tutorial_pl.md) - Tutorial krok po kroku
- 💻 [examples/README_PL.md](./examples/README_PL.md) - Przewodnik po przykładach

## Przegląd

**Model Context Protocol (MCP)** pozwala aplikacjom dostarczać kontekst dla modeli językowych (LLM) w ustandaryzowany sposób, oddzielając zagadnienia dostarczania kontekstu od właściwej interakcji z LLM. 

### Po co nam MCP? Kluczowe korzyści:

1. **Standaryzacja komunikacji** - Zamiast tworzyć własne protokoły dla każdego projektu, MCP oferuje ujednolicony sposób komunikacji między aplikacjami a modelami AI.

2. **Modularność** - Możesz tworzyć niezależne serwery MCP, które dostarczają różne funkcjonalności (narzędzia, dane, szablony) i łączyć je w większe systemy.

3. **Bezpieczeństwo** - MCP zapewnia kontrolowaną wymianę danych z jasno zdefiniowanymi interfejsami, co jest kluczowe w projektach robotycznych.

### Python SDK implementuje pełną specyfikację MCP, umożliwiając:

- **Budowanie klientów MCP** - które mogą łączyć się z dowolnym serwerem MCP
- **Tworzenie serwerów MCP** - które udostępniają zasoby (Resources), szablony (Prompts) i narzędzia (Tools)
- **Użycie standardowych transportów** - takich jak stdio, SSE, i Streamable HTTP
- **Obsługę wszystkich komunikatów protokołu MCP** - i zdarzeń cyklu życia

## 🚀 Szybki start dla studentów

**Dla studentów Politechniki Rzeszowskiej:** Zobacz [SZYBKI_START.md](./SZYBKI_START.md) - wprowadzenie w 5 minut!

**Pełna dokumentacja po polsku:**
- 📖 [SZYBKI_START.md](./SZYBKI_START.md) - Start w 5 minut
- 📚 [PRZEWODNIK_STUDENTA.md](./PRZEWODNIK_STUDENTA.md) - Kompletny przewodnik
- 🤖 [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md) - Robot Unitree G1
- 🎓 [docs/tutorial_pl.md](./docs/tutorial_pl.md) - Tutorial krok po kroku
- 💻 [examples/README_PL.md](./examples/README_PL.md) - Przewodnik po przykładach

## Instalacja

### Dodawanie MCP do projektu Python

Zalecamy używanie [uv](https://docs.astral.sh/uv/) do zarządzania projektami Python. Jest to nowoczesne narzędzie, które łączy w sobie funkcjonalność pip, venv i poetry.

**Krok 1:** Jeśli jeszcze nie utworzyłeś projektu zarządzanego przez uv, stwórz go:

```bash
# Inicjalizacja nowego projektu
uv init mcp-server-demo
cd mcp-server-demo
```

**Krok 2:** Dodaj MCP do zależności projektu:

```bash
# Dodanie MCP z narzędziami CLI (command-line interface)
uv add "mcp[cli]"
```

**Alternatywnie**, dla projektów używających pip:

```bash
pip install "mcp[cli]"
```

### Uruchamianie narzędzi deweloperskich MCP

Aby uruchomić polecenie `mcp` z uv:

```bash
# Uruchomienie narzędzia mcp
uv run mcp
```

## Szybki start

Stwórzmy prosty serwer MCP, który udostępnia narzędzie kalkulatora i przykładowe dane:

```python
"""Przykład szybkiego startu z MCPServer.

Uruchom z katalogu głównego repozytorium:
    uv run examples/snippets/servers/mcpserver_quickstart.py
"""

from mcp.server.mcpserver import MCPServer

# Krok 1: Tworzenie instancji serwera MCP
# MCPServer to główna klasa obsługująca komunikację z klientami MCP
mcp = MCPServer("Demo")


# Krok 2: Dodanie narzędzia (Tool)
# Dekorator @mcp.tool() automatycznie rejestruje funkcję jako narzędzie MCP
# Narzędzia to funkcje, które model AI może wywoływać do wykonania akcji
@mcp.tool()
def add(a: int, b: int) -> int:
    """Dodaj dwie liczby
    
    Model AI może użyć tego narzędzia do wykonywania obliczeń matematycznych.
    Typy parametrów (int) są automatycznie walidowane przez MCP.
    """
    return a + b


# Krok 3: Dodanie zasobu dynamicznego (Resource)
# Resources to dane, które model AI może odczytywać
# Wzorzec {name} w URI tworzy dynamiczny zasób - można podstawiać różne wartości
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Pobierz spersonalizowane powitanie
    
    Przykład użycia URI:
    - greeting://Jan -> "Hello, Jan!"
    - greeting://Maria -> "Hello, Maria!"
    """
    return f"Hello, {name}!"


# Krok 4: Dodanie szablonu (Prompt)
# Prompts to szablony interakcji z modelem AI
# Pozwalają na wielokrotne użycie tych samych wzorców komunikacji
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generuj szablon powitania
    
    Args:
        name: Imię osoby do powitania
        style: Styl powitania (friendly/formal/casual)
    
    Ten szablon pomoże modelowi AI wygenerować odpowiednie powitanie
    w zależności od wybranego stylu.
    """
    styles = {
        "friendly": "Napisz ciepłe, przyjacielskie powitanie",
        "formal": "Napisz formalne, profesjonalne powitanie",
        "casual": "Napisz swobodne, nieformalne powitanie",
    }
    
    return f"{styles.get(style, styles['friendly'])} dla osoby o imieniu {name}."


# Krok 5: Uruchomienie serwera
# transport="streamable-http" - serwer będzie dostępny przez HTTP
# json_response=True - odpowiedzi w formacie JSON
if __name__ == "__main__":
    mcp.run(transport="streamable-http", json_response=True)
```

**Uruchomienie przykładu:**

```bash
# Uruchom serwer
uv run --with mcp examples/snippets/servers/mcpserver_quickstart.py
```

**Testowanie z MCP Inspector:**

```bash
# W nowym terminalu uruchom Inspector
npx -y @modelcontextprotocol/inspector
```

W interfejsie Inspector połącz się z `http://localhost:8000/mcp`.

## Czym jest MCP?

**Model Context Protocol (MCP)** to otwarty protokół, który umożliwia budowanie serwerów udostępniających dane i funkcjonalności aplikacjom LLM w bezpieczny, ustandaryzowany sposób.

### Analogia do API webowego:

Pomyśl o MCP jak o Web API, ale specjalnie zaprojektowanym do interakcji z modelami językowymi. 

### Główne komponenty MCP:

1. **Resources (Zasoby)** - Podobne do endpointów GET w REST API
   - Służą do ładowania informacji do kontekstu LLM
   - Przykład: odczyt plików, konfiguracji, danych z bazy

2. **Tools (Narzędzia)** - Podobne do endpointów POST w REST API  
   - Służą do wykonywania kodu lub wywoływania efektów ubocznych
   - Przykład: wysłanie wiadomości, sterowanie robotem, zapis do pliku

3. **Prompts (Szablony)** - Wielokrotnie używane wzorce interakcji z LLM
   - Definiują standardowe sposoby komunikacji
   - Przykład: szablon do analizy danych, szablon do generowania raportów

## Podstawowe koncepcje

### Server - Serwer

**MCPServer** to Twój główny interfejs do protokołu MCP. Obsługuje:
- Zarządzanie połączeniami
- Zgodność z protokołem
- Routing wiadomości

```python
"""Przykład pokazujący obsługę cyklu życia serwera (startup/shutdown)."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.mcpserver import Context, MCPServer
from mcp.server.session import ServerSession


# Klasa symulująca połączenie z bazą danych
class Database:
    """Przykładowa klasa bazy danych."""
    
    @classmethod
    async def connect(cls) -> "Database":
        """Nawiąż połączenie z bazą danych."""
        return cls()
    
    async def disconnect(self) -> None:
        """Rozłącz się z bazą danych."""
        pass
    
    def query(self) -> str:
        """Wykonaj zapytanie."""
        return "Wynik zapytania"


@dataclass
class AppContext:
    """Kontekst aplikacji z zależnościami typowanymi."""
    db: Database


@asynccontextmanager
async def app_lifespan(server: MCPServer) -> AsyncIterator[AppContext]:
    """Zarządzaj cyklem życia aplikacji z type-safe kontekstem.
    
    Ta funkcja jest wywoływana:
    - RAZ przy starcie serwera (yield)
    - RAZ przy zamykaniu serwera (finally)
    
    Pozwala to na:
    - Inicjalizację połączeń (baza danych, API)
    - Załadowanie konfiguracji
    - Czyszczenie zasobów przy zamykaniu
    """
    # Inicjalizacja przy starcie
    db = await Database.connect()
    try:
        # Przekazanie kontekstu do wszystkich narzędzi
        yield AppContext(db=db)
    finally:
        # Czyszczenie przy zamykaniu
        await db.disconnect()


# Przekazanie funkcji lifespan do serwera
mcp = MCPServer("My App", lifespan=app_lifespan)


# Dostęp do type-safe kontekstu w narzędziach
@mcp.tool()
def query_db(ctx: Context[ServerSession, AppContext]) -> str:
    """Narzędzie używające zainicjalizowanych zasobów.
    
    Parametr ctx daje dostęp do:
    - ctx.request_context.lifespan_context.db - nasz obiekt bazy danych
    - ctx.session - informacje o sesji
    - ctx.info(), ctx.debug() - metody logowania
    """
    db = ctx.request_context.lifespan_context.db
    return db.query()
```

### Resources - Zasoby

**Resources** to sposób na udostępnienie danych modelom AI. Są podobne do endpointów GET w REST API - dostarczają dane, ale nie powinny wykonywać znaczących obliczeń ani mieć efektów ubocznych.

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer(name="Przykład zasobów")


# Zasób dynamiczny - {name} to parametr
# URI: file://documents/raport.txt -> name="raport.txt"
@mcp.resource("file://documents/{name}")
def read_document(name: str) -> str:
    """Odczytaj dokument po nazwie.
    
    W rzeczywistym zastosowaniu ta funkcja:
    - Odczytałaby plik z dysku
    - Sprawdziłaby uprawnienia
    - Zwróciłaby zawartość pliku
    """
    return f"Zawartość dokumentu: {name}"


# Zasób statyczny - stały URI
@mcp.resource("config://settings")
def get_settings() -> str:
    """Pobierz ustawienia aplikacji.
    
    Zwraca konfigurację w formacie JSON.
    Model AI może użyć tych informacji do dostosowania swojej pracy.
    """
    return """{
  "theme": "dark",
  "language": "pl",
  "debug": false
}"""
```

### Tools - Narzędzia

**Tools** pozwalają modelom AI wykonywać akcje przez Twój serwer. W przeciwieństwie do Resources, Tools mogą wykonywać obliczenia i mieć efekty uboczne.

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer(name="Przykład narzędzi")


@mcp.tool()
def sum(a: int, b: int) -> int:
    """Dodaj dwie liczby.
    
    Typy parametrów (int) są automatycznie walidowane.
    Model AI otrzyma błąd, jeśli spróbuje przekazać inny typ danych.
    """
    return a + b


@mcp.tool()
def get_weather(city: str, unit: str = "celsius") -> str:
    """Pobierz pogodę dla miasta.
    
    Args:
        city: Nazwa miasta
        unit: Jednostka temperatury (celsius/fahrenheit)
    
    W rzeczywistej implementacji:
    - Wywołałbyś API pogodowe
    - Obsłużyłbyś błędy połączenia
    - Sformatowałbyś dane pogodowe
    """
    return f"Pogoda w {city}: 22 stopni {unit[0].upper()}"
```

**Narzędzia z raportowaniem postępu:**

```python
from mcp.server.mcpserver import Context, MCPServer
from mcp.server.session import ServerSession

mcp = MCPServer(name="Przykład postępu")


@mcp.tool()
async def long_running_task(
    task_name: str, 
    ctx: Context[ServerSession, None], 
    steps: int = 5
) -> str:
    """Wykonaj długotrwałe zadanie z aktualizacjami postępu.
    
    Parametr ctx jest automatycznie wstrzykiwany przez framework MCPServer
    i NIE musi być przekazywany przez model AI.
    
    Context zapewnia metody:
    - ctx.info() - logowanie informacji
    - ctx.debug() - logowanie debugowania  
    - ctx.report_progress() - raportowanie postępu
    """
    # Logowanie rozpoczęcia zadania
    await ctx.info(f"Rozpoczynam: {task_name}")
    
    # Wykonanie zadania krok po kroku
    for i in range(steps):
        # Obliczenie postępu (0.0 - 1.0)
        progress = (i + 1) / steps
        
        # Raportowanie postępu do klienta
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Krok {i + 1}/{steps}",
        )
        
        # Logowanie debugowania
        await ctx.debug(f"Ukończono krok {i + 1}")
    
    return f"Zadanie '{task_name}' zakończone"
```

### Prompts - Szablony

**Prompts** to wielokrotnie używane szablony do interakcji z LLM. Definiują standardowe wzorce komunikacji.

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer(name="Przykład szablonów")


@mcp.prompt()
def analyze_data(data_type: str, detail_level: str = "medium") -> str:
    """Szablon do analizy danych.
    
    Args:
        data_type: Typ danych do analizy (sensory/logs/metrics)
        detail_level: Poziom szczegółowości (basic/medium/detailed)
    
    Zwraca szablon instrukcji dla modelu AI.
    """
    levels = {
        "basic": "Wykonaj podstawową analizę",
        "medium": "Wykonaj szczegółową analizę z wizualizacjami",
        "detailed": "Wykonaj kompleksową analizę z rekomendacjami",
    }
    
    return f"{levels.get(detail_level, levels['medium'])} danych typu {data_type}."
```

### Context - Kontekst

**Context** dostarcza informacji o bieżącym zapytaniu i dostęp do możliwości MCP. Jest automatycznie wstrzykiwany do funkcji przez framework.

```python
from mcp.server.mcpserver import Context, MCPServer
from mcp.server.session import ServerSession

mcp = MCPServer(name="Przykład kontekstu")


@mcp.tool()
async def smart_tool(
    param: str,
    ctx: Context[ServerSession, None]  # Automatycznie wstrzykiwany - NIE przekazywany przez AI
) -> str:
    """Narzędzie wykorzystujące kontekst.
    
    Context daje dostęp do:
    - ctx.session - informacje o sesji
    - ctx.info(), ctx.debug(), ctx.error() - metody logowania
    - ctx.report_progress() - raportowanie postępu
    - ctx.request_context - kontekst zapytania
    """
    # Logowanie informacji
    await ctx.info(f"Wywołano narzędzie z parametrem: {param}")
    
    # Logowanie debugowania (tylko jeśli włączone)
    await ctx.debug(f"Session ID: {ctx.session.session_id}")
    
    # Wykonanie operacji...
    result = f"Przetworzono: {param}"
    
    await ctx.info("Operacja zakończona pomyślnie")
    return result
```

## Uruchamianie serwera

### Tryb deweloperski

Najszybszy sposób na testowanie serwera:

```bash
# Uruchom serwer z transportem HTTP
uv run twoj_serwer.py
```

### Integracja z Claude Desktop

```bash
# Dodaj serwer do Claude Desktop
claude mcp add --transport http moj-serwer http://localhost:8000/mcp
```

### Transport Streamable HTTP

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Mój Serwer")

# ... definicje narzędzi, zasobów, szablonów ...

if __name__ == "__main__":
    # Uruchomienie z transportem HTTP na porcie 8000
    mcp.run(transport="streamable-http", port=8000, json_response=True)
```

## Zastosowanie w robotyce - Robot Unitree G1

MCP Python SDK jest idealnym narzędziem do projektów z robotami humanoidalnymi jak **Unitree G1 EDU-U6**. Zobacz szczegółowy przewodnik: [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md)

### Przykładowe zastosowania:

1. **Sterowanie ruchem robota** - Tools do kontroli stawów i ruchu
2. **Odczyt sensorów** - Resources dostarczające dane z kamer, IMU, czujników siły
3. **Planowanie trajektorii** - Tools do obliczania i wykonywania trajektorii ruchu
4. **Wizja komputerowa** - Integracja z systemami rozpoznawania obiektów
5. **Interakcja człowiek-robot** - Prompts do naturalnej komunikacji

Więcej informacji: [PRZEWODNIK_STUDENTA.md](./PRZEWODNIK_STUDENTA.md)

## Dokumentacja

- 📖 [Pełna dokumentacja w języku angielskim](https://modelcontextprotocol.github.io/python-sdk/)
- 📚 [Przewodnik dla studentów (PL)](./PRZEWODNIK_STUDENTA.md)
- 🤖 [Przewodnik Unitree G1 (PL)](./UNITREE_G1_PRZEWODNIK.md)
- 🔧 [Specyfikacja protokołu MCP](https://modelcontextprotocol.io/specification/latest)

## Licencja

Ten projekt jest licencjonowany na licencji MIT - zobacz plik [LICENSE](LICENSE) dla szczegółów.
