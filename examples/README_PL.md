# Przykłady MCP Python SDK - Przewodnik po polsku

> **Uwaga:** Ten dokument to polskie tłumaczenie i rozszerzenie README.md w tym katalogu.
> Został przygotowany specjalnie dla studentów Politechniki Rzeszowskiej.

## 📚 Spis treści

- [Wprowadzenie](#wprowadzenie)
- [Struktura katalogów](#struktura-katalogów)
- [Przykłady dla początkujących](#przykłady-dla-początkujących)
- [Przykłady zaawansowane](#przykłady-zaawansowane)
- [Przykłady robotyczne](#przykłady-robotyczne)
- [Jak uruchamiać przykłady](#jak-uruchamiać-przykłady)
- [Testowanie z MCP Inspector](#testowanie-z-mcp-inspector)

---

## 🎯 Wprowadzenie

Ten folder zawiera przykłady użycia MCP Python SDK. Wszystkie przykłady są w pełni funkcjonalne i mogą być uruchamiane bezpośrednio.

### Dla kogo są te przykłady?

1. **Początkujący** - Proste przykłady pokazujące podstawy MCP
2. **Średniozaawansowani** - Przykłady z integracją różnych transportów
3. **Zaawansowani** - Przykłady z autentykacją, paginacją, strukturowanymi danymi
4. **Studenci robotyki** - Przykłady zastosowania MCP w robotyce

---

## 📁 Struktura katalogów

```
examples/
├── mcpserver/                    # Proste przykłady serwerów MCPServer
│   ├── simple_echo.py           # ⭐ ZACZYNAJ TUTAJ - najprostszy przykład
│   ├── robot_educational.py     # ⭐ Przykład robotyczny z komentarzami PL
│   ├── weather_structured.py    # Strukturowane odpowiedzi (Pydantic)
│   └── ...                      # Inne przykłady
│
├── servers/                      # Kompletne przykładowe serwery
│   ├── simple-tool/             # Serwer z narzędziem fetch
│   ├── simple-resource/         # Serwer z zasobami
│   ├── simple-prompt/           # Serwer z promptami
│   ├── simple-auth/             # Serwer z autentykacją
│   └── ...                      # Inne serwery
│
└── clients/                      # Przykładowe klienty MCP
    ├── simple-task-client/      # Klient wykonujący zadania
    └── ...                      # Inne klienty
```

---

## 🌟 Przykłady dla początkujących

### 1. `mcpserver/simple_echo.py` - Najprostszy serwer

**Co pokazuje:** Absolutne minimum kodu potrzebnego do serwera MCP.

**Poziom:** ⭐ Początkujący

**Uruchomienie:**
```bash
uv run examples/mcpserver/simple_echo.py
```

**Zawartość:**
- Utworzenie serwera MCP
- Definicja jednego narzędzia (Tool)
- Podstawy dekoratorów

**Kiedy użyć jako wzorca:**
- Tworzysz pierwszy serwer MCP
- Potrzebujesz prostego przykładu do nauki
- Chcesz przetestować instalację MCP

---

### 2. `mcpserver/robot_educational.py` - Robot edukacyjny

**Co pokazuje:** Kompletny przykład serwera MCP dla robotyki z polskimi komentarzami.

**Poziom:** ⭐⭐ Początkujący/Średnio-zaawansowani

**Uruchomienie:**
```bash
uv run examples/mcpserver/robot_educational.py
```

**Zawartość:**
- ✅ Symulator robota z 3 stawami
- ✅ Resources - odczyt stanu robota
- ✅ Tools - sterowanie robotem
- ✅ Prompts - szablony diagnostyczne
- ✅ Context & Lifespan - zarządzanie zasobami
- ✅ Logowanie i raportowanie postępu
- ✅ **PEŁNE polskie komentarze edukacyjne**

**Kiedy użyć jako wzorca:**
- Tworzysz serwer MCP dla robota
- Potrzebujesz przykładu z Resources, Tools i Prompts
- Uczysz się Context i Lifespan
- Projekt z robotem Unitree G1 lub innym

**Kluczowe koncepcje:**
```python
# 1. Lifespan - zarządzanie cyklem życia
@asynccontextmanager
async def app_lifespan(server):
    robot = RobotSimulator()  # Inicjalizacja
    yield AppContext(robot=robot)
    # Czyszczenie przy zamykaniu

# 2. Resource - odczyt danych
@mcp.resource("robot://joints/all")
def get_all_joints(ctx):
    return robot.get_all_joints()

# 3. Tool - wykonanie akcji
@mcp.tool()
async def move_joint(joint_name, position, ctx):
    await ctx.info(f"Przesuwam {joint_name}")
    return robot.move_joint(joint_name, position)

# 4. Prompt - szablon dla AI
@mcp.prompt()
def diagnose_robot():
    return "Instrukcje diagnostyczne..."
```

---

### 3. `servers/simple-tool/` - Serwer z narzędziem fetch

**Co pokazuje:** Jak stworzyć serwer z narzędziem pobierającym strony WWW.

**Poziom:** ⭐⭐ Średnio-zaawansowani

**Uruchomienie:**
```bash
cd examples/servers/simple-tool
uv run mcp-simple-tool
```

**Zawartość:**
- Narzędzie `fetch` do pobierania stron
- Obsługa dwóch transportów (stdio, SSE)
- Struktura projektu z pyproject.toml

**Kiedy użyć jako wzorca:**
- Tworzysz serwer z narzędziem wykonującym HTTP requests
- Potrzebujesz wsparcia dla wielu transportów
- Budujesz pakiet do dystrybucji

---

### 4. `servers/simple-resource/` - Serwer z zasobami

**Co pokazuje:** Jak udostępniać dane przez Resources.

**Poziom:** ⭐⭐ Średnio-zaawansowani

**Uruchomienie:**
```bash
cd examples/servers/simple-resource
uv run mcp-simple-resource
```

**Zawartość:**
- Resources do odczytu plików
- Dynamiczne URI z parametrami
- Lista zasobów

**Kiedy użyć jako wzorca:**
- Udostępniasz dane (pliki, konfigurację, stan)
- Potrzebujesz dynamicznych URI
- Budujesz system do przeglądania zasobów

---

## 🔥 Przykłady zaawansowane

### 5. `mcpserver/weather_structured.py` - Strukturowane odpowiedzi

**Co pokazuje:** Jak używać Pydantic, TypedDict i dataclass do strukturowanych danych.

**Poziom:** ⭐⭐⭐ Zaawansowani

**Uruchomienie:**
```bash
uv run examples/mcpserver/weather_structured.py
```

**Zawartość:**
- 6 różnych sposobów strukturyzacji danych
- Pydantic BaseModel
- TypedDict
- dataclass
- Zagnieżdżone modele
- Automatyczna walidacja

**Kiedy użyć jako wzorca:**
- Zwracasz strukturowane dane z API
- Potrzebujesz walidacji typów
- AI/LLM ma przetwarzać dane w określonym formacie

**Przykład:**
```python
from pydantic import BaseModel, Field

class WeatherData(BaseModel):
    temperature: float = Field(description="Temp in Celsius")
    humidity: float = Field(description="Humidity %")
    condition: str

@mcp.tool()
def get_weather(city: str) -> WeatherData:
    return WeatherData(
        temperature=22.5,
        humidity=65.0,
        condition="partly cloudy"
    )
```

---

### 6. `servers/simple-auth/` - Autentykacja OAuth

**Co pokazuje:** Jak zabezpieczyć serwer MCP autentykacją OAuth.

**Poziom:** ⭐⭐⭐ Zaawansowani

**Uruchomienie:**
```bash
cd examples/servers/simple-auth
uv run mcp-simple-auth
```

**Zawartość:**
- Implementacja OAuth 2.0
- Weryfikacja tokenów
- Zabezpieczanie narzędzi

**Kiedy użyć jako wzorca:**
- Tworzysz serwer wymagający uwierzytelnienia
- Integracja z systemami OAuth
- Potrzebujesz kontroli dostępu

---

### 7. `servers/simple-pagination/` - Paginacja wyników

**Co pokazuje:** Jak obsługiwać duże zbiory danych z paginacją.

**Poziom:** ⭐⭐⭐ Zaawansowani

**Uruchomienie:**
```bash
cd examples/servers/simple-pagination
uv run mcp-simple-pagination
```

**Zawartość:**
- Cursor-based pagination
- Obsługa dużych list
- Optymalizacja pamięci

**Kiedy użyć jako wzorca:**
- Zwracasz duże listy (>100 elementów)
- Potrzebujesz efektywnej paginacji
- Optymalizujesz zużycie pamięci

---

## 🤖 Przykłady robotyczne

### Dla projektów z robotem Unitree G1

**Główny przykład:** `mcpserver/robot_educational.py`

**Rozszerzone przewodniki:**
- [PRZEWODNIK_STUDENTA.md](../../PRZEWODNIK_STUDENTA.md) - Kompletny przewodnik MCP
- [UNITREE_G1_PRZEWODNIK.md](../../UNITREE_G1_PRZEWODNIK.md) - Specyficzne dla Unitree G1

**Kluczowe wzorce dla robotyki:**

#### 1. Odczyt sensorów (Resources)
```python
@mcp.resource("robot://sensors/imu")
def get_imu_data(ctx):
    """Odczyt z IMU (orientacja, przyspieszenie)"""
    return robot.get_imu_data()
```

#### 2. Sterowanie robotem (Tools)
```python
@mcp.tool()
async def move_joint(joint_name: str, position: float, ctx):
    """Sterowanie stawem z bezpieczeństwem"""
    # Sprawdź limity
    if not validate_position(joint_name, position):
        return "❌ Pozycja poza zakresem"
    
    # Wykonaj ruch
    await ctx.info(f"Przesuwam {joint_name}")
    return robot.move_joint(joint_name, position)
```

#### 3. Diagnostyka (Prompts)
```python
@mcp.prompt()
def diagnose_balance():
    """Szablon diagnostyki równowagi"""
    return """
    1. Odczytaj IMU
    2. Sprawdź siły w stopach
    3. Oceń stabilność
    4. Wygeneruj raport
    """
```

#### 4. Stop awaryjny (Tool)
```python
@mcp.tool()
async def emergency_stop(ctx):
    """KRYTYCZNE - zawsze dostępne"""
    await ctx.info("🚨 STOP AWARYJNY")
    robot.emergency_stop()
    return "✅ Robot zatrzymany"
```

---

## 🚀 Jak uruchamiać przykłady

### Metoda 1: Uruchomienie bezpośrednie

```bash
# Dla przykładów w mcpserver/
uv run examples/mcpserver/nazwa_pliku.py

# Przykład:
uv run examples/mcpserver/simple_echo.py
uv run examples/mcpserver/robot_educational.py
```

### Metoda 2: Instalacja jako pakiet

```bash
# Wejdź do katalogu serwera
cd examples/servers/simple-tool

# Uruchom bezpośrednio
uv run mcp-simple-tool

# Lub z opcjami
uv run mcp-simple-tool --transport sse --port 8000
```

### Metoda 3: Instalacja globalna (opcjonalnie)

```bash
cd examples/servers/simple-tool
uv pip install -e .
mcp-simple-tool
```

---

## 🔍 Testowanie z MCP Inspector

**MCP Inspector** to narzędzie do testowania serwerów MCP w przeglądarce.

### Krok 1: Uruchom serwer

```bash
# Terminal 1: Uruchom serwer (HTTP)
uv run examples/mcpserver/robot_educational.py

# Serwer uruchomi się na: http://localhost:8000/mcp
```

### Krok 2: Uruchom Inspector

```bash
# Terminal 2: Uruchom Inspector
npx -y @modelcontextprotocol/inspector

# Inspector uruchomi się w przeglądarce
```

### Krok 3: Połącz się z serwerem

1. W Inspector otwórz się strona w przeglądarce
2. Wpisz adres serwera: `http://localhost:8000/mcp`
3. Kliknij "Connect"

### Krok 4: Testuj funkcje

**Resources:**
- Kliknij "Resources"
- Wybierz zasób (np. `robot://joints/all`)
- Zobacz wynik

**Tools:**
- Kliknij "Tools"
- Wybierz narzędzie (np. `move_joint_to`)
- Wypełnij parametry: `joint_name: "shoulder_pitch"`, `position: 1.5`
- Kliknij "Call Tool"
- Zobacz wynik

**Prompts:**
- Kliknij "Prompts"
- Wybierz prompt (np. `diagnose_robot`)
- Zobacz instrukcje

---

## 💡 Wskazówki dla studentów

### 1. Zacznij od prostych przykładów

```
simple_echo.py
    ↓
robot_educational.py
    ↓
weather_structured.py
    ↓
Własny projekt!
```

### 2. Modyfikuj przykłady

Najlepszy sposób nauki to modyfikacja:
- Dodaj nowe narzędzie do `simple_echo.py`
- Dodaj nowy staw do `robot_educational.py`
- Zmień strukturę danych w `weather_structured.py`

### 3. Używaj Inspector do debugowania

Inspector pokazuje:
- ✅ Jakie narzędzia są dostępne
- ✅ Jakie parametry przyjmują
- ✅ Jakie zwracają wyniki
- ✅ Czy są błędy

### 4. Czytaj komentarze w kodzie

Przykłady zawierają szczegółowe komentarze wyjaśniające:
- **PO CO** dana konstrukcja
- **JAK** działa mechanizm
- **KIEDY** użyć wzorca
- **PRZYKŁADY** zastosowania

### 5. Eksperymentuj bezpiecznie

Wszystkie przykłady to symulatory - możesz:
- ✅ Zmieniać kod bez obaw
- ✅ Testować różne scenariusze
- ✅ Popełniać błędy i się uczyć
- ✅ Uruchamiać wiele razy

---

## 🎓 Ścieżka nauki dla projektu z robotem

### Tydzień 1: Podstawy MCP
- [ ] Przeczytaj [README_PL.md](../../README_PL.md)
- [ ] Uruchom `simple_echo.py`
- [ ] Przetestuj z Inspector
- [ ] Dodaj własne narzędzie

### Tydzień 2: Robot Simulator
- [ ] Przeczytaj [PRZEWODNIK_STUDENTA.md](../../PRZEWODNIK_STUDENTA.md)
- [ ] Uruchom `robot_educational.py`
- [ ] Zrozum Resources, Tools, Prompts
- [ ] Dodaj nowy staw do symulatora

### Tydzień 3: Strukturowane dane
- [ ] Uruchom `weather_structured.py`
- [ ] Dodaj Pydantic model do robota
- [ ] Zwracaj strukturowane dane z Tools

### Tydzień 4: Integracja z robotem
- [ ] Przeczytaj [UNITREE_G1_PRZEWODNIK.md](../../UNITREE_G1_PRZEWODNIK.md)
- [ ] Zamień symulator na SDK Unitree G1
- [ ] Przetestuj bezpieczne ruchy
- [ ] Zaimplementuj diagnostykę

---

## 📖 Dokumentacja dodatkowa

### Dokumenty polskojęzyczne:
- [README_PL.md](../../README_PL.md) - Przegląd MCP po polsku
- [PRZEWODNIK_STUDENTA.md](../../PRZEWODNIK_STUDENTA.md) - Szczegółowy przewodnik
- [UNITREE_G1_PRZEWODNIK.md](../../UNITREE_G1_PRZEWODNIK.md) - Przewodnik Unitree G1

### Dokumentacja angielska:
- [README.md](../../README.md) - Główna dokumentacja
- [Specyfikacja MCP](https://modelcontextprotocol.io/specification/latest)
- [API Reference](https://modelcontextprotocol.github.io/python-sdk/)

---

## ❓ FAQ - Najczęstsze pytania

### Q: Który przykład uruchomić pierwszy?
**A:** `mcpserver/simple_echo.py` - najprostszy możliwy przykład.

### Q: Jak testować przykłady bez Inspector?
**A:** Większość przykładów ma wbudowane testy. Uruchom z `--help` aby zobaczyć opcje.

### Q: Czy mogę używać tych przykładów w projekcie?
**A:** TAK! Wszystkie przykłady są MIT licensed - możesz je kopiować i modyfikować.

### Q: Przykład nie działa - co robić?
**A:** 
1. Sprawdź czy masz zainstalowane `uv` i `mcp`
2. Uruchom z katalogu głównego repozytorium
3. Sprawdź logi błędów
4. Porównaj z oryginalnym kodem

### Q: Jak dodać przykład do MCP Inspector?
**A:**
1. Uruchom serwer z transportem HTTP
2. Uruchom Inspector
3. Podaj URL: `http://localhost:8000/mcp`

---

## 🎉 Podsumowanie

**Masz dostęp do:**
- ✅ 10+ gotowych przykładów
- ✅ Pełne polskie komentarze w kluczowych plikach
- ✅ Przykłady dla robotyki
- ✅ Wzorce dla różnych poziomów zaawansowania

**Następne kroki:**
1. Uruchom `simple_echo.py`
2. Przetestuj `robot_educational.py`
3. Przeczytaj przewodniki
4. Zacznij własny projekt!

**Powodzenia! 🚀🤖**

---

*Dokument przygotowany dla studentów Politechniki Rzeszowskiej*  
*Wersja: 1.0 - Luty 2025*
