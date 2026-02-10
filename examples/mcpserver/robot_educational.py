"""
Przykład serwera MCP dla robota - Wersja edukacyjna
====================================================

PRZEZNACZENIE:
Ten plik pokazuje KOMPLETNY przykład serwera MCP dla prostego robota.
Zawiera wszystkie kluczowe elementy: Resources, Tools, Prompts i Context.

ADRESACI:
Studenci Politechniki Rzeszowskiej pracujący z robotem Unitree G1 EDU-U6.

STRUKTURA:
1. Symulator robota (klasa RobotSimulator)
2. Serwer MCP z integracją symulatora
3. Resources - odczyt stanu robota
4. Tools - sterowanie robotem
5. Prompts - szablony dla AI

URUCHOMIENIE:
    uv run examples/mcpserver/robot_educational.py

TESTOWANIE:
    # Terminal 1: Uruchom serwer
    uv run examples/mcpserver/robot_educational.py
    
    # Terminal 2: Testuj z Inspector
    npx -y @modelcontextprotocol/inspector
    # Połącz się z: http://localhost:8000/mcp

AUTOR: Przygotowane dla projektu robota humanoidalnego na Politechnice Rzeszowskiej
DATA: 2025
"""

# ============================================================================
# SEKCJA IMPORTÓW - Wymagane biblioteki
# ============================================================================

from dataclasses import dataclass
from typing import Dict, List
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

# Import głównej klasy serwera MCP
from mcp.server.mcpserver import Context, MCPServer
from mcp.server.session import ServerSession


# ============================================================================
# SEKCJA 1: MODEL DANYCH ROBOTA
# ============================================================================
# W tej sekcji definiujemy struktury danych opisujące stan robota.
# W prawdziwym projekcie te dane pochodziłyby z rzeczywistego robota (Unitree G1).

@dataclass
class JointState:
    """Stan pojedynczego stawu robota.
    
    ZASTOSOWANIE:
    Każdy staw robota (np. kolano, ramię) ma swój stan opisany przez:
    - Pozycję (gdzie aktualnie jest staw)
    - Prędkość (jak szybko się obraca)
    - Moment obrotowy (jaka siła działa na staw)
    
    PRZYKŁAD dla Unitree G1:
    JointState(
        name="l_shoulder_pitch",  # lewe ramię - pochylenie
        position=0.785,            # 45 stopni w radianach
        velocity=0.5,              # obraca się z prędkością 0.5 rad/s
        torque=2.3                 # działa moment 2.3 Nm
    )
    """
    name: str       # Nazwa stawu (np. "shoulder_pitch", "knee")
    position: float # Pozycja w radianach (1 rad ≈ 57.3°)
    velocity: float # Prędkość obrotowa w rad/s
    torque: float   # Moment obrotowy w Nm (Newton-metrach)


