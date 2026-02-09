# Przewodnik Studenta - MCP Python SDK
## Politechnika Rzeszowska - Projekt Robot Humanoidalny

---

## 📚 Wprowadzenie

Witaj w przewodniku po MCP Python SDK przygotowanym specjalnie dla studentów Politechniki Rzeszowskiej pracujących nad projektami z robotem humanoidalnym **Unitree G1 EDU-U6**.

### Cele tego przewodnika:

1. ✅ Zrozumienie **czym jest MCP** i **po co jest potrzebne**
2. ✅ Nauka **tworzenia serwerów MCP** krok po kroku
3. ✅ Praktyczne **zastosowanie w projektach robotycznych**
4. ✅ **Gotowe przykłady** do użycia w swoich projektach

---

## 🎯 Czym jest MCP i po co to wszystko?

### Problem bez MCP

Wyobraź sobie, że tworzysz projekt z robotem:
- Masz **model AI** (np. ChatGPT, Claude), który ma pomóc w sterowaniu robotem
- Model AI potrzebuje **dostępu do danych robota** (sensory, pozycja, stan)
- Model AI musi **wykonywać akcje** (ruch, chwytanie, planowanie)

**Jak to zrobić?** Możesz:
1. ❌ Pisać własny protokół komunikacji (dużo pracy, błędy, brak standaryzacji)
2. ❌ Kopiować dane ręcznie do promptów (niepraktyczne, wolne)
3. ✅ **Użyć MCP** - gotowego, ustandaryzowanego rozwiązania!

### Rozwiązanie: MCP

**Model Context Protocol (MCP)** to **standardowy sposób** komunikacji między:
- **Aplikacjami** (Twój kod robota) ↔️ **Modele AI** (GPT, Claude, inne)

**Korzyści:**
- 🔧 **Gotowa infrastruktura** - nie piszesz wszystkiego od zera
- 🔒 **Bezpieczeństwo** - kontrolowany dostęp do funkcji robota
- 📦 **Modularność** - łatwo dodawać nowe funkcje
- 🌐 **Standaryzacja** - działa z wieloma systemami AI

---

## 🏗️ Architektura MCP - Jak to działa?

```
┌─────────────────────────────────────────────────────────────┐
│                      MODEL AI (Klient)                      │
│                   (ChatGPT, Claude, etc.)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ MCP Protocol
                         │ (JSON-RPC over HTTP/stdio/SSE)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    SERWER MCP (Twój kod)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              MCPServer Framework                     │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Resources │  Tools    │  Prompts  │  Sampling      │  │
│  │  (dane)    │  (akcje)  │ (szablony)│  (AI queries)  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Twoje funkcje
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   ROBOT UNITREE G1                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Sensory    │  │   Aktuatory  │  │    Kamery    │     │
│  │   (IMU, FT)  │  │   (silniki)  │  │   (wizja)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Kluczowe komponenty:

1. **Resources (Zasoby)** - DANE z robota
   - Przykład: pozycja stawów, odczyty sensorów, stan baterii

2. **Tools (Narzędzia)** - AKCJE dla robota
   - Przykład: porusz stawem, chwyt obiekt, wykonaj ruch

3. **Prompts (Szablony)** - WZORCE komunikacji
   - Przykład: "przeanalizuj dane z sensora X", "zaplanuj ruch do punktu Y"

---

## 📖 Podstawy - Pierwszy serwer MCP

### Krok 1: Instalacja

```bash
# Utwórz nowy projekt
uv init moj-robot-server
cd moj-robot-server

# Dodaj MCP do projektu
uv add "mcp[cli]"
```

### Krok 2: Najprostszy serwer (`hello_mcp.py`)

```python
"""
Najprostszy możliwy serwer MCP.
Ten przykład pokazuje MINIMALNE wymagania do utworzenia działającego serwera.
"""

# Import głównej klasy serwera MCP
from mcp.server.mcpserver import MCPServer

# KROK 1: Tworzenie instancji serwera
# Parametr "Hello Server" to nazwa serwera widoczna dla klientów MCP
mcp = MCPServer("Hello Server")


