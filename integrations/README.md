# HyperVibe Integrations

Dieses Verzeichnis enthalt Konfigurationen für die Integration von:
1. **Skills** - Andere Mistral Vibe Skills
2. **MCP-Server** - Model Context Protocol Server

## Integration-Konzept

HyperVibe kann automatisch **passende Skills und MCP-Server** für deine Aufgabe erkennen und vorschlagen oder aktivieren.

### Integration-Modi

| Modus | Beschreibung | Beispiel |
|-------|--------------|----------|
| `auto` | Skill/MCP wird **automatisch aktiviert** | mapbox-token-security für Sicherheitsaudits |
| `suggest` | Skill/MCP wird **vorgeschlagen** (User entscheidet) | mapbox-cartography für Design-Fragen |
| `required` | Skill/MCP ist **zwingend erforderlich** | mapbox-web-integration-patterns für Mapbox-Aufgaben |

### Integrations-Phasen

1. **Pre-Execution**: Skill/MCP wird BEVOR die Subagents starten verwendet
   - Beispiel: Datenabruf, die alle Subagents benötigen
   - MCP: `mapbox-location-grounding` für Standort-Daten

2. **Parallel**: Skill/MCP läuft PARALLEL zu Subagents
   - Beispiel: Tools, die Subagents unterstützen
   - Skill: `mapbox-web-integration-patterns` für Framework-Integrationen

3. **Post-Execution**: Skill/MCP wird NACH den Subagents verwendet
   - Beispiel: Validierung der Ergebnisse
   - MCP: `mapbox-style-quality` für Style-Validierung

## Konfigurationsdateien

### skills.yaml
Definiert, welche **Skills** für welche Aufgabentypen geeignet sind.

Struktur:
```yaml
skill_mappings:
  migration:
    - name: "mapbox-web-integration-patterns"
      trigger_patterns: ["Vue.*Mapbox", "Mapbox.*Integration"]
      integration_mode: auto
      priority: 10
      description: "Für Mapbox-Integrationen in Vue/Nuxt"
```

### mcps.yaml
Definiert, welche **MCP-Server** für welche Aufgabentypen geeignet sind.

Struktur:
```yaml
mcp_mappings:
  research:
    - name: "mapbox-search-patterns"
      trigger_patterns: ["Mapbox.*Suche", "Search.*Pattern"]
      integration_mode: auto
      priority: 10
      tools: ["search_patterns", "autocomplete_config"]
```

## Prioritäts-System

Skills/MCPs werden nach **Relevanz** sortiert:

| Priorität | Beschreibung | Beispiel |
|-----------|--------------|----------|
| 10 | Exakter Pattern-Match | "Mapbox Token Sicherheit" → mapbox-token-security |
| 7 | Teilweiser Match | "Mapbox Suche" → mapbox-search-patterns |
| 5 | Keyword im Task | "Suche" → mapbox-search-patterns |
| 3 | Allgemeine Übereinstimmung | "Karte" → mapbox-web-integration-patterns |

### Konfliktlösung
Wenn mehrere Skills/MCPs passen:
1. **Highest Priority** (Standard) - Höchste Priorität gewinnt
2. **First Match** - Erster Treffer gewinnt
3. **User Choice** - User wählt aus Vorschlägen

Konfiguration in `skills.yaml` und `mcps.yaml`:
```yaml
conflict_resolution:
  strategy: highest_priority
  max_suggestions: 3
```

## Beispiele

### Beispiel 1: Mapbox-Integration

**User-Prompt:**
```
/hypervibe migriere meine Vue 3 App zu Mapbox GL JS v3
```

**HyperVibe-Erkennung:**
1. Aufgabe: Migration (Typ: `migration`)
2. Pattern-Match: "Vue" + "Mapbox" + "GL JS" + "v3"
3. Passende Skills:
   - `mapbox-web-integration-patterns` (Priority: 10, Mode: auto)
   - `mapbox-maplibre-migration` (Priority: 9, Mode: suggest)