class RobotSimulator:
    """Symulator prostego robota z trzema stawami.
    
    DLACZEGO SYMULATOR?
    ====================
    Ten symulator pokazuje STRUKTURĘ kodu bez potrzeby fizycznego robota.
    W prawdziwym projekcie zamiast symulatora byłoby połączenie z SDK robota Unitree G1.
    
    ARCHITEKTURA:
    =============
    RobotSimulator ←→ MCP Server ←→ AI/LLM
         ↑                             ↑
    (Symulacja)                  (ChatGPT, Claude)
    
    W prawdziwym projekcie:
    Unitree G1 SDK ←→ MCP Server ←→ AI/LLM
    
    STAWY W SYMULATORZE:
    ====================
    - shoulder_pitch: Ramię - ruch góra/dół
    - shoulder_roll: Ramię - ruch w bok
    - elbow_pitch: Łokieć - zginanie
    
    METODY:
    =======
    - get_joint_state(name): Pobierz stan jednego stawu
    - get_all_joints(): Pobierz stan wszystkich stawów
    - move_joint(name, position): Przesuń staw do pozycji
    - get_battery_status(): Sprawdź baterię
    """
    
    def __init__(self):
        """Inicjalizacja symulatora robota.
        
        CO SIĘ DZIEJE:
        1. Tworzymy słownik ze wszystkimi stawami
        2. Każdy staw zaczyna w pozycji 0.0 (neutralnej)
        3. Ustawiamy początkowy stan baterii
        
        W PRAWDZIWYM ROBOCIE:
        Tutaj byłoby:
        - Połączenie z robotem przez Ethernet/WiFi
        - Inicjalizacja SDK Unitree
        - Sprawdzenie stanu startowego
        """
        # Słownik przechowujący stan każdego stawu
        # Klucz: nazwa stawu, Wartość: obiekt JointState
        self.joints: Dict[str, JointState] = {
            "shoulder_pitch": JointState("shoulder_pitch", 0.0, 0.0, 0.0),
            "shoulder_roll": JointState("shoulder_roll", 0.0, 0.0, 0.0),
            "elbow_pitch": JointState("elbow_pitch", 0.0, 0.0, 0.0),
        }
        
        # Status robota
        self.is_moving = False        # Czy robot się rusza?
        self.battery_level = 100.0    # Stan baterii w procentach
    
    def get_joint_state(self, joint_name: str) -> JointState:
        """Pobierz stan konkretnego stawu.
        
        Args:
            joint_name: Nazwa stawu (np. "shoulder_pitch")
            
        Returns:
            Obiekt JointState ze stanem stawu
            
        Raises:
            ValueError: Jeśli nazwa stawu nie istnieje
            
        PRZYKŁAD UŻYCIA:
            state = robot.get_joint_state("shoulder_pitch")
            print(f"Pozycja: {state.position} rad")
        """
        # Sprawdzenie czy staw istnieje w słowniku
        if joint_name not in self.joints:
            # Jeśli nie - rzuć wyjątek (błąd)
            raise ValueError(f"Nieznany staw: {joint_name}")
        
        # Zwróć stan stawu ze słownika
        return self.joints[joint_name]
    
    def get_all_joints(self) -> List[JointState]:
        """Pobierz stan WSZYSTKICH stawów jako lista.
        
        Returns:
            Lista obiektów JointState dla wszystkich stawów
            
        PRZYKŁAD UŻYCIA:
            joints = robot.get_all_joints()
            for joint in joints:
                print(f"{joint.name}: {joint.position} rad")
        """
        # dict.values() zwraca wszystkie wartości ze słownika
        # list() konwertuje je na listę
        return list(self.joints.values())
    
    def move_joint(self, joint_name: str, target_position: float) -> str:
        """Przesuń staw do określonej pozycji.
        
        BEZPIECZEŃSTWO - KRYTYCZNE!
        ============================
        W prawdziwym robocie ta funkcja MUSI:
        1. Sprawdzić limity ruchu (min/max pozycja)
        2. Sprawdzić czy ruch nie spowoduje kolizji
        3. Ograniczyć prędkość do bezpiecznej wartości
        4. Monitorować wykonanie ruchu
        5. Obsłużyć błędy (utrata połączenia, błąd silnika)
        
        Args:
            joint_name: Nazwa stawu do przesunięcia
            target_position: Docelowa pozycja w radianach
            
        Returns:
            Komunikat o sukcesie
            
        Raises:
            ValueError: Jeśli staw nie istnieje lub pozycja poza zakresem
            
        PRZYKŁAD:
            robot.move_joint("shoulder_pitch", 1.57)  # 90 stopni
        """
        # KROK 1: Walidacja - czy staw istnieje?
        if joint_name not in self.joints:
            raise ValueError(f"Nieznany staw: {joint_name}")
        
        # KROK 2: Walidacja - czy pozycja jest bezpieczna?
        # Limit ±180 stopni (±3.14 radianów)
        MAX_POSITION = 3.14  # radiany
        if abs(target_position) > MAX_POSITION:
            raise ValueError(
                f"Pozycja {target_position:.2f} rad poza zakresem "
                f"[{-MAX_POSITION:.2f}, {MAX_POSITION:.2f}]"
            )
        
        # KROK 3: Wykonanie ruchu (SYMULACJA)
        # W prawdziwym robocie:
        # - Wysłałbyś komendę do kontrolera silnika
        # - Czekałbyś na potwierdzenie
        # - Monitorowałbyś wykonanie
        self.joints[joint_name].position = target_position
        self.is_moving = True
        
        # KROK 4: Zwróć komunikat o sukcesie
        return f"✅ Staw {joint_name} przesunięty do {target_position:.2f} rad"
    
    def get_battery_status(self) -> float:
        """Pobierz stan baterii.
        
        Returns:
            Poziom baterii w procentach (0.0 - 100.0)
            
        W PRAWDZIWYM ROBOCIE:
        Dane pochodziłyby z:
        - BMS (Battery Management System)
        - Czujników napięcia
        - Monitorowania prądu
        """
        return self.battery_level


