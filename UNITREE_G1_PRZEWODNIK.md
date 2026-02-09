# Przewodnik MCP dla Robota Unitree G1 EDU-U6
## Praktyczne zastosowanie w projektach robotycznych

---

## 🤖 O robocie Unitree G1 EDU-U6

**Unitree G1** to zaawansowany humanoidalny robot edukacyjny wyposażony w:

### Specyfikacja techniczna:
- **23 lub 29 stopni swobody** (zależnie od wersji)
- **Wysokość:** ~127 cm
- **Waga:** ~35 kg
- **Procesor:** ARM-based computing unit
- **Sensory:**
  - IMU (Inertial Measurement Unit) - orientacja i przyspieszenie
  - Czujniki siły i momentu (Force/Torque sensors) w stopach
  - Kamery RGB (opcjonalnie głębia)
  - Enkodery w stawach
- **Komunikacja:** Ethernet, WiFi, USB
- **SDK:** Python/C++ API do kontroli

### Możliwości:
- ✅ Chodzenie i bieganie
- ✅ Manipulacja obiektami (jeśli wyposażony w chwytaki)
- ✅ Rozpoznawanie obiektów (z integracją wizji)
- ✅ Interakcja człowiek-robot
- ✅ Uczenie ze wzmocnieniem

---

## 🎯 Po co MCP dla Unitree G1?

### Problem bez MCP:

Typowy projekt z robotem wymaga:
1. Pisania kodu niskopoziomowego (kontrola silników)
2. Przetwarzania danych z sensorów
3. Planowania trajektorii
4. Integracji z AI/LLM dla zadań wysokopoziomowych
5. Debugowania i monitoringu

**Każdy z tych elementów wymaga osobnej implementacji.**

### Rozwiązanie z MCP:

MCP tworzy **jednolity interfejs** łączący:
- 🤖 Robot (hardware + niskopoziomowe API)
- 🧠 AI/LLM (wysokopoziomowe planowanie)
- 👨‍💻 Deweloper (debugging, monitoring)

```
┌─────────────────────────────────────────────────────────┐
│            AI/LLM (ChatGPT, Claude, etc.)               │
│     "Podnieś obiekt z podłogi i połóż go na stole"      │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
                     │ (wysokopoziomowe komendy)
┌────────────────────▼────────────────────────────────────┐
│                 SERWER MCP (Twój kod)                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Resources    │  Tools       │  Prompts          │  │
│  │  - odczyty    │  - sterowanie│  - szablony AI    │  │
│  │  - stan       │  - wizja     │  - diagnostyka    │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ Unitree SDK
                     │ (niskopoziomowe API)
┌────────────────────▼────────────────────────────────────┐
│                  UNITREE G1 ROBOT                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │  IMU    │  │ Kamery  │  │ Stawy   │  │  F/T    │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Architektura systemu MCP dla G1

### Warstwa 1: Niskopoziomowa komunikacja z robotem

```python
"""
unitree_interface.py - Warstwa komunikacji z robotem

Ta klasa ENKAPSULUJE niskopoziomowe API Unitree.
Zapewnia prosty, bezpieczny interfejs do kontroli robota.
"""

from typing import List, Dict, Optional
import numpy as np

# Import z Unitree SDK (przykład - dokładne API zależy od wersji)
# from unitree_sdk import Robot, JointMode, MotorCommand


