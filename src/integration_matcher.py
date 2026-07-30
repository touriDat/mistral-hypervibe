#!/usr/bin/env python3
"""
Integration Matcher - Integration-Engine für HyperVibe

Diese Klasse ist das Herzstück der Integration-Funktionalität. Sie:

1. Lädt Konfigurationen aus YAML-Dateien:
   - skills.yaml: Skill-Integrationen
   - mcps.yaml: MCP-Server-Integrationen
   - patterns.yaml: Aufgaben-Typ-Patterns

2. Erkennt passende Integrationen für jede Aufgabe:
   - Pattern-Matching gegen Aufgabentext
   - Prioritäten-basierte Auswahl
   - Konfliktlösung bei mehreren Matches

3. Erstellt Integrationsvorschläge:
   - Automatisch aktivierte Integrationen
   - Vorgeschlagene Integrationen (User-Entscheidung)
   - Zwingend erforderliche Integrationen

Beispiel:
    >>> matcher = IntegrationMatcher()
    >>> proposal = matcher.create_proposal("migriere Vue zu Mapbox v3")
    >>> print(IntegrationFormatter.format_proposal(proposal))

Verwandte Klassen:
    - IntegrationProposal: Vorschlagsstruktur
    - IntegrationMatch: Einzelner Integrations-Match
    - IntegrationFormatter: Formatierung für Ausgabe
    - ConflictResolutionStrategy: Konfliktlösungsstrategien
"""

import re
import yaml
import os
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class IntegrationType(Enum):
    """Typ einer Integration."""
    SKILL = "skill"  # Skill-Integration (z.B. mapbox-web-integration-patterns)
    MCP = "mcp"      # MCP-Server-Integration (z.B. mapbox-location-grounding)


class IntegrationMode(Enum):
    """Modus, in dem eine Integration aktiviert wird."""
    AUTO = "auto"      # Automatisch aktivieren (ohne User-Bestätigung)
    SUGGEST = "suggest" # User entscheidet über Aktivierung
    REQUIRED = "required" # Zwingend erforderlich für die Aufgabe


class ConflictResolutionStrategy(Enum):
    """Strategie zur Lösung von Konflikten bei mehreren Matches."""
    HIGHEST_PRIORITY = "highest_priority"  # Wähle Integrationen mit höchster Priorität
    FIRST_MATCH = "first_match"            # Wähle den ersten gefundenen Match
    USER_CHOICE = "user_choice"           # Zeige Top N dem User zur Auswahl


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class IntegrationMatch:
    """
    Ein gefundener Match für eine Integration (Skill oder MCP).
    
    Enthält alle Informationen, die nötig sind, um eine Integration
    zu identifizieren und zu aktivieren.
    
    Attributes:
        name: Name der Integration (z.B. "mapbox-web-integration-patterns")
        type: Typ (SKILL oder MCP)
        integration_mode: Modus (AUTO, SUGGEST, REQUIRED)
        priority: Priorität aus der Konfiguration (höher = besser)
        description: Menschlich lesbare Beschreibung
        matched_pattern: Das Pattern, das gematcht hat
        score: Berechneter Match-Score (0.0 - 10.0+)
        trigger_patterns: Alle trigger_patterns aus der Konfiguration
        tools: Verfügbare Tools dieser Integration (falls MCP)
    """
    name: str
    type: IntegrationType
    integration_mode: IntegrationMode
    priority: int
    description: str
    matched_pattern: str
    score: float = 0.0
    trigger_patterns: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)


@dataclass
class IntegrationProposal:
    """
    Vorschlag für Integrationen zu einer Aufgabe.
    
    Enthält alle Integrationen, die für eine gegebene Aufgabe passen,
    kategorisiert nach Aktivierungsmodus.
    
    Attributes:
        auto_integrations: Integrationen, die automatisch aktiviert werden
        suggested_integrations: Integrationen, die dem User vorgeschlagen werden
        required_integrations: Integrationen, die zwingend erforderlich sind
        task_type: Erkanntes Aufgabentyp (migration, audit, research, etc.)
        confidence: Vertrauensstufe (0.0 - 1.0) basierend auf der Anzahl Matches
    """
    auto_integrations: List[IntegrationMatch] = field(default_factory=list)
    suggested_integrations: List[IntegrationMatch] = field(default_factory=list)
    required_integrations: List[IntegrationMatch] = field(default_factory=list)
    task_type: Optional[str] = None
    confidence: float = 0.0


