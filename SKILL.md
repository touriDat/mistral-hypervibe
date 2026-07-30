---
name: hypervibe
id: hypervibe
description: |
  HyperVibe ist ein intelligenter Workflow-Orchestrator, der komplexe Aufgaben
  automatisch in Subagents aufteilt. Er analysiert deine Anfrage, bewertet die
  Komplexität und schlägt einen Ausführungsplan vor - nach deiner Bestätigung
  werden die Aufgaben parallel oder sequentiell von Subagents abgearbeitet.

 Verwendungszwecke:
  - Code-Migrationen (z.B. Vue 2 → Vue 3, Options API → Composition API)
  - Code-Audits (Sicherheit, Performance, Best Practices)
  - Rechercheaufgaben (Dokumentation, API-Specs, Best Practices)
  - Code-Reviews (Pull Requests, ganze Codebasen)
  - Testing (Test-Suiten ausführen, Test-Coverage analysieren)
  - Tooling (Build-Pipelines, Dependency-Updates)
  - Scraping (Daten extrahieren, Webseiten analysieren)
  - Refactoring (Architektur-Anpassungen, Code-Optimierungen)

  Der Skill entscheidet basierend auf der Aufgabenkomplexität, ob eine
  Parallelisierung sinnvoll ist und hält Rücksprache mit dir.

triggers:
  - prefix: "/hypervibe "
  - prefix: "/hv "
  - keyword: "hypervibe"
  - pattern: ".*\b(migriere|auditiere|refactore|analysiere|teste|scrape|recherchiere|review|prüfe)\b.*"

skills: []

required_tools:
  - task

# Integration mit anderen Skills und MCP-Server
integrations:
  skills:
    - name: skills.yaml
      description: "Konfiguration für Skill-Integrationen"
    - name: mcps.yaml
      description: "Konfiguration für MCP-Server-Integrationen"
  
  integration_features:
    - auto_detection: true
    - priority_based_selection: true
    - phase_aware_integration: true
    - conflict_resolution: "highest_priority"

hidden: false
enabled: true
version: 1.0.0
author: Mistral Vibe
---

# HyperVibe - Intelligente Workflow-Orchestrierung

## Übersicht

HyperVibe ist dein **persönlicher Workflow-Assistent**, der komplexe Aufgaben in
managbare Subtasks aufteilt und diese parallel oder sequentiell durch Subagents
ausführen lässt.

## Verwendung

### Explizite Aktivierung
```
/hypervibe <deine Aufgabe>
/hv <deine Aufgabe>  # Kurzform
```

Beispiele:
```
/hypervibe migriere alle Vue-Komponenten von Options API zu Composition API
/hypervibe auditiere die gesamte Codebase auf Sicherheitslücken
/hypervibe recherchiere die besten Practices für Cloudflare Workers mit D1
/hypervibe führe alle Unit-Tests aus und erstelle ein Coverage-Report
```

### Automatische Erkennung
HyperVibe erkennt auch Aufgaben in normalen Prompts, die typische Aktionsverben
enthalten (migriere, auditiere, refactore, analysiere, teste, scrape, recherchiere,
review, prüfe) und fragt nach, ob du einen Workflow starten möchtest.

## Workflow-Phasen

### 1. Aufgabenanalyse
- **Typ-Klassifizierung**: Migration, Audit, Recherche, Review, Testing, Scraping
- **Scope-Bestimmung**: Betroffene Dateien, Verzeichnisse, Module
- **Komplexitätsbewertung**: ⭐ (einfach) bis ⭐⭐⭐⭐⭐ (sehr komplex)

### 2. Plan-Generierung
Basierend auf der Analyse wird ein detaillierter Ausführungsplan erstellt:
- Anzahl benötigter Subagents
- Aufteilung der Aufgaben
- Geschätzte Dauer
- Geschätzte Token-Kosten
- Abhängigkeiten zwischen Subtasks

### 3. User-Bestätigung
Du erhältst eine klare Übersicht:
```
🔍 Aufgabenanalyse
- Typ: Migration
- Scope: 127 Vue-Dateien in /app/components/
- Komplexität: ⭐⭐⭐⭐

📋 Vorgeschlagener Plan
1. Subagent 1: Analysiere bestehende Muster
2. Subagents 2-5: Migriere je 30 Dateien (parallel)
3. Subagent 6: Führe ESLint aus
4. Subagent 7: Erstelle Report

⚠️  Geschätzte Dauer: 15-20 Minuten
💰 Geschätzte Tokens: ~50k

✅ Plan bestätigen? (Y/n/Anpassen)
```