4. Passende MCPs:
   - `mapbox-web-integration-patterns` (MCP, Priority: 10, Mode: auto)

**Vorschlag:**
```
🔍 Aufgabenanalyse: Vue → Mapbox GL JS v3 Migration

💡 Empfohlene Integrationen:
1. ✅ Skill: mapbox-web-integration-patterns (auto-aktiviert)
   → Bietet Best Practices für Vue + Mapbox v3
   
2. 🤖 MCP: mapbox-web-integration-patterns (auto-aktiviert)
   → Stellt Tools für Framework-Integrationen bereit
   
3. ❓ Skill: mapbox-maplibre-migration (vorgeschlagen)
   → Falls du von MapLibre kommst
   
✅ Mit diesen Integrationen fortfahren? (Y/n)
```

### Beispiel 2: Sicherheitsaudit

**User-Prompt:**
```
/hv auditiere meine Mapbox-Token-Nutzung auf Sicherheitslücken
```

**HyperVibe-Erkennung:**
1. Aufgabe: Audit (Typ: `audit`)
2. Pattern-Match: "Mapbox" + "Token" + "Sicherheit"
3. Passende Skills:
   - `mapbox-token-security` (Priority: 10, Mode: auto)
   - `security-audit` (Priority: 8, Mode: suggest)
4. Passende MCPs:
   - `mapbox-token-security` (Priority: 10, Mode: auto)

**Aktivierung:**
```
🔍 Aufgabenanalyse: Mapbox-Token-Sicherheitsaudit

💡 Empfohlene Integrationen:
1. ✅ Skill: mapbox-token-security (auto-aktiviert)
   → Prüft Token-Scopes, Restrictions, Rotation
   
2. ✅ MCP: mapbox-token-security (auto-aktiviert)
   → Tools: token_audit, scope_analysis
   
3. ❓ Skill: security-audit (vorgeschlagen)
   → Allgemeines Sicherheitsaudit
   
📋 Plan mit Integrationen:
1. Skill: mapbox-token-security → Analysiere aktuelle Token-Nutzung
2. MCP: token_audit → Prüfe alle Token in der Codebase
3. Subagents: Auditiere Code auf Token-Leaks
4. MCP: scope_analysis → Optimierungsvorschläge

✅ Plan bestätigen? (Y/n)
```

### Beispiel 3: Standort-basierte Recherche

**User-Prompt:**
```
/hypervibe recherchiere Restaurants in Berlin mit Mapbox
```

**HyperVibe-Erkennung:**
1. Aufgabe: Recherche (Typ: `research`)
2. Pattern-Match: "Recherche" + "Restaurants" + "Berlin" + "Mapbox"
3. Passende Skills:
   - `mapbox-search-integration` (Priority: 10, Mode: auto)
4. Passende MCPs:
   - `mapbox-location-grounding` (Priority: 10, Mode: auto)
   - `mapbox-search-patterns` (Priority: 9, Mode: auto)
   - `mapbox-search-integration` (Priority: 8, Mode: suggest)

**Aktivierung:**
```
🔍 Aufgabenanalyse: Standort-basierte Restaurant-Recherche

💡 Empfohlene Integrationen:
1. ✅ MCP: mapbox-location-grounding (auto-aktiviert)
   → Konvertiert "Berlin" zu Koordinaten
   
2. ✅ MCP: mapbox-search-patterns (auto-aktiviert)
   → Sucht nach POI-Mustern für Restaurants
   
3. ✅ Skill: mapbox-search-integration (auto-aktiviert)
   → Kompletter Workflow für Mapbox-Suche
   
4. ❓ MCP: mapbox-search-integration (vorgeschlagen)
   → Für erweiterte Suchfunktionen
   
📋 Plan mit Integrationen:
1. MCP: mapbox-location-grounding → "Berlin" → [13.4050, 52.5200]
2. MCP: mapbox-search-patterns → POI-Kategorien für Restaurants
3. Subagents: Suche Restaurants in Berlin
4. MCP: mapbox-search-integration → Ergebnisse formatieren

✅ Plan bestätigen? (Y/n)
```