# ============================================================================
# SEKCJA 2: KONTEKST APLIKACJI - Cykl życia serwera
# ============================================================================
# Context to mechanizm do zarządzania zasobami (połączenia, bazy danych, etc.)
# które są potrzebne przez cały czas działania serwera.

@dataclass
class AppContext:
    """Kontekst aplikacji przechowujący instancję robota.
    
    DLACZEGO TO POTRZEBNE?
    ======================
    Chcemy mieć JEDNO połączenie z robotem współdzielone przez wszystkie narzędzia.
    Context zapewnia to poprzez mechanizm lifespan.
    
    ALTERNATYWY (GORSZE):
    - Zmienna globalna (niebezpieczne, trudne do testowania)
    - Tworzenie nowego połączenia w każdym narzędziu (wolne, marnowanie zasobów)
    """
    robot: RobotSimulator  # Instancja symulatora/robota


@asynccontextmanager
async def app_lifespan(server: MCPServer) -> AsyncIterator[AppContext]:
    """Zarządza cyklem życia połączenia z robotem.
    
    MECHANIZM LIFESPAN:
    ===================
    Ta funkcja jest wywoływana:
    1. RAZ przy starcie serwera (kod przed yield)
    2. RAZ przy zamykaniu serwera (kod po yield w finally)
    
    DLACZEGO async?
    ===============
    Połączenie z robotem może wymagać operacji I/O:
    - Nawiązanie połączenia sieciowego
    - Odczyt konfiguracji
    - Inicjalizacja urządzeń
    
    async pozwala na nieblokujące wykonanie tych operacji.
    
    WZORZEC:
        async def lifespan():
            # 1. INICJALIZACJA (startup)
            resource = await initialize()
            
            try:
                # 2. UDOSTĘPNIENIE (yield przekazuje context do narzędzi)
                yield Context(resource=resource)
            finally:
                # 3. CZYSZCZENIE (shutdown)
                await cleanup(resource)
    
    Args:
        server: Instancja MCPServer (dla przyszłego użycia)
        
    Yields:
        AppContext z instancją robota
    """
    # FAZA 1: STARTUP - Inicjalizacja zasobów
    print("🔧 [LIFESPAN] Inicjalizacja symulatora robota...")
    
    # Tworzenie symulatora robota
    # W prawdziwym projekcie:
    # robot = UnitreeG1Interface(ip="192.168.123.10")
    # await robot.connect()
    robot = RobotSimulator()
    
    print("✅ [LIFESPAN] Symulator robota gotowy")
    
    try:
        # FAZA 2: DZIAŁANIE - Przekazanie kontekstu
        # yield ZAWIESZA funkcję i zwraca AppContext
        # Wszystkie narzędzia mogą teraz używać tego kontekstu
        yield AppContext(robot=robot)
        
    finally:
        # FAZA 3: SHUTDOWN - Czyszczenie zasobów
        # Ten blok ZAWSZE się wykona, nawet jeśli wystąpi błąd
        print("🔌 [LIFESPAN] Zamykanie połączenia z robotem...")
        
        # W prawdziwym projekcie:
        # await robot.disconnect()
        # await robot.emergency_stop()
        
        print("✅ [LIFESPAN] Zasoby zwolnione")