### 4. Ausführung
Nach deiner Bestätigung werden die Subagents gestartet. Je nach Aufgabe:
- **Parallel**: Unabhängige Aufgaben (z.B. Datei-Migrationen)
- **Sequentiell**: Abhängige Aufgaben (z.B. Build → Test → Deploy)

### 5. Ergebnis-Aggregation
Alle Ergebnisse werden zu einer zusammenhängenden Antwort kombiniert.

## Aufgaben-Typen & Strategien

### 🔄 Migrationen
**Beispiele:** Framework-Upgrades, API-Wechsel, Code-Stil-Anpassungen
**Strategie:** Parallel, nach Datei-Gruppen aufgeteilt
**Vorlage:** `templates/migration.md`

### 🔍 Audits
**Beispiele:** Sicherheitsaudits, Performance-Checks, Code-Qualität
**Strategie:** Parallel pro Datei/Modul, dann Zusammenführung
**Vorlage:** `templates/audit.md`

### 📚 Recherche
**Beispiele:** Dokumentations-Recherche, API-Specs, Best Practices
**Strategie:** Parallel pro Quelle/Thema
**Vorlage:** `templates/research.md`

### 👀 Code-Reviews
**Beispiele:** Pull Request Reviews, Architektur-Reviews
**Strategie:** Parallel pro Datei/Modul, dann konsolidierte Bewertung
**Vorlage:** `templates/review.md`

### 🧪 Testing
**Beispiele:** Test-Suiten, Coverage-Analyse, Integrationstests
**Strategie:** Sequentiell (Build → Test → Report)
**Vorlage:** `templates/testing.md`

### 🛠️ Tooling
**Beispiele:** Dependency-Updates, Build-Optimierungen
**Strategie:** Sequentiell mit Abhängigkeiten
**Vorlage:** `templates/tooling.md`

### 🕷️ Scraping
**Beispiele:** Daten-Extraktion, Webseiten-Analyse
**Strategie:** Parallel pro Ziel-URL
**Vorlage:** `templates/scraping.md`

## Komplexitäts-Bewertung

HyperVibe bewertet Aufgaben nach folgenden Kriterien:

| Kriterium | Gewicht | Beispiel |
|-----------|---------|----------|
| Anzahl betroffener Dateien | ⭐⭐⭐⭐ | 100+ Dateien = ⭐⭐⭐⭐⭐ |
| Abhängigkeiten zwischen Aufgaben | ⭐⭐⭐⭐ | Build vor Test = ⭐⭐⭐ |
| Fachliche Komplexität | ⭐⭐⭐⭐ | Framework-Wechsel = ⭐⭐⭐⭐ |
| Externe Abhängigkeiten | ⭐⭐⭐ | API-Aufrufe = ⭐⭐⭐ |
| Geschätzte Ausführungszeit | ⭐⭐ | > 10 Min = ⭐⭐⭐ |

**Komplexitätsstufen:**
- ⭐: Einfach (1 Subagent, < 2 Min)
- ⭐⭐: Leicht (1-2 Subagents, < 5 Min)
- ⭐⭐⭐: Mittel (2-5 Subagents, < 15 Min)
- ⭐⭐⭐⭐: Komplex (5-10 Subagents, < 30 Min)
- ⭐⭐⭐⭐⭐: Sehr komplex (10+ Subagents, > 30 Min)

## Limits & Einschränkungen

- **Maximale Subagents**: 10 gleichzeitig (kann konfiguriert werden)
- **Maximale Aufgaben pro Workflow**: 50 Subtasks
- **Timeout pro Subagent**: 5 Minuten (Standard)
- **Gesamt-Timeout**: 60 Minuten

## Konfiguration

Du kannst HyperVibe in `~/.agents/skills/hypervibe/config.yaml` anpassen:
```yaml
max_concurrent_agents: 8
max_total_agents: 50
default_timeout_minutes: 5
complexity_thresholds:
  low: 1
  medium: 3
  high: 6
```

## Beispiele

### Beispiel 1: Migration
```
User: /hypervibe migriere alle TypeScript-Dateien von JavaScript zu TypeScript

HyperVibe:
🔍 Aufgabenanalyse
- Typ: Migration (JS → TS)
- Scope: 89 .js Dateien in /app/
- Komplexität: ⭐⭐⭐⭐

📋 Plan:
1. Subagent 1: Analysiere bestehende JS-Muster
2. Subagents 2-5: Konvertiere je 20 Dateien
3. Subagent 6: Führe Typecheck aus
4. Subagent 7: Erstelle Migrations-Report

✅ Bestätigen?
```