## Konfiguration anpassen

### Neue Skills hinzufügen

Füge in `skills.yaml` einen neuen Eintrag hinzu:

```yaml
skill_mappings:
  scraping:
    - name: "mein-custom-scraper"
      trigger_patterns:
        - "(?:meine| custom).*Scraping"
        - "Special.*Data.*Extraction"
      integration_mode: suggest
      priority: 8
      description: "Custom Scraping-Skill für spezielle Datenquellen"
```

### Neue MCP-Server hinzufügen

Füge in `mcps.yaml` einen neuen Eintrag hinzu:

```yaml
mcp_mappings:
  general:
    - name: "mein-custom-mcp"
      trigger_patterns:
        - "(?:Custom|Spezial).*Daten"
      integration_mode: suggest
      priority: 7
      description: "Custom MCP für spezielle Datenabfragen"
      tools:
        - "custom_data_fetch"
        - "special_analysis"
```

## Automatische Aktivierung steuern

In `skills.yaml` und `mcps.yaml`:

```yaml
activation_options:
  auto_activate: false      # Skills/MCPs nicht automatisch aktivieren
  always_suggest: true      # Immer vorschlagen
  show_description: true    # Beschreibung anzeigen
  show_priority: true       # Priorität anzeigen
```

## Best Practices

1. **Skill/MCP-Spezifität**: Je spezifischer der Pattern, desto besser die Übereinstimmung
2. **Prioritäten setzen**: Wichtige Integrationen mit höherer Priorität ausstatten
3. **Modus wählen**: 
   - `auto` für häufig benötigte, sichere Integrationen
   - `suggest` für optionale oder spezielle Integrationen
4. **Testen**: Neue Integrationen zuerst im `suggest`-Modus testen
5. **Dokumentieren**: Immer eine klare `description` angeben

## Fehlerbehandlung

### Wenn ein Skill nicht verfügbar ist
- HyperVibe überspringt den Skill und fährt fort
- Der User wird informiert
- Alternative Skills/MCPs werden vorgeschlagen

### Wenn ein MCP nicht erreichbar ist
- HyperVibe versucht es mit Retry (2 Versuche)
- Bei anhaltenden Problemen wird der MCP übersprungen
- Der User wird gewarnt

### Wenn zu viele Integrationen passen
- Nur die Top `max_suggestions` (Standard: 3) werden angezeigt
- Nach Priorität sortiert
- User kann weitere anfordern

## Monitoring & Logging

HyperVibe loggt alle Integration-Aktivierungen:

```yaml
logging:
  log_integrations: true
  log_path: "~/.vibe/hypervibe_integrations.log"
  log_level: info  # info, debug, warn, error
```

Beispiel-Log-Eintrag:
```
[2026-07-30 14:30:45] INFO: Integration activated
  Task: migration (Vue → Mapbox)
  Skill: mapbox-web-integration-patterns (auto)
  MCP: mapbox-web-integration-patterns (auto)
  Duration: 2.5s
  Status: success
```

## Erweiterte Konfiguration

### Skill-spezifische Parameter

Einige Skills benötigen spezifische Parameter:

```yaml
skill_config:
  mapbox-web-integration-patterns:
    default_framework: "vue"  # Standard-Framework
    check_compatibility: true # Kompatibilität prüfen
    
  mapbox-token-security:
    check_scopes: true
    check_restrictions: true
    suggest_rotation: true
```

### MCP-spezifische Parameter

```yaml
mcp_config:
  timeout_seconds: 30        # Timeout für MCP-Aufrufe
  max_concurrent_calls: 5   # Maximale Parallel-Aufrufe
  retry_attempts: 2        # Wiederholungsversuche
  retry_delay_seconds: 5   # Verzögerung zwischen Retries
```