# KROK 2: Definicja pierwszego narzędzia
# Dekorator @mcp.tool() REJESTRUJE funkcję jako narzędzie dostępne dla AI
@mcp.tool()
def hello(name: str) -> str:
    """Przywitaj się z użytkownikiem.
    
    Args:
        name: Imię osoby do powitania
    
    Returns:
        Wiadomość powitalna
    
    WAŻNE ZASADY:
    - Docstring opisuje CO robi funkcja (AI to widzi!)
    - Typy parametrów (str) są WYMAGANE - służą do walidacji
    - Zwracany typ też powinien być określony
    """
    return f"Cześć {name}! Witaj w świecie MCP!"


# KROK 3: Uruchomienie serwera (tylko gdy uruchamiamy bezpośrednio)
if __name__ == "__main__":
    # Transport "streamable-http" - serwer dostępny przez HTTP
    # Port domyślny: 8000
    # json_response=True - odpowiedzi w formacie JSON (czytelniejsze)
    mcp.run(transport="streamable-http", json_response=True)
```

### Krok 3: Uruchomienie

```bash
# Uruchom serwer
uv run hello_mcp.py

# Serwer jest dostępny na: http://localhost:8000/mcp
```

### Krok 4: Test z MCP Inspector

```bash
# W NOWYM terminalu uruchom Inspector
npx -y @modelcontextprotocol/inspector

# W przeglądarce połącz się z: http://localhost:8000/mcp
# Przetestuj narzędzie 'hello' z parametrem name="Jan"
```

**Co się dzieje?**
1. Inspector wysyła żądanie JSON-RPC do serwera MCP
2. Serwer wywołuje funkcję `hello("Jan")`
3. Funkcja zwraca "Cześć Jan! Witaj w świecie MCP!"
4. Inspector pokazuje wynik

---

## 🤖 Przykład robotyczny - Prosty robot

### Scenariusz: Symulator podstawowego robota

Stwórzmy serwer MCP dla prostego symulatora robota z:
- Odczytem pozycji (Resource)
- Sterowaniem ruchem (Tool)
- Szablonem diagnostycznym (Prompt)

```python
"""
Serwer MCP dla prostego symulatora robota.
Ten przykład pokazuje PRAKTYCZNE użycie MCP w robotyce.

Plik: robot_simulator.py
"""

from dataclasses import dataclass
from typing import Dict, List
from mcp.server.mcpserver import Context, MCPServer
from mcp.server.session import ServerSession


# ============================================================================
# SEKCJA 1: MODEL DANYCH ROBOTA
# ============================================================================

@dataclass
class JointState:
    """Stan pojedynczego stawu robota.
    
    Atrybuty:
        name: Nazwa stawu (np. "shoulder_pitch", "elbow_roll")
        position: Pozycja w radianach
        velocity: Prędkość w rad/s
        torque: Moment obrotowy w Nm
    """
    name: str
    position: float  # radiany
    velocity: float  # rad/s
    torque: float    # Nm


class RobotSimulator:
    """Prosty symulator robota.
    
    Symuluje robota z kilkoma stawami. W prawdziwym projekcie
    tutaj byłoby połączenie z rzeczywistym robotem Unitree G1.
    """
    
    def __init__(self):
        """Inicjalizacja symulatora z domyślnymi wartościami."""
        # Słownik przechowujący stan każdego stawu
        self.joints: Dict[str, JointState] = {
            "shoulder_pitch": JointState("shoulder_pitch", 0.0, 0.0, 0.0),
            "shoulder_roll": JointState("shoulder_roll", 0.0, 0.0, 0.0),
            "elbow_pitch": JointState("elbow_pitch", 0.0, 0.0, 0.0),
        }
        
        # Status robota
        self.is_moving = False
        self.battery_level = 100.0  # procent
    
    def get_joint_state(self, joint_name: str) -> JointState:
        """Pobierz stan konkretnego stawu.
        
        Args:
            joint_name: Nazwa stawu
            
        Returns:
            Stan stawu
            
        Raises:
            ValueError: Jeśli staw nie istnieje
        """
        if joint_name not in self.joints:
            raise ValueError(f"Nieznany staw: {joint_name}")
        return self.joints[joint_name]
    
    def get_all_joints(self) -> List[JointState]:
        """Pobierz stan wszystkich stawów."""
        return list(self.joints.values())
    
    def move_joint(self, joint_name: str, target_position: float) -> str:
        """Przesuń staw do docelowej pozycji.
        
        Args:
            joint_name: Nazwa stawu
            target_position: Docelowa pozycja w radianach
            
        Returns:
            Komunikat o sukcesie
            
        UWAGA: To symulacja! W prawdziwym robocie tutaj byłby:
        - Sprawdzenie limitów ruchu
        - Planowanie trajektorii
        - Wysłanie komend do kontrolera silnika
        - Monitorowanie wykonania
        """
        if joint_name not in self.joints:
            raise ValueError(f"Nieznany staw: {joint_name}")
        
        # Walidacja zakresu (dla bezpieczeństwa!)
        if abs(target_position) > 3.14:  # ±180 stopni
            raise ValueError(f"Pozycja poza zakresem: {target_position}")
        
        # Aktualizacja stanu (symulacja)
        self.joints[joint_name].position = target_position
        self.is_moving = True
        
        return f"Staw {joint_name} przesunięty do {target_position:.2f} rad"
    
    def get_battery_status(self) -> float:
        """Pobierz stan baterii."""
        return self.battery_level