# ============================================================================
# SEKCJA 3: UTWORZENIE SERWERA MCP
# ============================================================================

# Tworzenie instancji serwera MCP z funkcją lifespan
# lifespan=app_lifespan oznacza: "użyj funkcji app_lifespan do zarządzania cyklem życia"
mcp = MCPServer("Robot Educational Server", lifespan=app_lifespan)


# ============================================================================
# SEKCJA 4: RESOURCES - Odczyt danych z robota
# ============================================================================
# Resources to DANE do odczytu (GET endpoints).
# Nie powinny zmieniać stanu robota, tylko dostarczać informacji.

@mcp.resource("robot://joints/all")
def get_all_joints_resource(ctx: Context[ServerSession, AppContext]) -> str:
    """Pobierz stan wszystkich stawów robota.
    
    URI: robot://joints/all
    
    CZYM JEST URI?
    ==============
    URI (Uniform Resource Identifier) to adres zasobu w MCP.
    Podobnie jak URL w www, URI identyfikuje zasób.
    
    Format: protokół://ścieżka
    - robot:// - własny protokół (możesz wymyślić dowolny)
    - joints/all - ścieżka do zasobu
    
    PARAMETR ctx (Context):
    =======================
    ctx to obiekt automatycznie wstrzykiwany przez MCP.
    Zawiera:
    - ctx.request_context.lifespan_context.robot - nasz robot z lifespan
    - ctx.session - informacje o sesji
    - ctx.info(), ctx.debug(), ctx.error() - metody logowania
    
    Type hints:
    - Context[ServerSession, AppContext]
      ↑ Typ sesji    ↑ Typ kontekstu z lifespan
    
    Returns:
        String z formatowanym stanem wszystkich stawów
        (czytelny dla AI i człowieka)
    """
    # Pobranie instancji robota z kontekstu
    robot = ctx.request_context.lifespan_context.robot
    
    # Odczyt stanu wszystkich stawów
    joints = robot.get_all_joints()
    
    # Formatowanie dla czytelności (dla AI i człowieka)
    result = "=== STAN WSZYSTKICH STAWÓW ===\n\n"
    
    for joint in joints:
        result += f"📍 {joint.name}:\n"
        result += f"   Pozycja: {joint.position:.3f} rad\n"
        result += f"   Prędkość: {joint.velocity:.3f} rad/s\n"
        result += f"   Moment: {joint.torque:.2f} Nm\n"
        result += "\n"
    
    return result


@mcp.resource("robot://joints/{joint_name}")
def get_joint_resource(joint_name: str, ctx: Context[ServerSession, AppContext]) -> str:
    """Pobierz stan konkretnego stawu.
    
    URI: robot://joints/shoulder_pitch
    
    DYNAMICZNE URI:
    ===============
    {joint_name} w URI to PARAMETR - zostanie wyekstrahowany z URI.
    
    Przykłady:
    - URI: robot://joints/shoulder_pitch → joint_name = "shoulder_pitch"
    - URI: robot://joints/elbow_pitch → joint_name = "elbow_pitch"
    
    Args:
        joint_name: Nazwa stawu (wyekstrahowana z URI)
        ctx: Kontekst MCP
        
    Returns:
        String ze stanem stawu lub komunikat o błędzie
    """
    robot = ctx.request_context.lifespan_context.robot
    
    try:
        # Próba pobrania stanu stawu
        joint = robot.get_joint_state(joint_name)
        
        # Formatowanie wyniku
        return f"""📍 Staw: {joint.name}
Pozycja: {joint.position:.3f} rad
Prędkość: {joint.velocity:.3f} rad/s
Moment: {joint.torque:.2f} Nm"""
        
    except ValueError as e:
        # Obsługa błędu - staw nie istnieje
        return f"❌ Błąd: {e}"


