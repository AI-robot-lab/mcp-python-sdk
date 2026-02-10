"""MCPServer Echo Server

OPIS DLA STUDENTÓW:
===================
To jest NAJPROSTSZY możliwy serwer MCP. Pokazuje podstawową strukturę
każdego serwera MCP:

1. Import klasy MCPServer
2. Utworzenie instancji serwera
3. Definicja narzędzi (tools) przy użyciu dekoratora @mcp.tool()

Ten przykład służy jako punkt startowy do nauki MCP - zrozumienie go
jest kluczowe przed przejściem do bardziej skomplikowanych przykładów.

ZASTOSOWANIE W ROBOTYCE:
=========================
Choć prosty, ten wzorzec jest podstawą do:
- Tworzenia narzędzi diagnostycznych robota
- Testowania komunikacji MCP
- Prototypowania nowych funkcjonalności

URUCHOMIENIE:
=============
Z katalogu głównego repozytorium:
    uv run examples/mcpserver/simple_echo.py
"""

# KROK 1: Import głównej klasy serwera MCP
# MCPServer to klasa bazowa do tworzenia serwerów MCP
# Obsługuje ona całą komunikację z klientami MCP (AI, Inspector, etc.)
from mcp.server.mcpserver import MCPServer

# KROK 2: Utworzenie instancji serwera
# Parametr "Echo Server" to NAZWA SERWERA widoczna dla klientów
# Ta nazwa pomaga zidentyfikować serwer gdy wiele serwerów jest uruchomionych
mcp = MCPServer("Echo Server")


# KROK 3: Definicja narzędzia (Tool)
# Dekorator @mcp.tool() REJESTRUJE funkcję jako narzędzie dostępne dla AI/klientów MCP
# 
# CO ROBI DEKORATOR:
# - Automatycznie generuje schemat JSON dla parametrów (z type hints)
# - Waliduje argumenty przed wywołaniem funkcji
# - Formatuje wynik do odpowiedzi MCP
# - Dodaje narzędzie do listy dostępnych narzędzi serwera
@mcp.tool()
def echo(text: str) -> str:
    """Zwróć dokładnie ten sam tekst, który został podany.
    
    WAŻNE ZASADY DOCSTRINGU:
    ========================
    Docstring jest WIDOCZNY dla AI! AI czyta go aby zrozumieć:
    - CO robi funkcja
    - KIEDY jej użyć
    - JAKIE są ograniczenia/wymagania
    
    TYPY PARAMETRÓW (Type Hints):
    ==============================
    - text: str - WYMAGANE! Określa typ parametru (string)
    - -> str - WYMAGANE! Określa typ zwracanej wartości
    
    Typy są używane do:
    - Automatycznej walidacji (MCP odrzuci nieprawidłowy typ)
    - Generowania schematu JSON (dla dokumentacji API)
    - Lepszego wsparcia IDE (autouzupełnianie, sprawdzanie typów)
    
    Args:
        text: Tekst do zwrócenia (echo)
    
    Returns:
        Ten sam tekst co na wejściu
    
    PRZYKŁAD UŻYCIA PRZEZ AI:
    =========================
    AI: "Użyj narzędzia echo z tekstem 'Hello World'"
    → Wywołanie: echo(text="Hello World")  
    → Wynik: "Hello World"
    """
    # IMPLEMENTACJA:
    # Ta funkcja jest bardzo prosta - po prostu zwraca to co dostała
    # W prawdziwych aplikacjach tutaj byłaby logika biznesowa:
    # - Odczyt z bazy danych
    # - Wywołanie API
    # - Przetwarzanie danych
    # - Sterowanie robotem
    # etc.
    return text