class UnitreeG1Interface:
    """Interfejs do komunikacji z robotem Unitree G1.
    
    Ta klasa UKRYWA szczegóły implementacji Unitree SDK
    i zapewnia prosty, bezpieczny API.
    """
    
    # Definicja stawów robota G1 (przykład - dostosuj do rzeczywistej konfiguracji)
    JOINT_NAMES = [
        # Lewa noga
        "l_hip_pitch", "l_hip_roll", "l_hip_yaw",
        "l_knee", "l_ankle_pitch", "l_ankle_roll",
        # Prawa noga
        "r_hip_pitch", "r_hip_roll", "r_hip_yaw", 
        "r_knee", "r_ankle_pitch", "r_ankle_roll",
        # Tułów
        "waist_yaw", "waist_pitch", "waist_roll",
        # Lewe ramię
        "l_shoulder_pitch", "l_shoulder_roll", "l_shoulder_yaw",
        "l_elbow",
        # Prawe ramię
        "r_shoulder_pitch", "r_shoulder_roll", "r_shoulder_yaw",
        "r_elbow",
    ]
    
    # Limity bezpieczeństwa (radiany)
    JOINT_LIMITS = {
        "l_hip_pitch": (-1.57, 1.57),
        "l_hip_roll": (-0.79, 0.79),
        # ... (pełna lista dla wszystkich stawów)
    }
    
    def __init__(self, robot_ip: str = "192.168.123.10"):
        """Inicjalizacja połączenia z robotem.
        
        Args:
            robot_ip: Adres IP robota (domyślny dla Unitree G1)
        """
        self.robot_ip = robot_ip
        self.connected = False
        
        # W prawdziwej implementacji:
        # self.robot = Robot(robot_ip)
        # self.robot.connect()
        
        # Symulacja dla przykładu
        self.joint_positions = {name: 0.0 for name in self.JOINT_NAMES}
        self.joint_velocities = {name: 0.0 for name in self.JOINT_NAMES}
        self.joint_torques = {name: 0.0 for name in self.JOINT_NAMES}
        
        # Stan IMU
        self.imu_orientation = np.array([0.0, 0.0, 0.0])  # roll, pitch, yaw
        self.imu_angular_vel = np.array([0.0, 0.0, 0.0])
        self.imu_linear_acc = np.array([0.0, 0.0, 9.81])  # grawitacja
        
        # Stan czujników siły
        self.left_foot_force = np.array([0.0, 0.0, 0.0])
        self.right_foot_force = np.array([0.0, 0.0, 0.0])
    
    def connect(self) -> bool:
        """Nawiąż połączenie z robotem."""
        try:
            # W prawdziwej implementacji:
            # self.robot.connect()
            # self.connected = self.robot.is_connected()
            
            # Symulacja
            self.connected = True
            print(f"✅ Połączono z robotem: {self.robot_ip}")
            return True
        except Exception as e:
            print(f"❌ Błąd połączenia: {e}")
            return False
    
    def disconnect(self) -> None:
        """Rozłącz się z robotem."""
        # W prawdziwej implementacji:
        # self.robot.disconnect()
        self.connected = False
        print("🔌 Rozłączono z robotem")
    
    def get_joint_state(self, joint_name: str) -> Dict[str, float]:
        """Pobierz stan pojedynczego stawu.
        
        Args:
            joint_name: Nazwa stawu
            
        Returns:
            Słownik z pozycją, prędkością i momentem
        """
        if joint_name not in self.JOINT_NAMES:
            raise ValueError(f"Nieznany staw: {joint_name}")
        
        # W prawdziwej implementacji:
        # state = self.robot.get_joint_state(joint_name)
        
        return {
            "position": self.joint_positions[joint_name],
            "velocity": self.joint_velocities[joint_name],
            "torque": self.joint_torques[joint_name],
        }
    
    def get_all_joint_states(self) -> Dict[str, Dict[str, float]]:
        """Pobierz stan wszystkich stawów."""
        return {
            name: self.get_joint_state(name)
            for name in self.JOINT_NAMES
        }
    
    def set_joint_position(
        self,
        joint_name: str,
        position: float,
        max_velocity: float = 1.0
    ) -> bool:
        """Ustaw docelową pozycję stawu.
        
        Args:
            joint_name: Nazwa stawu
            position: Docelowa pozycja (radiany)
            max_velocity: Maksymalna prędkość ruchu (rad/s)
            
        Returns:
            True jeśli komenda wysłana pomyślnie
        
        BEZPIECZEŃSTWO:
        - Sprawdzamy limity ruchu
        - Ograniczamy prędkość
        - W prawdziwym robocie: sprawdzamy kolizje
        """
        if joint_name not in self.JOINT_NAMES:
            raise ValueError(f"Nieznany staw: {joint_name}")
        
        # Sprawdzenie limitów
        if joint_name in self.JOINT_LIMITS:
            min_pos, max_pos = self.JOINT_LIMITS[joint_name]
            if not (min_pos <= position <= max_pos):
                raise ValueError(
                    f"Pozycja {position:.2f} poza zakresem "
                    f"[{min_pos:.2f}, {max_pos:.2f}] dla {joint_name}"
                )
        
        # W prawdziwej implementacji:
        # command = MotorCommand(
        #     mode=JointMode.POSITION,
        #     position=position,
        #     max_velocity=max_velocity
        # )
        # self.robot.send_command(joint_name, command)
        
        # Symulacja
        self.joint_positions[joint_name] = position
        return True
    
    def get_imu_data(self) -> Dict[str, np.ndarray]:
        """Pobierz dane z IMU.
        
        Returns:
            Słownik z orientacją, prędkością kątową i przyspieszeniem
        """
        # W prawdziwej implementacji:
        # imu_data = self.robot.get_imu_data()
        
        return {
            "orientation": self.imu_orientation,      # [roll, pitch, yaw] w radianach
            "angular_velocity": self.imu_angular_vel, # [wx, wy, wz] w rad/s
            "linear_acceleration": self.imu_linear_acc # [ax, ay, az] w m/s²
        }
    
    def get_foot_forces(self) -> Dict[str, np.ndarray]:
        """Pobierz siły w stopach.
        
        Returns:
            Słownik z siłami dla lewej i prawej stopy
        """
        # W prawdziwej implementacji:
        # forces = self.robot.get_foot_sensors()
        
        return {
            "left": self.left_foot_force,   # [Fx, Fy, Fz] w N
            "right": self.right_foot_force, # [Fx, Fy, Fz] w N
        }
    
    def emergency_stop(self) -> None:
        """STOP AWARYJNY - natychmiastowe zatrzymanie robota.
        
        KRYTYCZNE DLA BEZPIECZEŃSTWA!
        - Zeruje prędkości wszystkich stawów
        - Przełącza w tryb wysokiej impedancji (soft)
        - Zatrzymuje wszystkie komendy ruchu
        """
        print("🚨 WYKONUJĘ STOP AWARYJNY")
        
        # W prawdziwej implementacji:
        # self.robot.emergency_stop()
        
        # Symulacja
        for name in self.JOINT_NAMES:
            self.joint_velocities[name] = 0.0
            self.joint_torques[name] = 0.0
        
        print("✅ Robot zatrzymany")