@mcp.resource("robot://status/battery")
def get_battery_resource(ctx: Context[ServerSession, AppContext]) -> str:
    """Pobierz stan baterii.
    
    URI: robot://status/battery
    
    ZWRACA:
    Procent naładowania baterii w czytelnym formacie.
    """
    robot = ctx.request_context.lifespan_context.robot
    battery = robot.get_battery_status()
    
    # Formatowanie z emoji dla czytelności
    if battery > 80:
        icon = "🔋"  # Pełna bateria
    elif battery > 20:
        icon = "🔋"  # Średnia bateria
    else:
        icon = "🪫"  # Niska bateria
    
    return f"{icon} Stan baterii: {battery:.1f}%"


# ============================================================================
# SEKCJA 5: TOOLS - Sterowanie robotem
# ============================================================================
# Tools to AKCJE (POST endpoints).
# Mogą zmieniać stan robota, wykonywać obliczenia, wywoływać efekty uboczne.

@mcp.tool()
async def move_joint_to(
    joint_name: str,
    position: float,
    ctx: Context[ServerSession, AppContext]
) -> str:
    """Przesuń staw robota do określonej pozycji.
    
    WAŻNE:
    ======
    To narzędzie ZMIENIA stan robota - przesuwając jego staw.
    W przeciwieństwie do Resources, Tools mogą wykonywać akcje.
    
    DLACZEGO async?
    ===============
    Funkcja jest async aby móc używać:
    - await ctx.info() - logowanie (nieblokujące)
    - await ctx.report_progress() - raportowanie postępu
    - await innych operacji I/O
    
    Args:
        joint_name: Nazwa stawu (shoulder_pitch, shoulder_roll, elbow_pitch)
        position: Docelowa pozycja w radianach (-3.14 do 3.14)
        ctx: Kontekst MCP (automatycznie wstrzykiwany)
        
    Returns:
        Komunikat o sukcesie lub błędzie
        
    PRZYKŁAD UŻYCIA PRZEZ AI:
    =========================
    AI: "Przesuń staw shoulder_pitch do pozycji 1.5 radiana"
    → Wywołanie: move_joint_to(joint_name="shoulder_pitch", position=1.5, ctx=auto)
    → Wynik: "✅ Staw shoulder_pitch przesunięty do 1.50 rad"
    
    BEZPIECZEŃSTWO:
    ===============
    Funkcja robot.move_joint() zawiera sprawdzenia:
    - Czy staw istnieje
    - Czy pozycja jest w dozwolonym zakresie
    """
    # Pobranie robota z kontekstu
    robot = ctx.request_context.lifespan_context.robot
    
    # Logowanie INFO - informacja o rozpoczęciu operacji
    await ctx.info(f"Przesuwam staw {joint_name} do {position:.2f} rad")
    
    try:
        # Wykonanie ruchu
        result = robot.move_joint(joint_name, position)
        
        # Logowanie sukcesu
        await ctx.info("Ruch wykonany pomyślnie")
        
        return result
        
    except ValueError as e:
        # Obsługa błędów walidacji
        await ctx.error(f"Błąd walidacji: {e}")
        return f"❌ {e}"


