# Tutorial MCP Python SDK - Po polsku
## Od zera do działającego serwera w 30 minut

---

## 🎯 Cel tego tutoriala

Po przejściu tego tutoriala będziesz w stanie:
- ✅ Zainstalować MCP Python SDK
- ✅ Stworzyć pierwszy serwer MCP
- ✅ Dodać Resources, Tools i Prompts
- ✅ Przetestować serwer z MCP Inspector
- ✅ Zintegrować z projektem robotycznym

**Czas:** ~30 minut  
**Poziom:** Początkujący  
**Wymagania:** Podstawowa znajomość Python

---

## 📋 Spis treści

1. [Instalacja](#1-instalacja)
2. [Pierwszy serwer - Hello World](#2-pierwszy-serwer---hello-world)
3. [Dodawanie Resources](#3-dodawanie-resources)
4. [Dodawanie Tools](#4-dodawanie-tools)
5. [Dodawanie Prompts](#5-dodawanie-prompts)
6. [Context i Lifespan](#6-context-i-lifespan)
7. [Testowanie z Inspector](#7-testowanie-z-inspector)
8. [Zastosowanie w robotyce](#8-zastosowanie-w-robotyce)

---

## 1. Instalacja

### Krok 1.1: Instalacja uv (jeśli nie masz)

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Krok 1.2: Utworzenie projektu

```bash
# Utwórz nowy projekt
uv init moj-pierwszy-mcp-server
cd moj-pierwszy-mcp-server

# Dodaj MCP do projektu
uv add "mcp[cli]"
```

### Krok 1.3: Sprawdzenie instalacji

```bash
# Sprawdź czy MCP jest zainstalowane
uv run python -c "import mcp; print(f'MCP {mcp.__version__} zainstalowane!')"
```

**Oczekiwany wynik:**
```
MCP 2.x.x zainstalowane!
```

---

## 2. Pierwszy serwer - Hello World

### Krok 2.1: Utwórz plik serwera

Utwórz plik `server.py`:

```python
"""Mój pierwszy serwer MCP!"""

from mcp.server.mcpserver import MCPServer

# Utworzenie serwera
mcp = MCPServer("Mój Pierwszy Serwer")


# Pierwsze narzędzie
@mcp.tool()
def hello(name: str) -> str:
    """Przywitaj się z użytkownikiem"""
    return f"Cześć {name}! Witaj w świecie MCP! 🎉"


# Uruchomienie serwera
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000, json_response=True)
```

### Krok 2.2: Uruchom serwer

```bash
uv run server.py
```

**Oczekiwany wynik:**
```
Serwer MCP działa na http://localhost:8000/mcp
```

### Krok 2.3: Przetestuj (w nowym terminalu)

```bash
# Uruchom Inspector
npx -y @modelcontextprotocol/inspector
```

W przeglądarce:
1. Połącz się z `http://localhost:8000/mcp`
2. Kliknij "Tools"
3. Wybierz `hello`
4. Wpisz parametr: `name: "Jan"`
5. Kliknij "Call Tool"

**Wynik:** `"Cześć Jan! Witaj w świecie MCP! 🎉"`

🎉 **Gratulacje!** Właśnie uruchomiłeś pierwszy serwer MCP!

---

## 3. Dodawanie Resources

Resources to **dane do odczytu**. Dodajmy odczyt konfiguracji.

### Krok 3.1: Rozszerz server.py

```python
"""Mój pierwszy serwer MCP z Resources"""

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Mój Pierwszy Serwer")


# TOOLS (jak poprzednio)
@mcp.tool()
def hello(name: str) -> str:
    """Przywitaj się z użytkownikiem"""
    return f"Cześć {name}! Witaj w świecie MCP! 🎉"


# RESOURCES (NOWOŚĆ!) - odczyt danych
@mcp.resource("config://app/settings")
def get_app_settings() -> str:
    """Pobierz ustawienia aplikacji"""
    return """
    {
        "app_name": "Mój Serwer MCP",
        "version": "1.0.0",
        "language": "pl",
        "debug": true
    }
    """


@mcp.resource("config://app/status")
def get_app_status() -> str:
    """Pobierz status aplikacji"""
    return """
    Status: ✅ Działa
    Uptime: 5 minut
    Requests: 42
    """


# Uruchomienie
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000, json_response=True)
```

### Krok 3.2: Przetestuj Resources

1. Uruchom serwer: `uv run server.py`
2. W Inspector → kliknij "Resources"
3. Zobaczysz:
   - `config://app/settings`
   - `config://app/status`
4. Kliknij na każdy - zobaczysz dane

**Różnica Tool vs Resource:**
- **Resource** = GET (odczyt danych, bez efektów ubocznych)
- **Tool** = POST (akcje, mogą zmieniać stan)

---

## 4. Dodawanie Tools

Tools to **akcje**. Dodajmy kalkulator.

### Krok 4.1: Rozszerz server.py

```python
"""Mój pierwszy serwer MCP z Tools"""

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Mój Pierwszy Serwer")


# TOOLS
@mcp.tool()
def hello(name: str) -> str:
    """Przywitaj się z użytkownikiem"""
    return f"Cześć {name}! Witaj w świecie MCP! 🎉"


@mcp.tool()
def dodaj(a: int, b: int) -> int:
    """Dodaj dwie liczby"""
    return a + b


@mcp.tool()
def odejmij(a: int, b: int) -> int:
    """Odejmij b od a"""
    return a - b


@mcp.tool()
def pomnoz(a: int, b: int) -> int:
    """Pomnóż dwie liczby"""
    return a * b


# RESOURCES
@mcp.resource("config://app/settings")
def get_app_settings() -> str:
    """Pobierz ustawienia aplikacji"""
    return """
    {
        "app_name": "Mój Serwer MCP",
        "version": "1.0.0",
        "features": ["calculator", "greeter"]
    }
    """


# Uruchomienie
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000, json_response=True)
```

### Krok 4.2: Przetestuj Tools

1. Uruchom: `uv run server.py`
2. Inspector → "Tools"
3. Przetestuj:
   - `dodaj(a=5, b=3)` → wynik: 8
   - `pomnoz(a=4, b=7)` → wynik: 28

---

## 5. Dodawanie Prompts

Prompts to **szablony instrukcji dla AI**.

### Krok 5.1: Rozszerz server.py

```python
"""Mój pierwszy serwer MCP z Prompts"""

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Mój Pierwszy Serwer")


# TOOLS
@mcp.tool()
def hello(name: str) -> str:
    """Przywitaj się z użytkownikiem"""
    return f"Cześć {name}! Witaj w świecie MCP! 🎉"


@mcp.tool()
def dodaj(a: int, b: int) -> int:
    """Dodaj dwie liczby"""
    return a + b


# PROMPTS (NOWOŚĆ!)
@mcp.prompt()
def analiza_matematyczna(liczby: str) -> str:
    """Szablon do analizy liczb"""
    return f"""
Przeprowadź analizę matematyczną liczb: {liczby}

Wykonaj następujące kroki:
1. Sprawdź czy liczby są dodatnie czy ujemne
2. Oblicz sumę używając narzędzia 'dodaj'
3. Znajdź największą i najmniejszą liczbę
4. Podaj średnią arytmetyczną
5. Wygeneruj podsumowanie w formacie:

   📊 Analiza liczb {liczby}:
   - Suma: [wynik]
   - Największa: [liczba]
   - Najmniejsza: [liczba]
   - Średnia: [wynik]
"""


@mcp.prompt()
def powitanie_formalne(osoba: str, tytul: str = "Pan/Pani") -> str:
    """Szablon do formalnego powitania"""
    return f"""
Wygeneruj formalne powitanie dla osoby:
- Imię: {osoba}
- Tytuł: {tytul}

Powitanie powinno być:
- Formalne i profesjonalne
- W języku polskim
- Uwzględniać porę dnia
- Zawierać zwrot grzecznościowy
"""


# RESOURCES
@mcp.resource("config://app/settings")
def get_app_settings() -> str:
    """Pobierz ustawienia aplikacji"""
    return """{"app_name": "Mój Serwer MCP", "version": "1.0.0"}"""


# Uruchomienie
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000, json_response=True)
```

### Krok 5.2: Przetestuj Prompts

1. Uruchom: `uv run server.py`
2. Inspector → "Prompts"
3. Wybierz `analiza_matematyczna`
4. Parametr: `liczby: "5, 10, 3, 8"`
5. Zobacz wygenerowane instrukcje dla AI

**Użycie Promptu:**
- AI czyta instrukcje z promptu
- AI wykonuje kroki (np. wywołuje narzędzie `dodaj`)
- AI generuje raport według szablonu

---

## 6. Context i Lifespan

Context i Lifespan służą do **zarządzania zasobami** (np. połączeniami).

### Krok 6.1: Stwórz serwer z bazą danych (symulacja)

```python
"""Serwer MCP z Context i Lifespan"""

from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from mcp.server.mcpserver import Context, MCPServer
from mcp.server.session import ServerSession


# KROK 1: Symulacja bazy danych
class Database:
    """Symulowana baza danych"""
    
    def __init__(self):
        self.data = {
            "users": ["Anna", "Jan", "Maria"],
            "products": ["Laptop", "Mysz", "Klawiatura"],
        }
        self.connected = False
    
    async def connect(self):
        """Połącz z bazą"""
        print("📊 Łączę z bazą danych...")
        self.connected = True
        print("✅ Połączono z bazą")
    
    async def disconnect(self):
        """Rozłącz z bazą"""
        print("🔌 Rozłączam z bazą danych...")
        self.connected = False
        print("✅ Rozłączono")
    
    def get_users(self):
        """Pobierz użytkowników"""
        return self.data["users"]
    
    def add_user(self, name: str):
        """Dodaj użytkownika"""
        self.data["users"].append(name)
        return f"Dodano użytkownika: {name}"


# KROK 2: Definicja kontekstu
@dataclass
class AppContext:
    """Kontekst aplikacji z bazą danych"""
    db: Database


# KROK 3: Funkcja lifespan
@asynccontextmanager
async def app_lifespan(server: MCPServer) -> AsyncIterator[AppContext]:
    """Zarządzaj cyklem życia bazy danych"""
    # STARTUP - wykonane RAZ przy starcie
    db = Database()
    await db.connect()
    
    try:
        # DZIAŁANIE - przekazanie kontekstu
        yield AppContext(db=db)
    finally:
        # SHUTDOWN - wykonane RAZ przy zamykaniu
        await db.disconnect()


# KROK 4: Utworzenie serwera z lifespan
mcp = MCPServer("Serwer z Bazą Danych", lifespan=app_lifespan)


# KROK 5: Tools używające kontekstu
@mcp.tool()
def lista_uzytkownikow(ctx: Context[ServerSession, AppContext]) -> str:
    """Pobierz listę użytkowników z bazy"""
    # Dostęp do bazy przez kontekst
    db = ctx.request_context.lifespan_context.db
    
    users = db.get_users()
    return f"Użytkownicy: {', '.join(users)}"


@mcp.tool()
async def dodaj_uzytkownika(
    name: str,
    ctx: Context[ServerSession, AppContext]
) -> str:
    """Dodaj użytkownika do bazy"""
    db = ctx.request_context.lifespan_context.db
    
    # Logowanie
    await ctx.info(f"Dodaję użytkownika: {name}")
    
    result = db.add_user(name)
    
    await ctx.info("Użytkownik dodany pomyślnie")
    return result


# Uruchomienie
if __name__ == "__main__":
    print("""
╔════════════════════════════════════════╗
║   Serwer MCP z Context i Lifespan      ║
╚════════════════════════════════════════╝
    """)
    mcp.run(transport="streamable-http", port=8000, json_response=True)
```

### Krok 6.2: Przetestuj Context

1. Uruchom: `uv run server.py`
2. Zobacz w konsoli:
   ```
   📊 Łączę z bazą danych...
   ✅ Połączono z bazą
   ```
3. Inspector → Tools:
   - `lista_uzytkownikow()` → Zobacz użytkowników
   - `dodaj_uzytkownika(name="Piotr")` → Dodaj użytkownika
   - `lista_uzytkownikow()` → Zobacz zaktualizowaną listę
4. Zatrzymaj serwer (Ctrl+C):
   ```
   🔌 Rozłączam z bazą danych...
   ✅ Rozłączono
   ```

**Dlaczego to ważne?**
- ✅ Jedno połączenie współdzielone przez wszystkie narzędzia
- ✅ Automatyczne czyszczenie przy zamykaniu
- ✅ Type-safe dostęp do zasobów

---

## 7. Testowanie z Inspector

### Krok 7.1: Przygotowanie

```bash
# Terminal 1: Uruchom serwer
uv run server.py

# Terminal 2: Uruchom Inspector
npx -y @modelcontextprotocol/inspector
```

### Krok 7.2: Połączenie

1. W przeglądarce otwórz Inspector
2. Wpisz URL: `http://localhost:8000/mcp`
3. Kliknij "Connect"

### Krok 7.3: Eksploracja

**Resources:**
- Kliknij "Resources" → Zobacz listę zasobów
- Kliknij na zasób → Zobacz dane

**Tools:**
- Kliknij "Tools" → Zobacz listę narzędzi
- Wybierz narzędzie → Wypełnij parametry → "Call Tool"

**Prompts:**
- Kliknij "Prompts" → Zobacz szablony
- Wybierz prompt → Wypełnij parametry → Zobacz instrukcje

### Krok 7.4: Debugowanie

Inspector pokazuje:
- ✅ Jakie narzędzia są dostępne
- ✅ Schematy parametrów (typy, opisy)
- ✅ Wyniki wywołań
- ✅ Błędy (jeśli wystąpią)

**Wskazówka:** Gdy coś nie działa, Inspector pokaże dokładny komunikat błędu!

---

## 8. Zastosowanie w robotyce

### Krok 8.1: Struktura serwera dla robota

```python
"""Szablon serwera MCP dla robota"""

from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Dict

from mcp.server.mcpserver import Context, MCPServer
from mcp.server.session import ServerSession


# KROK 1: Interfejs do robota (zastąp SDK prawdziwego robota)
class RobotInterface:
    """Interfejs do komunikacji z robotem"""
    
    def __init__(self, robot_ip: str):
        self.robot_ip = robot_ip
        self.connected = False
        # Stan stawów (przykład)
        self.joint_positions = {
            "shoulder": 0.0,
            "elbow": 0.0,
            "wrist": 0.0,
        }
    
    async def connect(self):
        """Połącz z robotem"""
        print(f"🤖 Łączę z robotem: {self.robot_ip}")
        # W prawdziwym projekcie: await robot_sdk.connect()
        self.connected = True
        print("✅ Połączono z robotem")
    
    async def disconnect(self):
        """Rozłącz z robotem"""
        print("🔌 Rozłączam z robotem")
        # W prawdziwym projekcie: await robot_sdk.disconnect()
        self.connected = False
        print("✅ Rozłączono")
    
    def get_joint_position(self, joint_name: str) -> float:
        """Pobierz pozycję stawu"""
        return self.joint_positions.get(joint_name, 0.0)
    
    def move_joint(self, joint_name: str, position: float):
        """Przesuń staw"""
        if joint_name not in self.joint_positions:
            raise ValueError(f"Nieznany staw: {joint_name}")
        
        # Sprawdzenie limitów (BEZPIECZEŃSTWO!)
        if abs(position) > 3.14:
            raise ValueError(f"Pozycja poza zakresem: {position}")
        
        # Wykonanie ruchu (symulacja)
        self.joint_positions[joint_name] = position
        return f"Przesunięto {joint_name} do {position:.2f} rad"
    
    def emergency_stop(self):
        """STOP AWARYJNY"""
        print("🚨 STOP AWARYJNY")
        for joint in self.joint_positions:
            self.joint_positions[joint] = 0.0


# KROK 2: Kontekst z robotem
@dataclass
class RobotContext:
    robot: RobotInterface


@asynccontextmanager
async def robot_lifespan(server: MCPServer) -> AsyncIterator[RobotContext]:
    """Zarządzaj połączeniem z robotem"""
    robot = RobotInterface(robot_ip="192.168.1.100")
    await robot.connect()
    
    try:
        yield RobotContext(robot=robot)
    finally:
        await robot.disconnect()


# KROK 3: Serwer MCP
mcp = MCPServer("Robot Controller", lifespan=robot_lifespan)


# KROK 4: Resources - odczyt stanu
@mcp.resource("robot://joints/{joint_name}")
def get_joint(joint_name: str, ctx: Context[ServerSession, RobotContext]) -> str:
    """Pobierz pozycję stawu"""
    robot = ctx.request_context.lifespan_context.robot
    position = robot.get_joint_position(joint_name)
    return f"Staw {joint_name}: {position:.3f} rad"


# KROK 5: Tools - sterowanie
@mcp.tool()
async def move_joint(
    joint_name: str,
    position: float,
    ctx: Context[ServerSession, RobotContext]
) -> str:
    """Przesuń staw robota"""
    robot = ctx.request_context.lifespan_context.robot
    
    await ctx.info(f"Przesuwam {joint_name} do {position:.2f}")
    
    try:
        result = robot.move_joint(joint_name, position)
        await ctx.info("Ruch wykonany")
        return f"✅ {result}"
    except ValueError as e:
        await ctx.error(f"Błąd: {e}")
        return f"❌ {e}"


@mcp.tool()
async def emergency_stop(ctx: Context[ServerSession, RobotContext]) -> str:
    """STOP AWARYJNY"""
    robot = ctx.request_context.lifespan_context.robot
    
    await ctx.info("🚨 WYKONUJĘ STOP AWARYJNY")
    robot.emergency_stop()
    
    return "✅ Robot zatrzymany"


# KROK 6: Prompts - diagnostyka
@mcp.prompt()
def check_robot_status() -> str:
    """Szablon diagnostyki robota"""
    return """
Sprawdź stan robota:

1. Odczytaj pozycje wszystkich stawów:
   - robot://joints/shoulder
   - robot://joints/elbow
   - robot://joints/wrist

2. Sprawdź czy pozycje są w normie (|p| < 3.0 rad)

3. Wygeneruj raport:
   🤖 Status Robota:
   - Shoulder: [pozycja] - [status]
   - Elbow: [pozycja] - [status]
   - Wrist: [pozycja] - [status]
   
   Ogólny stan: [OK/UWAGA]
"""


# Uruchomienie
if __name__ == "__main__":
    print("""
╔════════════════════════════════════════╗
║        Robot MCP Controller            ║
╚════════════════════════════════════════╝
    """)
    mcp.run(transport="streamable-http", port=8000, json_response=True)
```

### Krok 8.2: Użycie w projekcie z Unitree G1

**Zamień symulator na prawdziwy SDK:**

```python
# Zamiast RobotInterface użyj SDK Unitree G1
from unitree_sdk import UnitreeG1, JointCommand

class RobotInterface:
    def __init__(self, robot_ip: str):
        self.robot = UnitreeG1(ip=robot_ip)
    
    async def connect(self):
        await self.robot.connect()
    
    def get_joint_position(self, joint_name: str):
        return self.robot.get_joint_state(joint_name).position
    
    def move_joint(self, joint_name: str, position: float):
        command = JointCommand(
            name=joint_name,
            position=position,
            max_velocity=1.0
        )
        self.robot.send_command(command)
```

---

## 🎉 Podsumowanie

**Ukończyłeś tutorial!** Teraz potrafisz:

✅ Instalować MCP Python SDK  
✅ Tworzyć serwery MCP  
✅ Dodawać Resources (dane)  
✅ Dodawać Tools (akcje)  
✅ Dodawać Prompts (szablony)  
✅ Używać Context i Lifespan  
✅ Testować z Inspector  
✅ Tworzyć serwery dla robotów

**Następne kroki:**

1. **Przeczytaj przewodniki:**
   - [README_PL.md](../README_PL.md)
   - [PRZEWODNIK_STUDENTA.md](../PRZEWODNIK_STUDENTA.md)
   - [UNITREE_G1_PRZEWODNIK.md](../UNITREE_G1_PRZEWODNIK.md)

2. **Przejrzyj przykłady:**
   - [examples/README_PL.md](../examples/README_PL.md)
   - [examples/mcpserver/robot_educational.py](../examples/mcpserver/robot_educational.py)

3. **Zacznij własny projekt:**
   - Zidentyfikuj potrzeby (jakie dane? jakie akcje?)
   - Zaprojektuj interfejs (Resources, Tools, Prompts)
   - Implementuj krok po kroku
   - Testuj z Inspector

**Powodzenia! 🚀🤖**

---

*Tutorial przygotowany dla studentów Politechniki Rzeszowskiej*  
*Wersja: 1.0 - Luty 2025*