@dataclass
class IntegrationConfig:
    """Konfiguration für eine Integration."""
    name: str
    trigger_patterns: List[str]
    integration_mode: IntegrationMode
    priority: int
    description: str
    type: IntegrationType
    tools: List[str] = field(default_factory=list)


# ============================================================================
# INTEGRATION MATCHER
# ============================================================================

class IntegrationMatcher:
    """
    Erkennt passende Skills und MCP-Server für eine gegebene Aufgabe.
    
    Lädt Konfigurationen aus YAML-Dateien und matcht basierend auf:
    - Trigger-Patterns (Regex)
    - Prioritäten
    - Integration-Modi (auto, suggest, required)
    """
    
    # Pfade zu den Konfigurationsdateien
    SKILLS_YAML = "integrations/skills.yaml"
    MCPS_YAML = "integrations/mcps.yaml"
    PATTERNS_YAML = "patterns.yaml"
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialisiert den IntegrationMatcher.
        
        Args:
            config_dir: Verzeichnis, in dem die YAML-Dateien liegen.
                       Standard: aktuelles Verzeichnis.
        """
        self.config_dir = config_dir or os.path.dirname(os.path.dirname(__file__))
        self.skills_config: List[IntegrationConfig] = []
        self.mcps_config: List[IntegrationConfig] = []
        self.task_patterns: Dict[str, Any] = {}
        self.priority_rules: Dict[str, int] = {}
        self.conflict_resolution: ConflictResolutionStrategy = ConflictResolutionStrategy.HIGHEST_PRIORITY
        self.max_suggestions: int = 3
        
        self._load_configurations()
    
    def _fix_yaml_escape_sequences(self, content: str) -> str:
        """
        Korrigiert Escape-Sequenzen in YAML-Inhalten, die Regex-Patterns enthalten.
        
        YAML hat Probleme mit \\s, \\d, etc. in doppelten Anführungszeichen.
        Diese Methode konvertiert alle Pattern-Strings in einfache Anführungszeichen.
        """
        lines = content.split('\n')
        new_lines = []
        in_trigger_patterns = False
        in_patterns = False
        
        for line in lines:
            stripped = line.strip()
            
            if 'trigger_patterns:' in stripped:
                in_trigger_patterns = True
                new_lines.append(line)
                continue
            elif 'patterns:' in stripped and 'trigger_patterns:' not in stripped:
                in_patterns = True
                new_lines.append(line)
                continue
            
            if in_trigger_patterns or in_patterns:
                # Prüfe ob es eine Pattern-Zeile ist (beginnt mit - und hat Anführungszeichen)
                if stripped.startswith('- "'):
                    # Finde alle Anführungszeichen in der Zeile
                    quotes = [i for i, c in enumerate(line) if c == '"']
                    if len(quotes) >= 2:
                        # Nimm das erste Paar von Anführungszeichen
                        start_quote = quotes[0]
                        end_quote = quotes[1]
                        before = line[:start_quote]
                        pattern_content = line[start_quote+1:end_quote]
                        after = line[end_quote+1:]
                        # Ersetze durch einfache Anführungszeichen
                        new_line = f"{before}'{pattern_content}'{after}"
                        new_lines.append(new_line)
                        continue
                elif stripped.startswith("- '"):
                    # Bereits in einfachen Anführungszeichen - überspringen
                    new_lines.append(line)
                    continue
                elif not stripped:
                    # Leere Zeile - wahrscheinlich Ende des Blocks
                    in_trigger_patterns = False
                    in_patterns = False
            
            new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def _normalize_patterns(self, patterns: List[str]) -> List[str]:
        r"""
        Normalisiert Regex-Patterns für die Nutzung in Python.
        
        In YAML mit einfachen Anführungszeichen wird \s als Literal-String '\s' gespeichert.
        Aber wir wollen, dass es als Regex \s interpretiert wird.
        """
        normalized = []
        for pattern in patterns:
            if pattern:
                # In YAML wird \s als Literal '\\s' oder '\s' gespeichert
                # Wir müssen es zu \s für Python Regex machen
                # Ersetze alle doppelt-escaped Sequenzen
                normalized_pattern = pattern.replace(r'\\s', r'\s')
                normalized_pattern = normalized_pattern.replace(r'\s', r'\s')
                normalized_pattern = normalized_pattern.replace(r'\\d', r'\d')
                normalized_pattern = normalized_pattern.replace(r'\d', r'\d')
                normalized_pattern = normalized_pattern.replace(r'\\w', r'\w')
                normalized_pattern = normalized_pattern.replace(r'\w', r'\w')
                normalized.append(normalized_pattern)
        return normalized
    
    def _load_configurations(self):
        """Lädt alle Konfigurationsdateien."""
        self._load_skills_config()
        self._load_mcps_config()
        self._load_patterns_config()
    
    def _load_skills_config(self):
        """Lädt die skills.yaml."""
        skills_path = os.path.join(self.config_dir, self.SKILLS_YAML)
        try:
            with open(skills_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix escape sequences in the YAML content before parsing
            fixed_content = self._fix_yaml_escape_sequences(content)
            config = yaml.safe_load(fixed_content)
            
            if not config:
                return
            
            # Lade Priority Rules
            if 'priority_rules' in config:
                rules = config['priority_rules']
                self.priority_rules = rules if isinstance(rules, dict) else {}
            
            # Lade Conflict Resolution
            if 'conflict_resolution' in config:
                strategy = config['conflict_resolution'].get('strategy', 'highest_priority')
                self.conflict_resolution = ConflictResolutionStrategy(strategy)
                self.max_suggestions = config['conflict_resolution'].get('max_suggestions', 3)
            
            # Parse Skill Mappings
            if 'skill_mappings' in config:
                for task_type, mappings in config['skill_mappings'].items():
                    for mapping in mappings:
                        integration_config = IntegrationConfig(
                            name=mapping['name'],
                            trigger_patterns=self._normalize_patterns(mapping.get('trigger_patterns', [])),
                            integration_mode=IntegrationMode(mapping.get('integration_mode', 'suggest')),
                            priority=mapping.get('priority', 5),
                            description=mapping.get('description', ''),
                            type=IntegrationType.SKILL,
                            tools=mapping.get('tools', [])
                        )
                        self.skills_config.append(integration_config)
                        
        except FileNotFoundError:
            pass  # skills.yaml nicht vorhanden
        except Exception as e:
            print(f"⚠️  Fehler beim Laden von {skills_path}: {e}")
    
    def _load_mcps_config(self):
        """Lädt die mcps.yaml."""
        mcps_path = os.path.join(self.config_dir, self.MCPS_YAML)
        try:
            with open(mcps_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix escape sequences before parsing
            fixed_content = self._fix_yaml_escape_sequences(content)
            config = yaml.safe_load(fixed_content)
            
            if not config:
                return
            
            # Lade MCP-spezifische Priority Rules
            if 'priority_rules' in config:
                mcp_rules = config['priority_rules']
                if isinstance(mcp_rules, dict):
                    self.priority_rules.update(mcp_rules)
            
            # Lade Conflict Resolution (überschreibt Skills-Konfig)
            if 'conflict_resolution' in config:
                strategy = config['conflict_resolution'].get('strategy', 'highest_priority')
                self.conflict_resolution = ConflictResolutionStrategy(strategy)
                self.max_suggestions = config['conflict_resolution'].get('max_suggestions', self.max_suggestions)
            
            # Parse MCP Mappings
            if 'mcp_mappings' in config:
                for task_type, mappings in config['mcp_mappings'].items():
                    for mapping in mappings:
                        integration_config = IntegrationConfig(
                            name=mapping['name'],
                            trigger_patterns=self._normalize_patterns(mapping.get('trigger_patterns', [])),
                            integration_mode=IntegrationMode(mapping.get('integration_mode', 'suggest')),
                            priority=mapping.get('priority', 5),
                            description=mapping.get('description', ''),
                            type=IntegrationType.MCP,
                            tools=mapping.get('tools', [])
                        )
                        self.mcps_config.append(integration_config)
                        
        except FileNotFoundError:
            pass  # mcps.yaml nicht vorhanden
        except Exception as e:
            print(f"⚠️  Fehler beim Laden von {mcps_path}: {e}")
    
    def _load_patterns_config(self):
        """Lädt die patterns.yaml für Aufgaben-Typ-Erkennung."""
        patterns_path = os.path.join(self.config_dir, self.PATTERNS_YAML)
        try:
            with open(patterns_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix escape sequences before parsing
            fixed_content = self._fix_yaml_escape_sequences(content)
            self.task_patterns = yaml.safe_load(fixed_content) or {}
            
            # Normalisiere die Patterns in task_patterns
            if 'patterns' in self.task_patterns:
                for pattern_config in self.task_patterns['patterns']:
                    if 'patterns' in pattern_config:
                        pattern_config['patterns'] = self._normalize_patterns(pattern_config['patterns'])
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"⚠️  Fehler beim Laden von {patterns_path}: {e}")
    
    # ============================================================================
    # PATTERN MATCHING
    # ============================================================================
    
    def _compile_patterns(self, patterns: List[str]) -> List[Tuple[re.Pattern, str]]:
        """Kompiliert String-Patterns zu Regex-Objekten."""
        compiled = []
        for pattern in patterns:
            try:
                # Prüfe ob das Pattern Regex-Sonderzeichen enthält
                # Wenn ja, als Regex-Pattern behandeln
                regex_chars = ['.', '*', '+', '?', '^', '$', '[', ']', '(', ')', '{', '}', '|']
                has_regex_chars = any(char in pattern for char in regex_chars)
                
                if has_regex_chars or pattern.startswith('(?:') or pattern.startswith('.*'):
                    # Regex-Pattern - direkt kompilieren
                    compiled.append((re.compile(pattern, re.IGNORECASE), pattern))
                else:
                    # Einfaches Keyword - als Substring suchen
                    compiled.append((re.compile(re.escape(pattern), re.IGNORECASE), pattern))
            except Exception:
                # Ungültiges Pattern - überspringen
                continue
        return compiled
    
    def _calculate_match_score(self, pattern: str, task: str, priority: int) -> float:
        """
        Berechnet den Match-Score basierend auf:
        - Priority aus der Konfiguration
        - Art des Matches (exakt, partially, keyword)
        """
        task_lower = task.lower()
        pattern_lower = pattern.lower()
        
        # Prüfe Match-Typ
        if pattern_lower in task_lower:
            # Exakter Substring-Match
            base_score = self.priority_rules.get('exact_match', 10)
        elif any(word in task_lower for word in pattern_lower.split()):
            # Keyword-Match
            base_score = self.priority_rules.get('keyword_match', 5)
        else:
            # Partial Match (Regex)
            base_score = self.priority_rules.get('partial_match', 7)
        
        # Kombiniere mit der Integration-Priority
        return (base_score * 0.3) + (priority * 0.7)
    
    def _match_patterns(
        self, 
        task: str, 
        patterns: List[str], 
        priority: int,
        integration_name: str,
        integration_type: IntegrationType,
        description: str,
        tools: List[str] = None
    ) -> Optional[IntegrationMatch]:
        """
        Prüft, ob die Aufgabe zu den Patterns matcht.
        
        Returns:
            IntegrationMatch wenn Match gefunden, sonst None
        """
        compiled_patterns = self._compile_patterns(patterns)
        
        for regex_pattern, original_pattern in compiled_patterns:
            if regex_pattern.search(task):
                score = self._calculate_match_score(original_pattern, task, priority)
                return IntegrationMatch(
                    name=integration_name,
                    type=integration_type,
                    integration_mode=IntegrationMode.SUGGEST,  # wird später überschrieben
                    priority=priority,
                    description=description,
                    matched_pattern=original_pattern,
                    score=score,
                    trigger_patterns=patterns,
                    tools=tools or []
                )
        
        return None
    
    # ============================================================================
    # INTEGRATION MATCHING
    # ============================================================================
    
    def find_matches(
        self, 
        task: str, 
        integration_type: Optional[IntegrationType] = None
    ) -> List[IntegrationMatch]:
        """
        Findet alle passenden Integrationen für eine Aufgabe.
        
        Durchsucht alle Skills und MCPs nach passenden trigger_patterns.
        Jeder Match enthält:
        - name: Name der Integration
        - type: SKILL oder MCP
        - priority: Priorität aus der Konfiguration
        - score: Berechneter Match-Score
        - matched_pattern: Das Pattern, das gematcht hat
        - description: Beschreibung der Integration
        - tools: Verfügbare Tools (falls vorhanden)
        
        Args:
            task: Die Aufgabe als String (z.B. "migriere Vue zu Mapbox")
            integration_type: Filter nach IntegrationType (SKILL, MCP) oder None für beide
            
        Returns:
            Liste aller gefundenen IntegrationMatch-Objekte, sortiert nach Score
            (absteigend: beste Matches zuerst)
            
        Beispiel:
            >>> matcher = IntegrationMatcher()
            >>> matches = matcher.find_matches("migriere Vue zu Mapbox", IntegrationType.SKILL)
            >>> for m in matches:
            ...     print(f"{m.name} (Score: {m.score:.1f})")
        """
        matches: List[IntegrationMatch] = []
        
        # Durchsuche Skills
        if integration_type is None or integration_type == IntegrationType.SKILL:
            for config in self.skills_config:
                match = self._match_patterns(
                    task=task,
                    patterns=config.trigger_patterns,
                    priority=config.priority,
                    integration_name=config.name,
                    integration_type=IntegrationType.SKILL,
                    description=config.description,
                    tools=config.tools
                )
                if match:
                    match.integration_mode = config.integration_mode
                    matches.append(match)
        
        # Durchsuche MCPs
        if integration_type is None or integration_type == IntegrationType.MCP:
            for config in self.mcps_config:
                match = self._match_patterns(
                    task=task,
                    patterns=config.trigger_patterns,
                    priority=config.priority,
                    integration_name=config.name,
                    integration_type=IntegrationType.MCP,
                    description=config.description,
                    tools=config.tools
                )
                if match:
                    match.integration_mode = config.integration_mode
                    matches.append(match)
        
        # Sortiere nach Score (descending)
        matches.sort(key=lambda m: (-m.score, -m.priority))
        
        return matches
    
    def _resolve_conflicts(self, matches: List[IntegrationMatch]) -> List[IntegrationMatch]:
        """
        Löst Konflikte zwischen mehreren Matches.
        
        Args:
            matches: Liste aller Matches
            
        Returns:
            Gefilterte Liste basierend auf der Konfliktlösungsstrategie
        """
        if not matches:
            return []
        
        if self.conflict_resolution == ConflictResolutionStrategy.FIRST_MATCH:
            # Nimm nur den ersten Match
            return [matches[0]]
        elif self.conflict_resolution == ConflictResolutionStrategy.HIGHEST_PRIORITY:
            # Nimm alle, aber nur die mit höchster Priorität
            max_priority = max(m.priority for m in matches)
            return [m for m in matches if m.priority == max_priority][:self.max_suggestions]
        elif self.conflict_resolution == ConflictResolutionStrategy.USER_CHOICE:
            # Nimm Top max_suggestions
            return matches[:self.max_suggestions]
        
        return matches[:self.max_suggestions]
    
    def create_proposal(self, task: str) -> IntegrationProposal:
        """
        Erstellt einen Integrationsvorschlag für eine gegebene Aufgabe.
        
        Dieser Methode analysiert die Aufgabe und schlägt passende Skills
        und MCP-Server vor, die bei der Ausführung helfen können.
        
        Args:
            task: Die Aufgabe als String (z.B. "migriere Vue zu Composition API")
            
        Returns:
            IntegrationProposal mit:
            - auto_integrations: Automatisch zu aktivierende Integrationen
            - suggested_integrations: Vorgeschlagene Integrationen (User-Entscheidung)
            - required_integrations: Zwingend erforderliche Integrationen
            - task_type: Erkanntes Aufgabentyp (migration, audit, research, etc.)
            - confidence: Vertrauensstufe (0.0 - 1.0)
            
        Beispiel:
            >>> matcher = IntegrationMatcher()
            >>> proposal = matcher.create_proposal("auditiere die Codebase")
            >>> print(f"Gefunden: {len(proposal.auto_integrations)} Integrationen")
        """
        all_matches = self.find_matches(task)
        
        # Kategorisiere nach Integration-Mode
        auto_matches = []
        suggest_matches = []
        required_matches = []
        
        for match in all_matches:
            if match.integration_mode == IntegrationMode.AUTO:
                auto_matches.append(match)
            elif match.integration_mode == IntegrationMode.REQUIRED:
                required_matches.append(match)
            else:
                suggest_matches.append(match)
        
        # Löse Konflikte innerhalb jeder Kategorie
        auto_matches = self._resolve_conflicts(auto_matches)
        suggest_matches = self._resolve_conflicts(suggest_matches)
        required_matches = self._resolve_conflicts(required_matches)
        
        # Bestimme Task-Typ aus patterns.yaml
        task_type = self.detect_task_type(task)
        
        # Berechne Confidence (basierend auf Matches)
        total_matches = len(auto_matches) + len(suggest_matches) + len(required_matches)
        confidence = min(1.0, total_matches * 0.3) if total_matches > 0 else 0.0
        
        return IntegrationProposal(
            auto_integrations=auto_matches,
            suggested_integrations=suggest_matches,
            required_integrations=required_matches,
            task_type=task_type,
            confidence=confidence
        )
    
    def detect_task_type(self, task: str) -> Optional[str]:
        """
        Erkennt den Aufgabentyp basierend auf patterns.yaml.
        
        Args:
            task: Die Aufgabe als String
            
        Returns:
            Erkanntes Task-Typ (z. B. 'migration', 'audit') oder None
        """
        if not self.task_patterns or 'patterns' not in self.task_patterns:
            return None
        
        task_lower = task.lower()
        
        for pattern_config in self.task_patterns['patterns']:
            pattern_name = pattern_config.get('name', '')
            pattern_type = pattern_config.get('type', '')
            patterns = pattern_config.get('patterns', [])
            
            for regex_pattern in patterns:
                try:
                    if re.search(regex_pattern, task_lower, re.IGNORECASE):
                        return pattern_type
                except Exception:
                    continue
        
        return None


# ============================================================================
# FORMATTER
# ============================================================================

class IntegrationFormatter:
    """Formatiert Integrationsvorschläge für die Ausgabe."""
    
    @staticmethod
    def format_proposal(proposal: IntegrationProposal) -> str:
        """Formatiert einen Integrationsvorschlag."""
        lines = []
        
        # Header
        lines.append("")
        lines.append("💡 **Empfohlene Integrationen**")
        lines.append("")
        
        # Required Integrations
        if proposal.required_integrations:
            lines.append("### ⭐ Zwingend erforderlich")
            for integration in proposal.required_integrations:
                lines.append(IntegrationFormatter._format_integration(integration, "required"))
            lines.append("")
        
        # Auto Integrations
        if proposal.auto_integrations:
            lines.append("### ✅ Automatisch aktiviert")
            for integration in proposal.auto_integrations:
                lines.append(IntegrationFormatter._format_integration(integration, "auto"))
            lines.append("")
        
        # Suggested Integrations
        if proposal.suggested_integrations:
            lines.append("### ❓ Vorgeschlagen (du entscheidest)")
            for integration in proposal.suggested_integrations:
                lines.append(IntegrationFormatter._format_integration(integration, "suggest"))
            lines.append("")
        
        if not proposal.auto_integrations and not proposal.suggested_integrations and not proposal.required_integrations:
            lines.append("Keine passenden Integrationen gefunden.")
            lines.append("")
        
        # Footer
        lines.append("---")
        
        return "\n".join(lines)
    
    @staticmethod
    def _format_integration(integration: IntegrationMatch, mode: str) -> str:
        """Formatiert eine einzelne Integration."""
        type_icon = "🧠" if integration.type == IntegrationType.SKILL else "🔧"
        mode_text = {
            "auto": "automatisch",
            "suggest": "vorgeschlagen",
            "required": "erforderlich"
        }.get(mode, "vorgeschlagen")
        
        name = integration.name
        description = integration.description
        tools_text = f" (Tools: {', '.join(integration.tools)})" if integration.tools else ""
        
        return f"- {type_icon} **{name}** [{mode_text}] - {description}{tools_text}"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_integration_matcher(config_dir: Optional[str] = None) -> IntegrationMatcher:
    """
    Factory-Funktion für IntegrationMatcher.
    
    Args:
        config_dir: Verzeichnis mit den YAML-Konfigurationen
        
    Returns:
        Instanz von IntegrationMatcher
    """
    return IntegrationMatcher(config_dir)


if __name__ == "__main__":
    # Demo
    matcher = IntegrationMatcher()
    
    # Teste mit verschiedenen Aufgaben
    test_tasks = [
        "migriere meine Vue App zu Mapbox v3",
        "auditiere die Codebase auf Sicherheitslücken",
        "recherchiere die besten Practices für Nuxt 4 mit Cloudflare Workers",
        "führe alle Unit-Tests aus und erstelle ein Coverage-Report",
    ]
    
    for task in test_tasks:
        print(f"\n{'='*60}")
        print(f"Aufgabe: {task}")
        print('='*60)
        
        proposal = matcher.create_proposal(task)
        print(IntegrationFormatter.format_proposal(proposal))
