# Szybki Start - MCP Python SDK dla Studentów
## 5 minut do pierwszego działającego serwera MCP

---

## ⚡ Bardzo szybko

Jeśli chcesz **natychmiast** zobaczyć MCP w akcji:

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/AI-robot-lab/mcp-python-sdk.git
cd mcp-python-sdk

# 2. Uruchom przykład
uv run examples/mcpserver/simple_echo.py

# 3. W nowym terminalu uruchom Inspector
npx -y @modelcontextprotocol/inspector
# Połącz się z: http://localhost:8000/mcp
```

🎉 **Gotowe!** Masz działający serwer MCP.

---

## 📚 Co dalej?

### Dla POCZĄTKUJĄCYCH:

**1. Przeczytaj wprowadzenie (10 min):**
- [README_PL.md](./README_PL.md) - Czym jest MCP i po co?

**2. Przejdź tutorial (30 min):**
- [docs/tutorial_pl.md](./docs/tutorial_pl.md) - Krok po kroku od zera

**3. Zbadaj prosty przykład (15 min):**
- [examples/mcpserver/simple_echo.py](./examples/mcpserver/simple_echo.py) - Komentarze po polsku

### Dla pracujących z ROBOTEM:

**1. Przeczytaj przewodnik studenta (45 min):**
- [PRZEWODNIK_STUDENTA.md](./PRZEWODNIK_STUDENTA.md) - Kompletny przewodnik MCP

**2. Przestudiuj przykład robotyczny (30 min):**
- [examples/mcpserver/robot_educational.py](./examples/mcpserver/robot_educational.py) - Serwer dla robota

**3. Zobacz integrację z Unitree G1 (30 min):**
- [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md) - Praktyczne zastosowanie

---

## 🎯 Mapa nauki

```
DZIEŃ 1: Podstawy
├── README_PL.md                    (Czym jest MCP?)
├── docs/tutorial_pl.md             (Tutorial krok po kroku)
└── examples/mcpserver/simple_echo.py   (Pierwszy kod)

DZIEŃ 2: Koncepcje
├── PRZEWODNIK_STUDENTA.md          (Resources, Tools, Prompts)
└── examples/mcpserver/robot_educational.py  (Kompletny przykład)

DZIEŃ 3: Robotyka
├── UNITREE_G1_PRZEWODNIK.md        (Integracja z robotem)
└── Twój własny projekt!

```

---

## 📖 Pełna lista dokumentacji po polsku

### 🎓 Dla studentów (priorytet!)

| Dokument | Opis | Poziom | Czas |
|----------|------|--------|------|
| [README_PL.md](./README_PL.md) | Przegląd MCP po polsku | ⭐ Początkujący | 15 min |
| [PRZEWODNIK_STUDENTA.md](./PRZEWODNIK_STUDENTA.md) | Kompletny przewodnik z przykładami | ⭐⭐ Średnio-zaawansowani | 60 min |
| [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md) | Zastosowanie z robotem Unitree G1 | ⭐⭐⭐ Zaawansowani | 45 min |
| [docs/tutorial_pl.md](./docs/tutorial_pl.md) | Tutorial krok po kroku | ⭐ Początkujący | 30 min |
| [examples/README_PL.md](./examples/README_PL.md) | Przewodnik po przykładach | ⭐⭐ Średnio-zaawansowani | 20 min |

### 💻 Przykłady kodu z komentarzami PL

| Plik | Opis | Co pokazuje |
|------|------|-------------|
| [examples/mcpserver/simple_echo.py](./examples/mcpserver/simple_echo.py) | Najprostszy serwer | Podstawy dekoratorów, Tools |
| [examples/mcpserver/robot_educational.py](./examples/mcpserver/robot_educational.py) | Serwer robotyczny | Resources, Tools, Prompts, Context |

---

## 🚀 Instalacja w 3 krokach

### Krok 1: Zainstaluj uv

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Krok 2: Utwórz projekt

```bash
uv init moj-mcp-projekt
cd moj-mcp-projekt
uv add "mcp[cli]"
```

### Krok 3: Stwórz pierwszy serwer

```bash
# Skopiuj przykład
cp ../mcp-python-sdk/examples/mcpserver/simple_echo.py server.py

# Uruchom
uv run server.py
```

**Gotowe!** Serwer działa na `http://localhost:8000/mcp`

---

## 🧪 Testowanie

### Metoda 1: MCP Inspector (zalecana)

```bash
# Terminal 1: Serwer
uv run server.py

# Terminal 2: Inspector
npx -y @modelcontextprotocol/inspector
# Otwórz przeglądarkę → http://localhost:8000/mcp
```

### Metoda 2: Curl (dla zaawansowanych)

```bash
# Lista narzędzi
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Wywołanie narzędzia
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"tools/call",
    "params":{"name":"hello","arguments":{"name":"Jan"}},
    "id":2
  }'
```

---

## ❓ FAQ - Szybkie odpowiedzi

### Q: Nie wiem od czego zacząć
**A:** Zacznij od [README_PL.md](./README_PL.md), potem [docs/tutorial_pl.md](./docs/tutorial_pl.md)

### Q: Gdzie jest kod przykładowy?
**A:** W katalogu `examples/mcpserver/` - szczególnie `simple_echo.py` i `robot_educational.py`