# ============================================================================
# SEKCJA 2: SERWER MCP Z INTEGRACJĄ SYMULATORA
# ============================================================================

# Globalna instancja symulatora
# W prawdziwym projekcie to byłby singleton lub dependency injection
robot = RobotSimulator()

# Tworzenie serwera MCP
mcp = MCPServer("Robot Simulator Server")


# ----------------------------------------------------------------------------
# Resources - Zasoby do odczytu danych
# ----------------------------------------------------------------------------

@mcp.resource("robot://joints/all")
def get_all_joints_resource() -> str:
    """Pobierz stan wszystkich stawów robota.
    
    URI: robot://joints/all
    
    Ten zasób pozwala AI odczytać AKTUALNY stan wszystkich stawów.
    Zwraca dane w formacie JSON dla łatwej analizy.
    """
    joints = robot.get_all_joints()
    
    # Formatowanie do JSON
    result = "Stan wszystkich stawów:\n"
    for joint in joints:
        result += f"- {joint.name}:\n"
        result += f"  Pozycja: {joint.position:.3f} rad\n"
        result += f"  Prędkość: {joint.velocity:.3f} rad/s\n"
        result += f"  Moment: {joint.torque:.3f} Nm\n"
    
    return result


@mcp.resource("robot://joints/{joint_name}")
def get_joint_resource(joint_name: str) -> str:
    """Pobierz stan konkretnego stawu.
    
    URI: robot://joints/shoulder_pitch
    
    Args:
        joint_name: Nazwa stawu (z URI)
    
    Przykład użycia przez AI:
    "Odczytaj zasób robot://joints/shoulder_pitch"
    """
    try:
        joint = robot.get_joint_state(joint_name)
        return f"""Staw: {joint.name}
Pozycja: {joint.position:.3f} rad
Prędkość: {joint.velocity:.3f} rad/s  
Moment: {joint.torque:.3f} Nm"""
    except ValueError as e:
        return f"Błąd: {e}"


@mcp.resource("robot://status/battery")
def get_battery_resource() -> str:
    """Pobierz stan baterii.
    
    URI: robot://status/battery
    """
    battery = robot.get_battery_status()
    return f"Stan baterii: {battery:.1f}%"


# ----------------------------------------------------------------------------
# Tools - Narzędzia do wykonywania akcji
# ----------------------------------------------------------------------------

@mcp.tool()
def move_joint_to(joint_name: str, position: float) -> str:
    """Przesuń staw do określonej pozycji.
    
    Args:
        joint_name: Nazwa stawu (shoulder_pitch, shoulder_roll, elbow_pitch)
        position: Docelowa pozycja w radianach (-3.14 do 3.14)
    
    Returns:
        Komunikat o sukcesie lub błędzie
    
    BEZPIECZEŃSTWO:
    - Sprawdzamy zakres ruchu
    - Walidujemy nazwę stawu
    - W prawdziwym robocie: sprawdzilibyśmy kolizje, limity prędkości, etc.
    """
    try:
        result = robot.move_joint(joint_name, position)
        return result
    except ValueError as e:
        return f"Błąd: {e}"


@mcp.tool()
async def emergency_stop(ctx: Context[ServerSession, None]) -> str:
    """STOP AWARYJNY - natychmiastowe zatrzymanie robota.
    
    To narzędzie powinno być ZAWSZE dostępne dla bezpieczeństwa!
    
    Args:
        ctx: Kontekst MCP (automatycznie wstrzykiwany)
    
    W prawdziwym robocie:
    - Zatrzymanie wszystkich silników
    - Zwolnienie wszystkich chwytaków
    - Zapis logu zdarzenia
    - Powiadomienie operatora
    """
    # Logowanie zdarzenia STOP
    await ctx.info("🚨 WYKONANO STOP AWARYJNY")
    
    # Zatrzymanie robota (symulacja)
    robot.is_moving = False
    for joint in robot.joints.values():
        joint.velocity = 0.0
        joint.torque = 0.0
    
    await ctx.info("Robot zatrzymany bezpiecznie")
    return "✅ Robot zatrzymany - wszystkie ruchy wstrzymane"


