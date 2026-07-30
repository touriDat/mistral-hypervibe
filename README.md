# HyperVibe - Intelligenter Workflow-Orchestrator

HyperVibe ist ein **persönlicher Workflow-Assistent**, der komplexe Aufgaben automatisch analysiert, in Subtasks aufteilt und diese parallel oder sequentiell durch Subagents ausführen lässt.

## 🚀 Schnellstart

### Installation

```bash
cd mistral-hypervibe
pip install -r requirements.txt
```

### Verwendung

```bash
# Aufgabe analysieren und Workflow ausführen
python -m src.hypervibe "migriere alle Vue-Komponenten zu Composition API"

# Mit automatischer Bestätigung
python -m src.hypervibe --auto "auditiere die Codebase"

# Nur Plan erstellen (ohne Ausführung)
python -m src.hypervibe --no-execute "führe alle Unit-Tests aus"

# Hilfe anzeigen
python -m src.hypervibe
```

### Als Python-Modul

```python
from src.hypervibe import HyperVibe

hv = HyperVibe(verbose=True)
result = hv.process_task("migriere meine Vue App zu Mapbox v3", auto_confirm=True)

# Nur Analyse
task_analysis = hv.analyze_only("auditiere die API")
print(f"Typ: {task_analysis.type.value}")
print(f"Scope: {task_analysis.scope}")
print(f"Komplexität: {task_analysis.complexity_stars()}")
```

## ✅ Implementierte Features

### Aufgaben-Typen

| Typ | Strategie | Subagents | Beispiel |
|-----|-----------|-----------|----------|
| **Migration** | Parallel | 4 | "migriere Vue zu Composition API" |
| **Audit** | Parallel | 3 | "auditiere die Codebase" |
| **Recherche** | Parallel | 3 | "recherchiere Mapbox v3" |
| **Review** | Parallel | 2 | "review Pull Request #123" |
| **Testing** | Sequentiell | 2 | "führe alle Unit-Tests aus" |
| **Scraping** | Parallel | 4 | "scrape die Website" |
| **Tooling** | Sequentiell | 2 | "konfiguriere CI/CD" |
| **Refactoring** | Parallel | 3 | "refactore die Klasse" |

### Kernfunktionen

- **Aufgabenanalyse**: Automatische Typ- und Scope-Erkennung
- **Komplexitätsbewertung**: ⭐ (einfach) bis ⭐⭐⭐ (komplex)
- **Workflow-Planung**: Parallele/sequenzielle Strategie mit Ressourcen-Schätzung
- **Workflow-Ausführung**: Simuliert mit ThreadPoolExecutor

## 📁 Projektstruktur

```
mistral-hypervibe/
├── SKILL.md                    # Skill-Definition
├── config.yaml                 # Konfiguration
├── patterns.yaml               # Pattern-Definitionen
├── requirements.txt            # Abhängigkeiten
├── src/
│   └── hypervibe.py            # Haupt-Executor
├── integrations/               # Integrations-Konfigurationen
├── templates/                 # Vorlagen
└── workflows/                  # Workflow-Strategien
```

## 🧪 Beispiele

### Vue Migration
```
$ python -m src.hypervibe --no-execute "migriere alle Vue-Komponenten"
🔍 **Aufgabenanalyse**
- Typ: migration
- Scope: Vue
- Komplexität: ⭐⭐⭐

📋 **Vorgeschlagener Plan**
Strategie: Parallel
1. **Subagent 1**: Arbeitet an Teilaufgabe 1 von 4
2. **Subagent 2**: Arbeitet an Teilaufgabe 2 von 4
...
```

### Sicherheitsaudit
```
$ python -m src.hypervibe --auto "auditiere die Codebase"
🚀 Führe Workflow aus...
✅ Workflow abgeschlossen!
   Dauer: 0.31 Sekunden
   Subagents: 3
```

## 🛠️ Entwicklungsstatus

| Komponente | Status |
|-----------|--------|
| Aufgabenanalyse | ✅ |
| Workflow-Planung | ✅ |
| Workflow-Ausführung | ✅ (simuliert) |
| Echte Subagents (task-Tool) | ❌ |
| Pattern-Matching (YAML) | ⏸️ |
| Integrationen (Skills/MCPs) | ⏸️ |
| Anpassungsmodus | ❌ |
| History/Logging | ❌ |

## 📝 Lizenz

MIT License - Siehe [LICENSE](LICENSE)

---

**HyperVibe v1.0.0** - Vereinfachte, funktionierende Version