### Q: Jak użyć MCP z robotem Unitree G1?
**A:** Przeczytaj [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md)

### Q: Co to jest Resource vs Tool vs Prompt?
**A:** 
- **Resource** = odczyt danych (GET)
- **Tool** = wykonanie akcji (POST)
- **Prompt** = szablon instrukcji dla AI

### Q: Jak debugować serwer MCP?
**A:** Użyj MCP Inspector + logi w konsoli + `await ctx.debug()`

### Q: Gdzie znaleźć więcej przykładów?
**A:** Zobacz [examples/README_PL.md](./examples/README_PL.md) - ponad 10 przykładów!

---

## 💡 Szybkie wskazówki

### ✅ DO (Dobre praktyki)

```python
# ✅ Używaj type hints
@mcp.tool()
def dodaj(a: int, b: int) -> int:
    return a + b

# ✅ Pisz dobre docstringi (AI je czyta!)
@mcp.tool()
def move_joint(joint: str, pos: float) -> str:
    """Przesuń staw robota.
    
    BEZPIECZEŃSTWO: Sprawdza limity przed ruchem.
    """
    pass

# ✅ Loguj ważne zdarzenia
@mcp.tool()
async def important_action(ctx):
    await ctx.info("Rozpoczynam operację")
    # ... kod ...
    await ctx.info("Zakończono pomyślnie")
```

### ❌ NIE RÓB (Częste błędy)

```python
# ❌ Brak type hints
@mcp.tool()
def bad_tool(x, y):  # AI nie wie jakie typy!
    return x + y

# ❌ Pusty/zły docstring
@mcp.tool()
def move(a, b):
    """???"""  # AI nie wie co robi ta funkcja
    pass

# ❌ Brak sprawdzenia błędów
@mcp.tool()
def unsafe_move(position):
    robot.move(position)  # Co jeśli position=999999?
```

---

## 🎓 Ścieżka nauki krok po kroku

### Tydzień 1: Fundamenty
- [ ] Przeczytaj README_PL.md
- [ ] Przejdź tutorial_pl.md
- [ ] Uruchom simple_echo.py
- [ ] Przetestuj z Inspector
- [ ] Stwórz własne proste narzędzie

### Tydzień 2: Rozszerzenie
- [ ] Przeczytaj PRZEWODNIK_STUDENTA.md
- [ ] Uruchom robot_educational.py
- [ ] Dodaj własny Resource
- [ ] Dodaj własny Tool
- [ ] Dodaj własny Prompt

### Tydzień 3: Robotyka
- [ ] Przeczytaj UNITREE_G1_PRZEWODNIK.md
- [ ] Przestudiuj przykłady robotyczne
- [ ] Zaplanuj integrację z robotem
- [ ] Zaimplementuj podstawowe sterowanie
- [ ] Przetestuj bezpieczeństwo

### Tydzień 4: Projekt
- [ ] Zaprojektuj własny serwer MCP
- [ ] Zaimplementuj Resources (stan robota)
- [ ] Zaimplementuj Tools (sterowanie)
- [ ] Zaimplementuj Prompts (diagnostyka)
- [ ] Przetestuj z prawdziwym robotem!

---

## 🔗 Przydatne linki

### Dokumentacja polska:
- [README_PL.md](./README_PL.md) - Główny przegląd
- [PRZEWODNIK_STUDENTA.md](./PRZEWODNIK_STUDENTA.md) - Kompletny przewodnik
- [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md) - Robot Unitree G1
- [docs/tutorial_pl.md](./docs/tutorial_pl.md) - Tutorial
- [examples/README_PL.md](./examples/README_PL.md) - Przewodnik po przykładach

### Dokumentacja angielska:
- [README.md](./README.md) - Official README
- [MCP Specification](https://modelcontextprotocol.io/specification/latest)
- [Python SDK API](https://modelcontextprotocol.github.io/python-sdk/)

### Narzędzia:
- [uv](https://docs.astral.sh/uv/) - Python package manager
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - Testing tool

---

## 🎉 Gotowy na start?

**1. Wybierz swoją ścieżkę:**

**Początkujący?**
→ [README_PL.md](./README_PL.md) → [tutorial_pl.md](./docs/tutorial_pl.md) → [simple_echo.py](./examples/mcpserver/simple_echo.py)

**Robotyka?**
→ [PRZEWODNIK_STUDENTA.md](./PRZEWODNIK_STUDENTA.md) → [robot_educational.py](./examples/mcpserver/robot_educational.py) → [UNITREE_G1_PRZEWODNIK.md](./UNITREE_G1_PRZEWODNIK.md)

**2. Zainstaluj MCP:**
```bash
uv init moj-projekt
cd moj-projekt
uv add "mcp[cli]"
```

**3. Uruchom pierwszy przykład:**
```bash
# Skopiuj przykład z repozytorium
uv run examples/mcpserver/simple_echo.py
```

**4. Testuj z Inspector:**
```bash
npx -y @modelcontextprotocol/inspector
```

**Powodzenia! 🚀🤖**

---

*Przygotowane dla studentów Politechniki Rzeszowskiej*  
*Projekt: Robot humanoidalny Unitree G1 EDU-U6*  
*Wersja: 1.0 - Luty 2025*