@mcp.tool()
async def move_sequence(
    positions: List[float],
    ctx: Context[ServerSession, None]
) -> str:
    """Wykonaj sekwencję ruchów z raportowaniem postępu.
    
    Args:
        positions: Lista pozycji dla stawu shoulder_pitch
        ctx: Kontekst MCP
    
    Ten przykład pokazuje jak:
    - Wykonywać wielokrokowe operacje
    - Raportować postęp do AI
    - Obsługiwać błędy w sekwencji
    """
    await ctx.info(f"Rozpoczynam sekwencję {len(positions)} ruchów")
    
    for i, pos in enumerate(positions):
        # Raportowanie postępu
        progress = (i + 1) / len(positions)
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Ruch {i + 1}/{len(positions)}: {pos:.2f} rad"
        )
        
        # Wykonanie ruchu
        try:
            robot.move_joint("shoulder_pitch", pos)
            await ctx.debug(f"Ukończono ruch {i + 1}")
        except ValueError as e:
            await ctx.error(f"Błąd w ruchu {i + 1}: {e}")
            return f"❌ Sekwencja przerwana na ruchu {i + 1}: {e}"
    
    await ctx.info("Sekwencja zakończona pomyślnie")
    return f"✅ Wykonano {len(positions)} ruchów"


# ----------------------------------------------------------------------------
# Prompts - Szablony do interakcji z AI
# ----------------------------------------------------------------------------

@mcp.prompt()
def diagnose_robot(component: str = "all") -> str:
    """Szablon do diagnostyki robota.
    
    Args:
        component: Komponent do sprawdzenia (all/joints/battery/status)
    
    Ten prompt instruuje AI jak przeprowadzić diagnostykę robota.
    AI użyje dostępnych Resources i Tools do zebrania informacji.
    """
    prompts = {
        "all": """Przeprowadź pełną diagnostykę robota:
1. Sprawdź stan baterii (robot://status/battery)
2. Odczytaj pozycje wszystkich stawów (robot://joints/all)
3. Sprawdź czy wszystkie wartości są w normie
4. Wygeneruj raport diagnostyczny w formacie:
   - Stan baterii: OK/UWAGA/KRYTYCZNY
   - Stan stawów: lista z oceną każdego
   - Rekomendacje (jeśli są problemy)""",
        
        "joints": """Sprawdź stan stawów robota:
1. Odczytaj wszystkie stawy
2. Sprawdź czy pozycje są w bezpiecznym zakresie
3. Oceń czy moment obrotowy jest w normie
4. Zgłoś nieprawidłowości""",
        
        "battery": """Sprawdź stan baterii:
1. Odczytaj poziom baterii
2. Oceń czy wystarczy na planowane operacje
3. Zasugeruj ładowanie jeśli < 20%""",
    }
    
    return prompts.get(component, prompts["all"])


# ============================================================================
# SEKCJA 3: URUCHOMIENIE SERWERA
# ============================================================================

if __name__ == "__main__":
    # Uruchomienie serwera na porcie 8000
    # Serwer będzie dostępny pod adresem: http://localhost:8000/mcp
    
    print("🤖 Uruchamianie serwera MCP Robot Simulator...")
    print("📡 Serwer dostępny na: http://localhost:8000/mcp")
    print("🔧 Dostępne narzędzia:")
    print("   - move_joint_to: Przesuń staw")
    print("   - emergency_stop: Stop awaryjny")
    print("   - move_sequence: Sekwencja ruchów")
    print("📊 Dostępne zasoby:")
    print("   - robot://joints/all: Wszystkie stawy")
    print("   - robot://joints/{name}: Konkretny staw")
    print("   - robot://status/battery: Stan baterii")
    
    mcp.run(transport="streamable-http", port=8000, json_response=True)
```

### Jak używać tego serwera?

```bash
# Terminal 1: Uruchom serwer
uv run robot_simulator.py