```

### Warstwa 2: Serwer MCP integrujący z robotem

```python
"""
g1_mcp_server.py - Serwer MCP dla Unitree G1

Ten serwer ŁĄCZY niskopoziomowe API robota z protokołem MCP,
umożliwiając kontrolę robota przez AI/LLM.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from mcp.server.mcpserver import Context, MCPServer
from mcp.server.session import ServerSession

# Import naszego interfejsu do robota
from unitree_interface import UnitreeG1Interface


# ============================================================================
# KONTEKST APLIKACJI - przechowuje połączenie z robotem
# ============================================================================

@dataclass
class G1AppContext:
    """Kontekst aplikacji z połączeniem do robota."""
    robot: UnitreeG1Interface


@asynccontextmanager
async def app_lifespan(server: MCPServer) -> AsyncIterator[G1AppContext]:
    """Zarządza cyklem życia połączenia z robotem.
    
    WYWOŁANE:
    - RAZ przy starcie serwera (inicjalizacja)
    - RAZ przy zamykaniu (cleanup)
    
    WAŻNE:
    - Inicjalizujemy połączenie z robotem przy starcie
    - Bezpiecznie zamykamy przy końcu
    - Obsługujemy błędy połączenia
    """
    print("🔧 Inicjalizacja połączenia z robotem Unitree G1...")
    
    # Tworzenie interfejsu do robota
    robot = UnitreeG1Interface(robot_ip="192.168.123.10")
    
    # Próba połączenia
    if not robot.connect():
        raise RuntimeError("Nie można połączyć się z robotem!")
    
    print("✅ Połączono z robotem G1")
    
    try:
        # Przekazanie kontekstu do wszystkich narzędzi
        yield G1AppContext(robot=robot)
    finally:
        # Bezpieczne zamknięcie przy wyjściu
        print("🔌 Zamykanie połączenia z robotem...")
        robot.disconnect()
        print("✅ Połączenie zamknięte")


# ============================================================================
# SERWER MCP
# ============================================================================

mcp = MCPServer("Unitree G1 MCP Server", lifespan=app_lifespan)


# ============================================================================
# RESOURCES - Odczyt danych z robota
# ============================================================================

@mcp.resource("g1://joints/all")
def get_all_joints(ctx: Context[ServerSession, G1AppContext]) -> str:
    """Pobierz stan wszystkich stawów robota.
    
    URI: g1://joints/all
    
    Zwraca kompletny stan wszystkich 23 stawów w formacie czytelnym dla AI.
    """
    robot = ctx.request_context.lifespan_context.robot
    
    # Pobranie stanu wszystkich stawów
    states = robot.get_all_joint_states()
    
    # Formatowanie dla AI
    result = "=== STAN WSZYSTKICH STAWÓW UNITREE G1 ===\n\n"
    
    # Grupowanie stawów według części ciała
    groups = {
        "Lewa noga": ["l_hip_pitch", "l_hip_roll", "l_hip_yaw", "l_knee", "l_ankle_pitch", "l_ankle_roll"],
        "Prawa noga": ["r_hip_pitch", "r_hip_roll", "r_hip_yaw", "r_knee", "r_ankle_pitch", "r_ankle_roll"],
        "Lewe ramię": ["l_shoulder_pitch", "l_shoulder_roll", "l_shoulder_yaw", "l_elbow"],
        "Prawe ramię": ["r_shoulder_pitch", "r_shoulder_roll", "r_shoulder_yaw", "r_elbow"],
    }
    
    for group_name, joints in groups.items():
        result += f"📍 {group_name}:\n"
        for joint_name in joints:
            if joint_name in states:
                state = states[joint_name]
                result += f"  • {joint_name}:\n"
                result += f"    Pozycja: {state['position']:.3f} rad ({np.rad2deg(state['position']):.1f}°)\n"
                result += f"    Prędkość: {state['velocity']:.3f} rad/s\n"
                result += f"    Moment: {state['torque']:.2f} Nm\n"
        result += "\n"
    
    return result


@mcp.resource("g1://joints/{joint_name}")
def get_joint(joint_name: str, ctx: Context[ServerSession, G1AppContext]) -> str:
    """Pobierz stan pojedynczego stawu.
    
    URI: g1://joints/l_hip_pitch
    
    Args:
        joint_name: Nazwa stawu (z URI)
    """
    robot = ctx.request_context.lifespan_context.robot
    
    try:
        state = robot.get_joint_state(joint_name)
        
        return f"""📍 Staw: {joint_name}