@mcp.tool()
async def emergency_stop(ctx: Context[ServerSession, AppContext]) -> str:
    """🚨 STOP AWARYJNY - natychmiastowe zatrzymanie robota.
    
    KRYTYCZNE DLA BEZPIECZEŃSTWA!
    ==============================
    To narzędzie powinno być ZAWSZE dostępne i mieć najwyższy priorytet.
    
    W prawdziwym robocie:
    - Zatrzymuje wszystkie silniki
    - Zeruje prędkości
    - Zwalnia chwytaki
    - Loguje zdarzenie
    - Powiadamia operatora
    
    Args:
        ctx: Kontekst MCP
        
    Returns:
        Potwierdzenie zatrzymania
    """
    robot = ctx.request_context.lifespan_context.robot
    
    # Logowanie KRYTYCZNEGO zdarzenia
    await ctx.info("🚨🚨🚨 WYKONUJĘ STOP AWARYJNY 🚨🚨🚨")
    
    # Zatrzymanie robota (symulacja)
    robot.is_moving = False
    for joint in robot.joints.values():
        joint.velocity = 0.0
        joint.torque = 0.0
    
    await ctx.info("Robot zatrzymany bezpiecznie")
    
    return "✅ STOP AWARYJNY wykonany - robot zatrzymany"


@mcp.tool()
async def move_sequence(
    positions: List[float],
    ctx: Context[ServerSession, AppContext]
) -> str:
    """Wykonaj sekwencję ruchów z raportowaniem postępu.
    
    ZAAWANSOWANA FUNKCJA:
    =====================
    Pokazuje jak:
    1. Wykonywać operacje wielokrokowe
    2. Raportować postęp do AI (ctx.report_progress)
    3. Obsługiwać błędy w sekwencji
    4. Logować każdy krok (ctx.debug)
    
    Args:
        positions: Lista pozycji dla stawu shoulder_pitch
                  Przykład: [0.0, 0.5, 1.0, 1.5] - 4 ruchy
        ctx: Kontekst MCP
        
    Returns:
        Podsumowanie wykonania sekwencji
        
    PRZYKŁAD:
    =========
    AI: "Wykonaj sekwencję ruchów [0, 0.5, 1.0]"
    → move_sequence(positions=[0, 0.5, 1.0], ctx=auto)
    → Robot wykona 3 ruchy z raportowaniem po każdym
    """
    robot = ctx.request_context.lifespan_context.robot
    
    # Logowanie rozpoczęcia
    await ctx.info(f"Rozpoczynam sekwencję {len(positions)} ruchów")
    
    # Wykonanie każdego ruchu w sekwencji
    for i, pos in enumerate(positions):
        # OBLICZENIE POSTĘPU
        # Postęp to liczba od 0.0 (0%) do 1.0 (100%)
        progress = (i + 1) / len(positions)
        
        # RAPORTOWANIE POSTĘPU DO AI
        # AI może pokazać pasek postępu lub informację o stanie
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Ruch {i + 1}/{len(positions)}: {pos:.2f} rad"
        )
        
        # WYKONANIE RUCHU
        try:
            robot.move_joint("shoulder_pitch", pos)
            
            # Logowanie DEBUG - szczegóły techniczne
            await ctx.debug(f"Ukończono ruch {i + 1}: {pos:.2f} rad")
            
        except ValueError as e:
            # Obsługa błędu - przerwanie sekwencji
            await ctx.error(f"Błąd w ruchu {i + 1}: {e}")
            return f"❌ Sekwencja przerwana na ruchu {i + 1}: {e}"
    
    # Logowanie zakończenia
    await ctx.info("Sekwencja zakończona pomyślnie")
    
    return f"✅ Wykonano sekwencję {len(positions)} ruchów"


# ============================================================================
# SEKCJA 6: PROMPTS - Szablony dla AI
# ============================================================================
# Prompts to szablony instrukcji dla AI.
# Definiują STANDARDOWE sposoby interakcji z robotem.