### Beispiel 2: Audit
```
User: /hv auditiere die gesamte Codebase auf DSGVO-Compliance

HyperVibe:
🔍 Aufgabenanalyse
- Typ: Compliance-Audit
- Scope: Alle Dateien mit Datenverarbeitung
- Komplexität: ⭐⭐⭐⭐⭐

📋 Plan:
1. Subagents 1-4: Analysiere je 1 Modul (Auth, API, DB, UI)
2. Subagent 5: Prüfe Datenflüsse
3. Subagent 6: Erstelle Compliance-Report mit Handlungsempfehlungen

⚠️  6 Subagents, ~45 Min, ~80k Tokens
✅ Bestätigen?
```

### Beispiel 3: Recherche
```
User: Recherchiere die besten Practices für Nuxt 4 mit Cloudflare Workers

HyperVibe:
🔍 Aufgabenanalyse
- Typ: Recherche
- Scope: Nuxt 4 + Cloudflare Workers Best Practices
- Komplexität: ⭐⭐⭐

📋 Plan:
1. Subagent 1: Offizielle Nuxt 4 Docs
2. Subagent 2: Cloudflare Workers Docs
3. Subagent 3: Community-Best-Practices (GitHub, Blogs)
4. Subagent 4: Zusammenführung & Priorisierung

✅ Bestätigen?
```

## Troubleshooting

### Workflow startet nicht
- Prüfe, ob das `task`-Tool verfügbar ist
- Stelle sicher, dass du die notwendigen Berechtigungen hast

### Subagents scheitern
- Überprüfe die Fehler in den einzelnen Subagent-Reports
- Passe den Plan an und starte erneut

### Zu viele Subagents
- Reduziere `max_concurrent_agents` in der Config
- Teile die Aufgabe in kleinere Blöcke auf

## Integration mit Skills & MCP-Server

HyperVibe kann **automatisch passende Skills und MCP-Server** für deine Aufgabe erkennen und integrieren.

### Wie es funktioniert

1. **Aufgabenanalyse**: HyperVibe klassifiziert deine Aufgabe (Migration, Audit, Recherche, etc.)
2. **Pattern-Matching**: Sucht nach Schlüsselwörtern in deinem Prompt
3. **Integrations-Vorschlag**: Zeigt passende Skills und MCP-Server an
4. **Automatische Aktivierung**: Aktiviert Skills/MCPs im `auto`-Modus
5. **User-Bestätigung**: Du entscheidest über Vorschläge im `suggest`-Modus

### Integration-Modi

| Modus | Beschreibung | Beispiel |
|-------|--------------|----------|
| `auto` | **Automatisch aktiviert** | mapbox-token-security für Token-Audits |
| `suggest` | **Vorgeschlagen** (du entscheidest) | mapbox-cartography für Design-Fragen |
| `required` | **Zwingend erforderlich** | Grundlegende Validierung |

### Integrations-Phasen

1. **Pre-Execution** (vor Subagents):
   - Datenabruf, die alle Subagents benötigen
   - Beispiel: `mapbox-location-grounding` für Standort-Daten

2. **Parallel** (neben Subagents):
   - Tools, die Subagents unterstützen
   - Beispiel: `mapbox-web-integration-patterns` für Framework-Hilfe

3. **Post-Execution** (nach Subagents):
   - Validierung der Ergebnisse
   - Beispiel: `mapbox-style-quality` für Style-Checks

### Beispiel: Mapbox-Integration

```
User: /hypervibe migriere meine Vue App zu Mapbox v3

HyperVibe:
🔍 Aufgabenanalyse: Vue → Mapbox v3 Migration

💡 Empfohlene Integrationen:
1. ✅ Skill: mapbox-web-integration-patterns (auto)
   → Best Practices für Vue + Mapbox v3
   
2. ✅ MCP: mapbox-web-integration-patterns (auto)
   → Tools für Framework-Integrationen
   
3. ❓ MCP: mapbox-maplibre-migration (vorgeschlagen)
   → Falls du von MapLibre kommst
   
📋 Plan mit Integrationen:
1. MCP: mapbox-web-integration-patterns → Framework-spezifische Muster
2. Subagents: Migriere Komponenten in Chunks
3. Skill: mapbox-web-integration-patterns → Validierung

✅ Mit diesen Integrationen fortfahren? (Y/n)
```