# Terminal 2: Uruchom Inspector
npx -y @modelcontextprotocol/inspector
# Połącz się z: http://localhost:8000/mcp
```

### Przykładowe interakcje z AI:

**Przykład 1: Odczyt stanu**
```
AI: "Sprawdź stan baterii"
→ Odczyt zasobu: robot://status/battery
→ Wynik: "Stan baterii: 100.0%"
```

**Przykład 2: Wykonanie ruchu**
```
AI: "Przesuń staw shoulder_pitch do pozycji 1.5 radiana"
→ Wywołanie: move_joint_to("shoulder_pitch", 1.5)
→ Wynik: "Staw shoulder_pitch przesunięty do 1.50 rad"
```

**Przykład 3: Diagnostyka**
```
AI: "Użyj promptu diagnose_robot z parametrem all"
→ AI wykonuje kroki z promptu:
  1. Sprawdza baterię
  2. Odczytuje stawy
  3. Generuje raport
```

---

## 🎓 Dobre praktyki w projektach robotycznych

### 1. **Bezpieczeństwo przede wszystkim**

```python
@mcp.tool()
def move_robot(position: float) -> str:
    """ZAWSZE sprawdzaj limity przed ruchem!"""
    
    # ✅ Sprawdzenie zakresu
    MIN_POS, MAX_POS = -3.14, 3.14
    if not (MIN_POS <= position <= MAX_POS):
        return f"❌ Pozycja {position} poza zakresem [{MIN_POS}, {MAX_POS}]"
    
    # ✅ Sprawdzenie kolizji (w prawdziwym robocie)
    # if check_collision(position):
    #     return "❌ Ruch spowodowałby kolizję"
    
    # ✅ Dopiero teraz wykonaj ruch
    execute_motion(position)
    return f"✅ Ruch wykonany: {position}"
```

### 2. **Dokładne docstringi**

```python
@mcp.tool()
def grasp_object(force: float, object_id: str) -> str:
    """Chwyć obiekt z określoną siłą.
    
    Args:
        force: Siła chwytu w Newtonach (0.0 - 100.0)
               ⚠️ Siła > 50N może uszkodzić delikatne obiekty
        object_id: Identyfikator obiektu z systemu wizji
    
    Returns:
        Status operacji (success/failure)
    
    Raises:
        ValueError: Jeśli siła poza zakresem
        RuntimeError: Jeśli obiekt nie został wykryty
    
    Example:
        >>> grasp_object(force=25.0, object_id="cup_01")
        "✅ Obiekt cup_01 schwytany z siłą 25.0N"
    """
    # Implementacja...
```

### 3. **Logowanie i monitoring**

```python
@mcp.tool()
async def complex_task(ctx: Context[ServerSession, None]) -> str:
    """Używaj ctx do logowania WSZYSTKIEGO!"""
    
    # ℹ️ Info - ważne zdarzenia
    await ctx.info("Rozpoczynam złożone zadanie")
    
    try:
        # 🐛 Debug - szczegóły techniczne
        await ctx.debug(f"Parametry: {params}")
        
        # 📊 Progress - postęp długich operacji
        await ctx.report_progress(0.5, 1.0, "Połowa wykonana")
        
        # ⚠️ Warning - ostrzeżenia (nie używane bezpośrednio, użyj ctx.info)
        await ctx.info("⚠️ Wykryto potencjalny problem")
        
        return "✅ Sukces"
        
    except Exception as e:
        # ❌ Error - błędy
        await ctx.error(f"Wystąpił błąd: {e}")
        raise
```

### 4. **Struktura projektu**

```
moj-robot-projekt/
├── pyproject.toml          # Konfiguracja projektu (uv)
├── README.md               # Dokumentacja projektu
├── .gitignore              # Co ignorować w git
│
├── src/
│   ├── robot/
│   │   ├── __init__.py
│   │   ├── simulator.py    # Symulator robota
│   │   ├── controller.py   # Kontroler ruchu
│   │   └── sensors.py      # Obsługa sensorów
│   │
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py       # Główny serwer MCP
│       ├── resources.py    # Definicje Resources
│       ├── tools.py        # Definicje Tools
│       └── prompts.py      # Definicje Prompts
│
├── tests/
│   ├── test_simulator.py
│   ├── test_controller.py
│   └── test_mcp_server.py
│
└── examples/
    ├── basic_movement.py
    ├── vision_integration.py
    └── trajectory_planning.py
