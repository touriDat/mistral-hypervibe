# HyperVibe Tests

> Unit-Tests und Integrationstests fr den HyperVibe Skill

---

##  Inhaltsverzeichnis

- [ Uberblick](#-uberblick)
- [ Teststruktur](#-teststruktur)
- [ Voraussetzungen](#-voraussetzungen)
- [ Tests ausfhren](#-tests-ausfhren)
- [ Testabdeckung](#-testabdeckung)
- [ Neue Tests hinzufgen](#-neue-tests-hinzufgen)
- [ Tipps & Tricks](#-tipps--tricks)

---

##  Uberblick

Dieses Verzeichnis enthlt Unit-Tests fr den **HyperVibe Skill** und seine Komponenten:

| Komponente | Testdatei | Beschreibung |
|------------|-----------|--------------|
| IntegrationMatcher | `test_integration_matcher.py` | Pattern-Matching, Integrationsvorschlge, Konfliktlsung |

---

##  Teststruktur

```
tests/
├── __init__.py           # Python Package Marker
├── README.md            # Diese Datei
└── test_integration_matcher.py  # Unit-Tests fr IntegrationMatcher
```

---

##  Voraussetzungen

### Python-Version
- Python 3.8+

### Abhangigkeiten
- `unittest` (Standardbibliothek)
- `yaml` (PyYAML - fr YAML-Dateien)

Installiere die Abhangigkeiten:

```bash
# Im Projektverzeichnis
pip install -r requirements.txt
```

---

##  Tests ausfhren

### Alle Tests ausfhren

```bash
# Im Projekt-root
python -m unittest discover tests -v
```

### Spezifische Testdatei ausfhren

```bash
# Nur IntegrationMatcher-Tests
python -m unittest tests.test_integration_matcher -v
```

### Tests mit Details

```bash
# Sehr ausfhrliche Ausgabe
python -m unittest tests.test_integration_matcher -vv
```

### Test-Abdeckung prfen (optional)

Installiere `coverage`:

```bash
pip install coverage
```

Abdeckung messen:

```bash
coverage run -m unittest discover tests
coverage report -m
```

HTML-Report generieren:

```bash
coverage html
# ffne htmlcov/index.html im Browser
```

---

##  Testabdeckung

### Aktuelle Abdeckung

| Klasse | Methoden | Tests | Status |
|--------|----------|-------|--------|
| `IntegrationMatcher` | 12 | 16 |  OK |
| `IntegrationProposal` | 4 | 5 |  OK |
| `IntegrationFormatter` | 1 | 3 |  OK |
| `ConflictResolutionStrategy` | 3 | 3 |  OK |

**Gesamt: 22 Tests, 100% Erfolg**

### Getestete Funktionalitaten

-  Initialisierung mit Konfigurationsverzeichnis
-  Laden von YAML-Konfigurationen (skills.yaml, mcps.yaml, patterns.yaml)
-  Pattern-Matching fr verschiedene Aufgabentypen
-  Integration-Erkennung (Skills & MCPs)
-  Prioritaten-Berechnung
-  Konfliktlsungsstrategien
-  Aufgaben-Typ-Erkennung
-  Formatierung von Integrationsvorschlagen

---

##  Neue Tests hinzufgen

### Struktur einer Test-Klasse

```python
import unittest
from integration_matcher import IntegrationMatcher, IntegrationProposal

class TestNewFeature(unittest.TestCase):
    """Beschreibung der Test-Klasse."""
    
    def setUp(self):
        """Wird vor jedem Test ausgefhrt."""
        self.matcher = IntegrationMatcher()
    
    def tearDown(self):
        """Wird nach jedem Test ausgefhrt."""
        pass
    
    def test_something(self):
        """Beschreibung des Tests."""
        # Arrange
        task = "test task"
        
        # Act
        result = self.matcher.some_method(task)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result, expected_value)
```

### Best Practices

1. **Namen:** `test_<methode>_<szenario>` (z.B. `test_find_matches_migration`)
2. **Dokumentation:** Jede Test-Methode mit Docstring
3. **Isolation:** Jeder Test sollte unabhangig von anderen sein
4. **Setup/Cleanup:** `setUp()` und `tearDown()` nutzen
5. **Assertions:** Spezifische Assert-Methoden verwenden
   - `assertEqual(a, b)` - Gleichheit
   - `assertTrue(condition)` - Bedingung ist True
   - `assertGreater(a, b)` - a > b
   - `assertIn(item, container)` - Item ist in Container

### Test-Daten

Fr temporare Testdaten (YAML-Dateien), nutze `tempfile.mkdtemp()`:

```python
def setUp(self):
    import tempfile
    import os
    self.temp_dir = tempfile.mkdtemp()
    
    # Test-YAML erstellen
    with open(os.path.join(self.temp_dir, 'skills.yaml'), 'w') as f:
        f.write(self.TEST_SKILLS_YAML)

def tearDown(self):
    import shutil
    shutil.rmtree(self.temp_dir, ignore_errors=True)
```

---

##  Tipps & Tricks

### Debugging

```python
# Temporren Test ausfhren
python -m unittest tests.test_integration_matcher.TestClass.test_method -v
```

### Einzelnen Test ausfhren

```bash
python -m unittest tests.test_integration_matcher.TestIntegrationMatcherInit.test_init_loads_configurations
```

### Test mit Breakpoints

Fge `import pdb; pdb.set_trace()` in deinen Test ein:

```python
def test_something(self):
    import pdb; pdb.set_trace()
    result = function_to_test()
    self.assertTrue(result)
```

### Mocking

Nutze `unittest.mock` fr externen Abhangigkeiten:

```python
from unittest.mock import patch, MagicMock

@patch('module.function')
def test_with_mock(self, mock_function):
    mock_function.return_value = MagicMock()
    result = code_under_test()
    self.assertEqual(result, expected)
```

---

##  Fehlerbehebung

### Haufige Probleme

| Problem | Lsung |
|---------|----------|
| YAML-Datei nicht gefunden | Pfad in `setUp()` prfen |
| Pattern-Matching funktioniert nicht | Pattern-Syntax prfen |
| ImportError | `sys.path.insert(0, 'src')` in Testdatei |

### YAML-Syntax prfen

```bash
python -c "import yaml; yaml.safe_load(open('file.yaml'))"
```

---

##  Links

- [Python unittest Dokumentation](https://docs.python.org/3/library/unittest.html)
- [PyYAML Dokumentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Test-Driven Development mit Python](https://realpython.com/python-testing/)

---

*Dokumentation generiert am 30.07.2026 | HyperVibe v1.0.0*