Pozycja: {state['position']:.3f} rad ({np.rad2deg(state['position']):.1f}°)
Prędkość: {state['velocity']:.3f} rad/s
Moment: {state['torque']:.2f} Nm"""
        
    except ValueError as e:
        return f"❌ Błąd: {e}"


@mcp.resource("g1://sensors/imu")
def get_imu(ctx: Context[ServerSession, G1AppContext]) -> str:
    """Pobierz dane z IMU (Inertial Measurement Unit).
    
    URI: g1://sensors/imu
    
    IMU dostarcza informacji o:
    - Orientacji robota (roll, pitch, yaw)
    - Prędkości kątowej
    - Przyspieszeniu liniowym
    """
    robot = ctx.request_context.lifespan_context.robot
    imu_data = robot.get_imu_data()
    
    roll, pitch, yaw = imu_data["orientation"]
    wx, wy, wz = imu_data["angular_velocity"]
    ax, ay, az = imu_data["linear_acceleration"]
    
    return f"""📐 DANE IMU (Inertial Measurement Unit)

Orientacja (ZYX Euler):
  Roll:  {roll:.3f} rad ({np.rad2deg(roll):.1f}°)
  Pitch: {pitch:.3f} rad ({np.rad2deg(pitch):.1f}°)
  Yaw:   {yaw:.3f} rad ({np.rad2deg(yaw):.1f}°)

Prędkość kątowa:
  ωx: {wx:.3f} rad/s
  ωy: {wy:.3f} rad/s
  ωz: {wz:.3f} rad/s

Przyspieszenie liniowe:
  ax: {ax:.2f} m/s²
  ay: {ay:.2f} m/s²
  az: {az:.2f} m/s²
"""


@mcp.resource("g1://sensors/feet")
def get_foot_forces(ctx: Context[ServerSession, G1AppContext]) -> str:
    """Pobierz siły w stopach.
    
    URI: g1://sensors/feet
    
    Czujniki siły w stopach mierzą:
    - Siłę kontaktu z podłożem
    - Rozkład obciążenia (lewa/prawa noga)
    - Stan równowagi
    """
    robot = ctx.request_context.lifespan_context.robot
    forces = robot.get_foot_forces()
    
    left = forces["left"]
    right = forces["right"]
    
    # Obliczenie całkowitych sił
    left_total = np.linalg.norm(left)
    right_total = np.linalg.norm(right)
    total = left_total + right_total
    
    # Rozkład obciążenia
    left_percent = (left_total / total * 100) if total > 0 else 0
    right_percent = (right_total / total * 100) if total > 0 else 0
    
    return f"""👣 SIŁY W STOPACH