```

---

## 📝 Ćwiczenia dla studentów

### Ćwiczenie 1: Rozszerzenie symulatora (łatwe)

Dodaj do `robot_simulator.py`:
1. Nowy zasób: `robot://status/temperature` (temperatura silników)
2. Nowe narzędzie: `set_speed(speed: float)` (ustawienie prędkości ruchu)
3. Nowy prompt: `check_safety()` (sprawdzenie bezpieczeństwa)

### Ćwiczenie 2: Integracja z wizją (średnie)

Stwórz nowy serwer MCP do systemu wizji:
```python
@mcp.resource("vision://detected_objects")
def get_detected_objects() -> str:
    """Zwróć listę wykrytych obiektów"""
    # Twoja implementacja

@mcp.tool()
def track_object(object_id: str) -> str:
    """Śledź obiekt kamerą"""
    # Twoja implementacja
```

### Ćwiczenie 3: Planowanie trajektorii (trudne)

Stwórz narzędzie do planowania trajektorii:
```python
@mcp.tool()
async def plan_trajectory(
    start: List[float],
    goal: List[float],
    ctx: Context[ServerSession, None]
) -> str:
    """Zaplanuj trajektorię między dwoma punktami.
    
    Użyj:
    - await ctx.report_progress() do pokazania postępu
    - Algorytmu planowania (np. RRT, A*)
    - Sprawdzenia kolizji
    """
    # Twoja implementacja
```

---

## 🔗 Przydatne zasoby

### Dokumentacja:
- [MCP Python SDK - README_PL.md](./README_PL.md) - Polski przegląd
- [MCP Specification](https://modelcontextprotocol.io/specification/latest) - Pełna specyfikacja
- [Python Type Hints](https://docs.python.org/3/library/typing.html) - Adnotacje typów

### Narzędzia:
- [uv](https://docs.astral.sh/uv/) - Zarządzanie projektami Python
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - Testowanie serwerów MCP
- [Pydantic](https://docs.pydantic.dev/) - Walidacja danych

### Przykłady:
- [examples/](./examples/) - Oficjalne przykłady w repozytorium
- [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md) - Przewodnik Unitree G1

---

## ❓ Najczęściej zadawane pytania (FAQ)

### Q: Czy muszę znać TypeScript/JavaScript?
**A:** NIE! Ten SDK jest w 100% Pythonowy. Niektóre narzędzia testowe (Inspector) używają Node.js, ale to tylko do testowania.

### Q: Czy MCP działa z prawdziwym robotem Unitree G1?
**A:** TAK! Zobacz [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md) dla szczegółów integracji.

### Q: Jak debugować serwer MCP?
**A:** 
1. Użyj `await ctx.debug()` w narzędziach
2. Sprawdź logi serwera w terminalu
3. Użyj MCP Inspector do testowania
4. Dodaj `print()` do debugowania (tymczasowo)

### Q: Czy mogę użyć async/await?
**A:** TAK! MCP w pełni wspiera async:
```python
@mcp.tool()
async def async_tool(ctx: Context[ServerSession, None]) -> str:
    await ctx.info("To jest async!")
    result = await some_async_operation()
    return result
```

### Q: Jak obsługiwać błędy?
**A:**
```python
@mcp.tool()
async def safe_tool(ctx: Context[ServerSession, None]) -> str:
    try:
        # Niebezpieczna operacja
        result = risky_operation()
        return f"✅ Sukces: {result}"
    except ValueError as e:
        await ctx.error(f"Błąd walidacji: {e}")
        return f"❌ Błąd: {e}"
    except Exception as e:
        await ctx.error(f"Nieoczekiwany błąd: {e}")
        return "❌ Wystąpił nieoczekiwany błąd"
```

---

## 🎉 Podsumowanie

Teraz wiesz:
- ✅ **Czym jest MCP** i po co służy
- ✅ **Jak tworzyć serwery MCP** krok po kroku
- ✅ **Jak używać Resources, Tools i Prompts**
- ✅ **Jak zastosować MCP w robotyce**
- ✅ **Dobre praktyki** i wzorce projektowe

**Następny krok:** Przeczytaj [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md) aby dowiedzieć się jak zintegrować MCP z robotem Unitree G1!

---

**Powodzenia w projekcie! 🚀🤖**

*Ten przewodnik został przygotowany specjalnie dla studentów Politechniki Rzeszowskiej. W razie pytań, sprawdź dokumentację lub skonsultuj się z prowadzącym.*