### Konfiguration

Die Integrationen sind in `integrations/` konfiguriert:
- `skills.yaml`: Welche Skills für welche Aufgaben
- `mcps.yaml`: Welche MCP-Server für welche Aufgaben

Du kannst:
- Neue Skills/MCPs hinzufügen
- Prioritäten anpassen
- Integration-Modi ändern (auto/suggest/required)

### Prioritäts-System

| Priorität | Match-Typ | Beispiel |
|-----------|-----------|----------|
| 10 | Exakter Pattern-Match | "Mapbox Token" → mapbox-token-security |
| 7 | Teilweiser Match | "Mapbox Suche" → mapbox-search-patterns |
| 5 | Keyword-Match | "Suche" → mapbox-search-patterns |
| 3 | Allgemeiner Match | "Karte" → mapbox-web-integration-patterns |

### Konfliktlösung

Wenn mehrere Skills/MCPs passen:
1. **Highest Priority** (Standard): Höchste Priorität gewinnt
2. **First Match**: Erster Treffer gewinnt
3. **User Choice**: Du wählst aus den Top 3 Vorschlägen

### Fehlerbehandlung

- **Skill nicht verfügbar**: Wird übersprungen, User wird informiert
- **MCP nicht erreichbar**: Retry (2x), dann Überspringen mit Warnung
- **Zu viele Matches**: Nur Top 3 werden angezeigt

## Implementierungsdetails

### Architektur

```
src/
├── hypervibe.py          # Haupt-Workflow-Orchestrator
└── integration_matcher.py # Integration-Engine
    
integrations/
├── skills.yaml           # Skill-Konfigurationen
├── mcps.yaml             # MCP-Server-Konfigurationen
└── README.md             # Integrations-Dokumentation

tests/
├── __init__.py
├── README.md             # Test-Dokumentation
└── test_integration_matcher.py  # Unit-Tests
```

### IntegrationMatcher-Klasse

Die **IntegrationMatcher**-Klasse ist das Herzstück der Integration-Engine:

**Verantwortlichkeiten:**
- Lädt und parst `skills.yaml`, `mcps.yaml` und `patterns.yaml`
- Erkennt Aufgabentypen basierend auf Regex-Patterns
- Findet passende Skills und MCP-Server für eine Aufgabe
- Löst Konflikte zwischen mehreren Matches
- Erstellt Integrationsvorschläge mit Prioritäten

**Wichtige Methoden:**

| Methode | Beschreibung |
|---------|--------------|
| `create_proposal(task)` | Erstellt einen Integrationsvorschlag für eine Aufgabe |
| `find_matches(task, type)` | Findet alle passenden Integrationen |
| `detect_task_type(task)` | Erkennt den Aufgabentyp (migration, audit, etc.) |

**Konfigurationsdateien:**

- **skills.yaml**: Definiert welche Skills für welche Aufgabentypen geeignet sind
- **mcps.yaml**: Definiert welche MCP-Server für welche Aufgabentypen geeignet sind
- **patterns.yaml**: Definiert Regex-Patterns für die Aufgabentyp-Erkennung

### WorkflowExecutor-Erweiterung

Der `WorkflowExecutor` wurde um Integrationsunterstützung erweitert:

```python
# Erstellt einen Workflow-Plan mit Integrationsvorschlägen
workflow_plan = executor.create_workflow_plan(
    task="migriere Vue zu Composition API",
    enable_integrations=True
)

# Der Plan enthält jetzt:
# - workflow_plan.integration_proposal (Integrationsvorschläge)
# - workflow_plan.integrations_enabled (Flag)
```

### Testabdeckung

**22 Unit-Tests** decken folgende Funktionalitäten ab:

| Komponente | Tests | Status |
|-----------|-------|--------|
| IntegrationMatcher | 16 | ✅ |
| IntegrationProposal | 5 | ✅ |
| IntegrationFormatter | 3 | ✅ |
| Konfliktlösung | 3 | ✅ |

**Testausführung:**
```bash
# Alle Tests
python -m unittest discover tests -v

# Nur IntegrationMatcher
python -m unittest tests.test_integration_matcher -v
```

## Verwandte Skills

- `mapbox-web-integration-patterns`: Für Mapbox-spezifische Aufgaben (wird automatisch integriert!)
- `find-skills`: Zum Entdecken weiterer Skills
- Alle Skills in `integrations/skills.yaml`