Lewa stopa:
  Fx: {left[0]:.2f} N
  Fy: {left[1]:.2f} N
  Fz: {left[2]:.2f} N (pionowa)
  Całkowita: {left_total:.2f} N

Prawa stopa:
  Fx: {right[0]:.2f} N
  Fy: {right[1]:.2f} N
  Fz: {right[2]:.2f} N (pionowa)
  Całkowita: {right_total:.2f} N

Rozkład obciążenia:
  Lewa:  {left_percent:.1f}%
  Prawa: {right_percent:.1f}%
  
Stan: {'⚖️ Zrównoważony' if abs(left_percent - right_percent) < 20 else '⚠️ Niezrównoważony'}
"""


# ============================================================================
# TOOLS - Sterowanie robotem
# ============================================================================

@mcp.tool()
async def move_joint(
    joint_name: str,
    target_position: float,
    max_velocity: float = 1.0,
    ctx: Context[ServerSession, G1AppContext] = None
) -> str:
    """Przesuń pojedynczy staw do docelowej pozycji.
    
    Args:
        joint_name: Nazwa stawu (np. "l_shoulder_pitch")
        target_position: Docelowa pozycja w radianach
        max_velocity: Maksymalna prędkość ruchu w rad/s (domyślnie 1.0)
    
    Returns:
        Status operacji
    
    BEZPIECZEŃSTWO:
    ⚠️ Sprawdzane są limity ruchu przed wykonaniem
    ⚠️ Prędkość jest ograniczona do bezpiecznych wartości
    """
    robot = ctx.request_context.lifespan_context.robot
    
    await ctx.info(f"Przesuwam staw {joint_name} do {target_position:.2f} rad")
    
    try:
        # Wykonanie ruchu (z wbudowanymi sprawdzeniami bezpieczeństwa)
        success = robot.set_joint_position(joint_name, target_position, max_velocity)
        
        if success:
            await ctx.info(f"✅ Ruch wykonany pomyślnie")
            return f"✅ Staw {joint_name} przesunięty do {target_position:.2f} rad"
        else:
            await ctx.error("❌ Nie udało się wysłać komendy")
            return "❌ Błąd wysyłania komendy do robota"
            
    except ValueError as e:
        await ctx.error(f"❌ Błąd walidacji: {e}")
        return f"❌ {e}"
    except Exception as e:
        await ctx.error(f"❌ Nieoczekiwany błąd: {e}")
        return f"❌ Wystąpił błąd: {e}"


@mcp.tool()
async def move_multiple_joints(
    positions: Dict[str, float],
    max_velocity: float = 1.0,
    ctx: Context[ServerSession, G1AppContext] = None
) -> str:
    """Przesuń wiele stawów jednocześnie.
    
    Args:
        positions: Słownik {nazwa_stawu: docelowa_pozycja}
                  Przykład: {"l_shoulder_pitch": 0.5, "r_shoulder_pitch": 0.5}
        max_velocity: Maksymalna prędkość dla wszystkich stawów
    
    Returns:
        Status operacji
    
    Użycie:
    Zamiast przesuwać stawy po kolei, ta funkcja przesuwa je RÓWNOCZEŚNIE,
    co jest szybsze i bardziej naturalne dla ruchów robota.
    """
    robot = ctx.request_context.lifespan_context.robot
    
    await ctx.info(f"Przesuwam {len(positions)} stawów jednocześnie")
    
    success_count = 0
    errors = []
    
    for joint_name, position in positions.items():
        try:
            robot.set_joint_position(joint_name, position, max_velocity)
            success_count += 1
            await ctx.debug(f"✓ {joint_name} -> {position:.2f} rad")
        except Exception as e:
            error_msg = f"{joint_name}: {e}"
            errors.append(error_msg)
            await ctx.error(f"✗ {error_msg}")
    
    # Raport końcowy
    if errors:
        return f"⚠️ Przesunięto {success_count}/{len(positions)} stawów. Błędy:\n" + "\n".join(errors)
    else:
        await ctx.info(f"✅ Wszystkie stawy przesunięte pomyślnie")
        return f"✅ Przesunięto {success_count} stawów pomyślnie"


@mcp.tool()
async def emergency_stop(ctx: Context[ServerSession, G1AppContext]) -> str:
    """🚨 STOP AWARYJNY - natychmiastowe zatrzymanie robota.
    
    KRYTYCZNE DLA BEZPIECZEŃSTWA!
    
    Wywołaj to narzędzie gdy:
    - Robot wykonuje niebezpieczny ruch
    - Wykryto nieprawidłowość
    - Konieczne natychmiastowe zatrzymanie
    
    Returns:
        Potwierdzenie zatrzymania
    """
    robot = ctx.request_context.lifespan_context.robot
    
    await ctx.info("🚨🚨🚨 WYKONUJĘ STOP AWARYJNY 🚨🚨🚨")
    
    try:
        robot.emergency_stop()
        await ctx.info("✅ Robot zatrzymany bezpiecznie")
        return "✅ STOP AWARYJNY wykonany - robot zatrzymany"
    except Exception as e:
        await ctx.error(f"❌ Błąd podczas STOP: {e}")
        return f"❌ BŁĄD STOP AWARYJNEGO: {e}"


# ============================================================================
# PROMPTS - Szablony dla AI
# ============================================================================

@mcp.prompt()
def diagnose_balance() -> str:
    """Szablon diagnostyki równowagi robota.
    
    Instruuje AI jak sprawdzić czy robot jest stabilnie ustawiony.
    """
    return """Przeprowadź diagnostykę równowagi robota Unitree G1:

1. Odczytaj dane z IMU (g1://sensors/imu):
   - Sprawdź orientację (roll, pitch, yaw)
   - Wartości prawidłowe: |roll| < 5°, |pitch| < 5°

2. Odczytaj siły w stopach (g1://sensors/feet):
   - Sprawdź rozkład obciążenia
   - Wartość prawidłowa: różnica między stopami < 30%

3. Oceń stabilność:
   - STABILNY: orientacja prawidłowa + równomierny rozkład
   - NIESTABILNY: przekroczenie limitów orientacji
   - KRYTYCZNY: rozkład > 70% na jednej nodze

4. Wygeneruj raport z rekomendacjami.
"""


@mcp.prompt()
def check_joint_health() -> str:
    """Szablon diagnostyki zdrowia stawów."""
    return """Sprawdź stan techniczny stawów robota G1:

1. Odczytaj stan wszystkich stawów (g1://joints/all)

2. Dla każdego stawu sprawdź:
   - Czy pozycja jest w dopuszczalnym zakresie
   - Czy moment obrotowy nie jest nadmierny (|τ| < 50 Nm to normalnie)
   - Czy prędkość jest rozsądna (|v| < 10 rad/s w spoczynku)

3. Zidentyfikuj problemy:
   - Wysokie momenty → możliwe zablokowanie lub nadmierne obciążenie
   - Wysokie prędkości w spoczynku → możliwa niestabilność
   - Pozycje skrajne → ryzyko kolizji/uszkodzenia

4. Wygeneruj raport z listą problemów i rekomendacjami.
"""


# ============================================================================
# URUCHOMIENIE SERWERA
# ============================================================================

if __name__ == "__main__":
    import numpy as np  # Potrzebne do obliczeń
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║          UNITREE G1 MCP SERVER                               ║
║          Serwer MCP dla robota humanoidalnego                ║
╚══════════════════════════════════════════════════════════════╝

🤖 Robot: Unitree G1 EDU-U6
📡 Transport: Streamable HTTP
🌐 Adres: http://localhost:8000/mcp

📊 Dostępne zasoby (Resources):
   • g1://joints/all - Stan wszystkich stawów
   • g1://joints/{nazwa} - Stan konkretnego stawu
   • g1://sensors/imu - Dane z IMU
   • g1://sensors/feet - Siły w stopach

🔧 Dostępne narzędzia (Tools):
   • move_joint - Przesuń pojedynczy staw
   • move_multiple_joints - Przesuń wiele stawów
   • emergency_stop - 🚨 STOP AWARYJNY

📝 Dostępne szablony (Prompts):
   • diagnose_balance - Diagnostyka równowagi
   • check_joint_health - Diagnostyka zdrowia stawów

⚠️  UWAGA: Ten serwer kontroluje PRAWDZIWY robot!
    Zachowaj ostrożność podczas testowania.

Uruchamianie...
    """)
    
    mcp.run(transport="streamable-http", port=8000, json_response=True)
```

---

## 🎓 Przykłady użycia w projektach

### Projekt 1: Podstawowa diagnostyka robota

**Cel:** Stwórz system monitoringu stanu robota używający AI.

```python
# Interakcja z AI przez MCP:

AI: "Sprawdź czy robot jest stabilny"
→ AI użyje promptu: diagnose_balance
→ AI odczyta: g1://sensors/imu
→ AI odczyta: g1://sensors/feet
→ AI wygeneruje raport o stabilności

AI: "Znajdź problem jeśli robot się chwieje"
→ AI sprawdzi IMU (odchylenie orientacji)
→ AI sprawdzi siły (nierównomierny rozkład)
→ AI zasugeruje rozwiązanie (np. wyrównanie pozycji)
```

### Projekt 2: Kalibracja pozycji początkowej

**Cel:** Ustaw robota w bezpiecznej pozycji startowej.

```python
# home_position.py
"""Ustaw robota w pozycji home (bezpieczna pozycja startowa)."""

# Definicja pozycji home (przykładowe wartości)
HOME_POSITIONS = {
    # Nogi - lekko ugięte dla stabilności
    "l_hip_pitch": 0.2,
    "l_hip_roll": 0.0,
    "l_hip_yaw": 0.0,
    "l_knee": -0.4,
    "l_ankle_pitch": 0.2,
    "l_ankle_roll": 0.0,
    
    "r_hip_pitch": 0.2,
    "r_hip_roll": 0.0,
    "r_hip_yaw": 0.0,
    "r_knee": -0.4,
    "r_ankle_pitch": 0.2,
    "r_ankle_roll": 0.0,
    
    # Ramiona - wzdłuż ciała
    "l_shoulder_pitch": 0.0,
    "l_shoulder_roll": 0.0,
    "l_shoulder_yaw": 0.0,
    "l_elbow": 0.0,
    
    "r_shoulder_pitch": 0.0,
    "r_shoulder_roll": 0.0,
    "r_shoulder_yaw": 0.0,
    "r_elbow": 0.0,
}

# Użycie przez AI:
AI: "Ustaw robota w pozycji home"
→ move_multiple_joints(HOME_POSITIONS, max_velocity=0.5)
→ Wszystkie stawy przesuwają się PŁYNNIE do pozycji początkowej
```

### Projekt 3: Integracja z wizją komputerową

**Cel:** Robot identyfikuje i śledzi obiekt.

```python
# vision_integration.py - Dodatkowy serwer MCP dla wizji

from mcp.server.mcpserver import MCPServer
import cv2
import numpy as np

vision_mcp = MCPServer("Vision Server")


@vision_mcp.resource("vision://detected_objects")
def get_detected_objects() -> str:
    """Pobierz listę wykrytych obiektów.
    
    Integracja z systemem wizji (YOLO, OpenCV, etc.)
    """
    # W prawdziwej implementacji: object detection
    detected = [
        {"id": "obj_001", "class": "bottle", "position": [0.5, 0.3, 0.8], "confidence": 0.95},
        {"id": "obj_002", "class": "cup", "position": [0.6, 0.2, 0.7], "confidence": 0.88},
    ]
    
    result = "Wykryte obiekty:\n"
    for obj in detected:
        result += f"- {obj['class']} (ID: {obj['id']})\n"
        result += f"  Pozycja: {obj['position']}\n"
        result += f"  Pewność: {obj['confidence']*100:.1f}%\n"
    
    return result


@vision_mcp.tool()
def track_object(object_id: str) -> str:
    """Śledź obiekt kamerą.
    
    Args:
        object_id: ID obiektu do śledzenia
    
    W prawdziwej implementacji:
    - Oblicz kierunek do obiektu
    - Przesuń stawy głowy/kamery do śledzenia
    - Raportuj pozycję
    """
    return f"Śledzę obiekt: {object_id}"


# Użycie przez AI:
AI: "Znajdź butelkę i śledź ją"
→ AI odczyta: vision://detected_objects
→ AI znajdzie obiekt klasy "bottle"
→ AI wywoła: track_object("obj_001")
```

### Projekt 4: Planowanie i wykonanie trajektorii

**Cel:** Robot wykonuje płynny ruch z punktu A do punktu B.

```python
# trajectory_planner.py

@mcp.tool()
async def execute_trajectory(
    joint_name: str,
    waypoints: List[float],
    duration: float,
    ctx: Context[ServerSession, G1AppContext]
) -> str:
    """Wykonaj trajektorię przez sekwencję punktów.
    
    Args:
        joint_name: Staw do przesunięcia
        waypoints: Lista punktów pośrednich [p1, p2, p3, ...]
        duration: Całkowity czas trajektorii w sekundach
    
    Wykonuje płynny ruch interpolując między punktami.
    """
    robot = ctx.request_context.lifespan_context.robot
    
    await ctx.info(f"Wykonuję trajektorię: {len(waypoints)} punktów w {duration}s")
    
    import time
    
    time_per_segment = duration / (len(waypoints) - 1)
    
    for i, waypoint in enumerate(waypoints):
        # Raportowanie postępu
        progress = i / (len(waypoints) - 1)
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Punkt {i+1}/{len(waypoints)}"
        )
        
        # Ruch do punktu
        robot.set_joint_position(joint_name, waypoint)
        
        # Czekanie na zakończenie segmentu
        if i < len(waypoints) - 1:
            await asyncio.sleep(time_per_segment)
    
    await ctx.info("Trajektoria zakończona")
    return f"✅ Wykonano trajektorię przez {len(waypoints)} punktów"


# Użycie przez AI:
AI: "Przesuń ramię płynnie z pozycji 0 do 1.5 radiana przez 5 sekund"
→ execute_trajectory(
    joint_name="l_shoulder_pitch",
    waypoints=[0.0, 0.5, 1.0, 1.5],  # 4 punkty pośrednie
    duration=5.0
  )
```

---

## ⚠️ Bezpieczeństwo - NAJWAŻNIEJSZE ZASADY

### 1. Zawsze sprawdzaj limity

```python
def validate_position(joint_name: str, position: float) -> bool:
    """Sprawdź czy pozycja jest bezpieczna."""
    if joint_name not in JOINT_LIMITS:
        return False
    
    min_pos, max_pos = JOINT_LIMITS[joint_name]
    return min_pos <= position <= max_pos
```

### 2. Implementuj STOP AWARYJNY

```python
# ZAWSZE dostępne, ZAWSZE wysokie priorytety
@mcp.tool()
async def emergency_stop(ctx: Context) -> str:
    """STOP AWARYJNY musi być ZAWSZE dostępny!"""
    # ... kod stop
```

### 3. Ogranicz prędkości

```python
MAX_SAFE_VELOCITY = 2.0  # rad/s

def safe_move(joint: str, pos: float):
    # Ogranicz prędkość
    velocity = min(calculate_velocity(), MAX_SAFE_VELOCITY)
    robot.set_joint_position(joint, pos, velocity)
```

### 4. Monitoruj stan robota

```python
def check_robot_health() -> bool:
    """Sprawdź czy robot jest w dobrym stanie."""
    # Sprawdź temperatury
    # Sprawdź prądy
    # Sprawdź pozycje
    # Sprawdź stabilność
    return all_checks_ok
```

### 5. Loguj WSZYSTKO

```python
@mcp.tool()
async def critical_operation(ctx: Context) -> str:
    await ctx.info("Rozpoczynam krytyczną operację")
    await ctx.debug(f"Parametry: {params}")
    
    # ... wykonanie ...
    
    await ctx.info("Operacja zakończona pomyślnie")
```

---

## 📚 Dalsze kroki

### Zaawansowane tematy:

1. **Uczenie ze wzmocnieniem (RL)**
   - Integracja z PyTorch/TensorFlow
   - MCP jako interfejs do środowiska RL
   - Zbieranie danych treningowych

2. **Multi-robot coordination**
   - Wiele serwerów MCP (jeden na robot)
   - Synchronizacja ruchów
   - Komunikacja między robotami

3. **Autonomiczna nawigacja**
   - SLAM (Simultaneous Localization and Mapping)
   - Planowanie ścieżki
   - Unikanie przeszkód

4. **Manipulacja obiektami**
   - Kinematyka odwrotna
   - Planowanie chwytania
   - Kontrola siły

---

## 🎉 Podsumowanie

MCP dla Unitree G1 zapewnia:
- ✅ **Bezpieczny** interfejs do kontroli robota
- ✅ **Standardowy** protokół komunikacji z AI
- ✅ **Modularną** architekturę łatwą do rozszerzania
- ✅ **Praktyczne** narzędzia do projektów robotycznych

**Powodzenia w projekcie z robotem Unitree G1!** 🤖🚀

---

*Opracowano dla studentów Politechniki Rzeszowskiej*
*Wersja: 1.0 - Luty 2025*