@mcp.prompt()
def diagnose_robot(component: str = "all") -> str:
    """Szablon diagnostyki robota.
    
    ZASTOSOWANIE:
    =============
    Zamiast każdorazowo pisać instrukcje dla AI, używamy gotowego szablonu.
    AI wywołuje prompt i otrzymuje szczegółowe instrukcje co zrobić.
    
    Args:
        component: Komponent do sprawdzenia (all/joints/battery)
        
    Returns:
        Instrukcje dla AI jak przeprowadzić diagnostykę
        
    PRZYKŁAD UŻYCIA:
    ================
    AI: "Użyj promptu diagnose_robot z parametrem all"
    → AI otrzymuje pełne instrukcje diagnostyczne
    → AI wykonuje kroki z instrukcji
    → AI generuje raport
    """
    templates = {
        "all": """Przeprowadź pełną diagnostykę robota:

KROK 1: Sprawdź stan baterii
- Odczytaj zasób: robot://status/battery
- Oceń czy poziom > 20% (OK) czy < 20% (KRYTYCZNY)

KROK 2: Sprawdź wszystkie stawy
- Odczytaj zasób: robot://joints/all
- Dla każdego stawu sprawdź:
  * Czy pozycja jest rozsądna (|p| < 3.14 rad)
  * Czy moment nie jest nadmierny (|τ| < 10 Nm to normalnie)

KROK 3: Wygeneruj raport
Format:
  🔋 Bateria: [poziom]% - [status]
  📍 Stawy: [liczba sprawdzonych] - [status]
  ⚠️  Uwagi: [jeśli są problemy]
  ✅ Rekomendacje: [co zrobić]
""",
        
        "joints": """Sprawdź stan stawów:

1. Odczytaj wszystkie stawy (robot://joints/all)
2. Sprawdź każdy staw:
   - Pozycja w zakresie?
   - Moment w normie?
3. Zgłoś nieprawidłowości
""",
        
        "battery": """Sprawdź baterię:

1. Odczytaj poziom (robot://status/battery)
2. Oceń:
   - > 80%: Pełna
   - 20-80%: OK
   - < 20%: UWAGA - naładuj
3. Zasugeruj działanie jeśli niska
""",
    }
    
    # Zwróć odpowiedni szablon lub domyślny
    return templates.get(component, templates["all"])


# ============================================================================
# SEKCJA 7: URUCHOMIENIE SERWERA
# ============================================================================

if __name__ == "__main__":
    # Ten blok wykonuje się TYLKO gdy uruchamiamy plik bezpośrednio
    # (nie gdy importujemy go jako moduł)
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║              ROBOT EDUCATIONAL SERVER                        ║
║          Serwer MCP do nauki robotyki z MCP                  ║
╚══════════════════════════════════════════════════════════════╝

🤖 Typ: Symulator robota edukacyjnego
📡 Transport: Streamable HTTP
🌐 Adres: http://localhost:8000/mcp

📊 Dostępne zasoby (Resources):
   • robot://joints/all - Stan wszystkich stawów
   • robot://joints/{nazwa} - Stan konkretnego stawu
   • robot://status/battery - Stan baterii

🔧 Dostępne narzędzia (Tools):
   • move_joint_to - Przesuń pojedynczy staw
   • emergency_stop - 🚨 STOP AWARYJNY
   • move_sequence - Sekwencja ruchów z postępem

📝 Dostępne szablony (Prompts):
   • diagnose_robot - Diagnostyka robota

🎓 DLA STUDENTÓW:
   Ten serwer pokazuje WSZYSTKIE elementy MCP:
   - Resources (odczyt danych)
   - Tools (wykonywanie akcji)
   - Prompts (szablony dla AI)
   - Context (zarządzanie zasobami)
   - Logowanie i raportowanie postępu

📚 DOKUMENTACJA:
   README_PL.md - Przegląd MCP po polsku
   PRZEWODNIK_STUDENTA.md - Szczegółowy przewodnik
   UNITREE_G1_PRZEWODNIK.md - Zastosowanie z Unitree G1

Uruchamianie...
    """)
    
    # Uruchomienie serwera MCP
    # - transport="streamable-http" - serwer HTTP (łatwy do testowania)
    # - port=8000 - port sieciowy
    # - json_response=True - odpowiedzi w JSON (czytelniejsze)
    mcp.run(transport="streamable-http", port=8000, json_response=True)
