#!/usr/bin/env python3
"""
Unit Tests für IntegrationMatcher.

Testet:
- Pattern-Matching-Funktionalität
- Integration-Erkennung
- Prioritäten-Berechnung
- Konfliktlösung
- YAML-Konfigurationen laden
"""

import unittest
import os
import tempfile
import yaml
from unittest.mock import patch, MagicMock

# Füge src zum Path hinzu für Imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from integration_matcher import (
    IntegrationMatcher,
    IntegrationProposal,
    IntegrationMatch,
    IntegrationType,
    IntegrationMode,
    ConflictResolutionStrategy,
    IntegrationFormatter
)


# ============================================================================
# TEST CONFIGURATIONS
# ============================================================================

# Minimale skills.yaml für Tests
TEST_SKILLS_YAML = """
skill_mappings:
  migration:
    - name: "test-migration-skill"
      trigger_patterns:
        - "migriere.*Vue"
        - "Migration.*JavaScript"
      integration_mode: auto
      priority: 10
      description: "Test Skill für Migrationen"
      tools: ["migrate", "convert"]
    
    - name: "typescript-migration"
      trigger_patterns:
        - "TypeScript.*Migration"
        - "JS.*TS"
      integration_mode: suggest
      priority: 8
      description: "JS zu TS Migration"
  
  audit:
    - name: "security-audit"
      trigger_patterns:
        - "Sicherheits.*Audit"
        - "Security.*Check"
        - "auditiere.*Sicherheit"
        - "Sicherheitslücken"
      integration_mode: auto
      priority: 10
      description: "Sicherheitsaudit"

priority_rules:
  exact_match: 10
  partial_match: 7
  keyword_match: 5
  general_match: 3

conflict_resolution:
  strategy: highest_priority
  max_suggestions: 3
"""

# Minimale mcps.yaml für Tests
TEST_MCPS_YAML = """
mcp_mappings:
  migration:
    - name: "test-mcp-migration"
      trigger_patterns:
        - "migriere.*Mapbox"
        - "Mapbox.*Integration"
      integration_mode: auto
      priority: 9
      description: "Test MCP für Mapbox Migrationen"
      tools: ["location_grounding", "search"]
  
  research:
    - name: "mapbox-search-patterns"
      trigger_patterns:
        - "Mapbox.*Suche"
        - "Geocoding"
      integration_mode: auto
      priority: 10
      description: "Mapbox Suche"

priority_rules:
  exact_match: 10
  partial_match: 7

conflict_resolution:
  strategy: first_match
  max_suggestions: 2
"""

# Minimale patterns.yaml für Tests
TEST_PATTERNS_YAML = """
patterns:
  - name: "vue_migration"
    type: "migration"
    priority: 10
    patterns:
      - "migriere.*Vue"
      - "Vue.*Migration"
    description: "Vue Migration"
  
  - name: "security_audit"
    type: "audit"
    priority: 10
    patterns:
      - "auditiere.*Sicherheit"
      - "Security.*Audit"
    description: "Sicherheitsaudit"
  
  - name: "general_research"
    type: "research"
    priority: 7
    patterns:
      - "recherchiere"
      - "ermittle"
    description: "Allgemeine Recherche"
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_temp_yaml_files():
    """Erstellt temporäre YAML-Dateien für Tests."""
    temp_dir = tempfile.mkdtemp()
    
    # skills.yaml in Hauptverzeichnis
    skills_path = os.path.join(temp_dir, 'skills.yaml')
    with open(skills_path, 'w') as f:
        f.write(TEST_SKILLS_YAML)
    
    # mcps.yaml in Hauptverzeichnis
    mcps_path = os.path.join(temp_dir, 'mcps.yaml')
    with open(mcps_path, 'w') as f:
        f.write(TEST_MCPS_YAML)
    
    # patterns.yaml in Hauptverzeichnis
    patterns_path = os.path.join(temp_dir, 'patterns.yaml')
    with open(patterns_path, 'w') as f:
        f.write(TEST_PATTERNS_YAML)
    
    # Erstelle integrations Directory
    integrations_dir = os.path.join(temp_dir, 'integrations')
    os.makedirs(integrations_dir, exist_ok=True)
    
    # Kopiere skills.yaml und mcps.yaml nach integrations/
    import shutil
    shutil.copy(skills_path, os.path.join(integrations_dir, 'skills.yaml'))
    shutil.copy(mcps_path, os.path.join(integrations_dir, 'mcps.yaml'))
    # patterns.yaml wird nicht in integrations/ kopiert, da IntegrationMatcher
    # es aus dem Hauptverzeichnis lädt
    
    return temp_dir


# ============================================================================
# TEST CLASSES
# ============================================================================

class TestIntegrationMatcherInit(unittest.TestCase):
    """Testet die Initialisierung von IntegrationMatcher."""
    
    def setUp(self):
        self.temp_dir = create_temp_yaml_files()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init_with_config_dir(self):
        """Testet Initialisierung mit Konfigurationsverzeichnis."""
        matcher = IntegrationMatcher(self.temp_dir)
        self.assertIsNotNone(matcher)
        self.assertEqual(matcher.config_dir, self.temp_dir)
    
    def test_init_loads_configurations(self):
        """Testet, dass Konfigurationen geladen werden."""
        matcher = IntegrationMatcher(self.temp_dir)
        # Sollte Skills und MCPs geladen haben
        self.assertGreater(len(matcher.skills_config), 0)
        self.assertGreater(len(matcher.mcps_config), 0)
    
    def test_init_loads_patterns(self):
        """Testet, dass Patterns geladen werden."""
        matcher = IntegrationMatcher(self.temp_dir)
        self.assertIsNotNone(matcher.task_patterns)
        self.assertIn('patterns', matcher.task_patterns)


class TestPatternMatching(unittest.TestCase):
    """Testet Pattern-Matching-Funktionalität."""
    
    def setUp(self):
        self.temp_dir = create_temp_yaml_files()
        self.matcher = IntegrationMatcher(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_find_matches_migration(self):
        """Testet Pattern-Matching für Migration."""
        task = "migriere meine Vue App"
        matches = self.matcher.find_matches(task)
        
        # Sollte mindestens test-migration-skill finden
        names = [m.name for m in matches]
        # Da die temporären Dateien in integrations/ sind, sollten sie gefunden werden
        self.assertGreater(len(matches), 0, f"Keine Matches gefunden. Gefundene Names: {names}")
        
        # Prüfe dass wir Skills oder MCPs gefunden haben
        has_skill = any(m.type == IntegrationType.SKILL for m in matches)
        self.assertTrue(has_skill, "Keine Skills gefunden")
    
    def test_find_matches_security_audit(self):
        """Testet Pattern-Matching für Sicherheitsaudit."""
        task = "auditiere die Codebase auf Sicherheitslücken"
        matches = self.matcher.find_matches(task)
        
        names = [m.name for m in matches]
        # Sollte mindestens ein Match finden
        self.assertGreater(len(matches), 0, f"Keine Matches für '{task}' gefunden. Names: {names}")
        
        # Prüfe dass wir Sicherheits-relevante Integrationen finden
        has_security = any("security" in name.lower() or "audit" in name.lower() for name in names)
        self.assertTrue(has_security, f"Keine Sicherheits-Integrationen gefunden. Names: {names}")
    
    def test_find_matches_by_type_skill_only(self):
        """Testet Filterung nach IntegrationType."""
        task = "migriere meine Vue App"
        matches = self.matcher.find_matches(task, IntegrationType.SKILL)
        
        for match in matches:
            self.assertEqual(match.type, IntegrationType.SKILL)
    
    def test_find_matches_by_type_mcp_only(self):
        """Testet Filterung nach MCP."""
        task = "migriere meine Vue App zu Mapbox"
        matches = self.matcher.find_matches(task, IntegrationType.MCP)
        
        for match in matches:
            self.assertEqual(match.type, IntegrationType.MCP)


class TestIntegrationProposal(unittest.TestCase):
    """Testet die Erstellung von Integrationsvorschlägen."""
    
    def setUp(self):
        self.temp_dir = create_temp_yaml_files()
        self.matcher = IntegrationMatcher(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_proposal_auto_integrations(self):
        """Testet, dass auto-Integrationen erkannt werden."""
        task = "migriere meine Vue App"
        proposal = self.matcher.create_proposal(task)
        
        self.assertIsNotNone(proposal)
        self.assertIsInstance(proposal, IntegrationProposal)
        
        # Sollte auto-Integrationen oder vorgeschlagene Integrationen haben
        # (da unsere Test-YAMLs sowohl auto als auch suggest haben)
        total_integrations = (
            len(proposal.auto_integrations) + 
            len(proposal.suggested_integrations) + 
            len(proposal.required_integrations)
        )
        self.assertGreater(total_integrations, 0, 
                          f"Keine Integrationen gefunden. Auto: {len(proposal.auto_integrations)}, "
                          f"Suggested: {len(proposal.suggested_integrations)}, "
                          f"Required: {len(proposal.required_integrations)}")
    
    def test_create_proposal_suggested_integrations(self):
        """Testet, dass vorgeschlagene Integrationen erkannt werden."""
        task = "TypeScript Migration"
        proposal = self.matcher.create_proposal(task)
        
        # Sollte Integrationen (auto oder suggested) haben
        total_integrations = (
            len(proposal.auto_integrations) + 
            len(proposal.suggested_integrations) + 
            len(proposal.required_integrations)
        )
        self.assertGreater(total_integrations, 0,
                          f"Keine Integrationen für '{task}' gefunden")
    
    def test_create_proposal_task_type_detection(self):
        """Testet die Erkennung des Aufgabentyps."""
        task = "migriere meine Vue App"
        proposal = self.matcher.create_proposal(task)
        
        self.assertEqual(proposal.task_type, "migration")
    
    def test_create_proposal_confidence(self):
        """Testet die Confidence-Berechnung."""
        task = "migriere meine Vue App zu Mapbox"
        proposal = self.matcher.create_proposal(task)
        
        # Confidence sollte zwischen 0 und 1 liegen
        self.assertGreaterEqual(proposal.confidence, 0.0)
        self.assertLessEqual(proposal.confidence, 1.0)
    
    def test_create_proposal_no_matches(self):
        """Testet Vorschlag ohne Matches."""
        task = "mache irgendetwas völlig unbekanntes"
        proposal = self.matcher.create_proposal(task)
        
        # Sollte leere Listen haben
        self.assertEqual(len(proposal.auto_integrations), 0)
        self.assertEqual(len(proposal.suggested_integrations), 0)
        self.assertEqual(len(proposal.required_integrations), 0)


class TestConflictResolution(unittest.TestCase):
    """Testet Konfliktlösungsstrategien."""
    
    def test_highest_priority_strategy(self):
        """Testet highest_priority Strategie."""
        matcher = IntegrationMatcher()
        matcher.conflict_resolution = ConflictResolutionStrategy.HIGHEST_PRIORITY
        
        # Erstelle Test-Matches mit verschiedenen Prioritäten
        matches = [
            IntegrationMatch(
                name="low_priority",
                type=IntegrationType.SKILL,
                integration_mode=IntegrationMode.AUTO,
                priority=5,
                description="Niedrige Priorität",
                matched_pattern="pattern1",
                score=5.0
            ),
            IntegrationMatch(
                name="high_priority",
                type=IntegrationType.SKILL,
                integration_mode=IntegrationMode.AUTO,
                priority=10,
                description="Hohe Priorität",
                matched_pattern="pattern2",
                score=10.0
            ),
            IntegrationMatch(
                name="medium_priority",
                type=IntegrationType.SKILL,
                integration_mode=IntegrationMode.AUTO,
                priority=7,
                description="Mittlere Priorität",
                matched_pattern="pattern3",
                score=7.0
            )
        ]
        
        resolved = matcher._resolve_conflicts(matches)
        
        # Sollte nur die mit höchster Priorität (10) zurückgeben
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0].priority, 10)
    
    def test_first_match_strategy(self):
        """Testet first_match Strategie."""
        matcher = IntegrationMatcher()
        matcher.conflict_resolution = ConflictResolutionStrategy.FIRST_MATCH
        
        matches = [
            IntegrationMatch(
                name="first",
                type=IntegrationType.SKILL,
                integration_mode=IntegrationMode.AUTO,
                priority=5,
                description="Erster Match",
                matched_pattern="pattern1",
                score=5.0
            ),
            IntegrationMatch(
                name="second",
                type=IntegrationType.SKILL,
                integration_mode=IntegrationMode.AUTO,
                priority=10,
                description="Zweiter Match",
                matched_pattern="pattern2",
                score=10.0
            )
        ]
        
        resolved = matcher._resolve_conflicts(matches)
        
        # Sollte nur den ersten zurückgeben
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0].name, "first")
    
    def test_user_choice_strategy(self):
        """Testet user_choice Strategie."""
        matcher = IntegrationMatcher()
        matcher.conflict_resolution = ConflictResolutionStrategy.USER_CHOICE
        matcher.max_suggestions = 2
        
        # Matches müssen nach Score sortiert sein (descending)
        matches = [
            IntegrationMatch(
                name="third",
                type=IntegrationType.SKILL,
                integration_mode=IntegrationMode.SUGGEST,
                priority=10,
                description="Dritter",
                matched_pattern="pattern3",
                score=10.0
            ),
            IntegrationMatch(
                name="second",
                type=IntegrationType.SKILL,
                integration_mode=IntegrationMode.SUGGEST,
                priority=8,
                description="Zweiter",
                matched_pattern="pattern2",
                score=8.0
            ),
            IntegrationMatch(
                name="first",
                type=IntegrationType.SKILL,
                integration_mode=IntegrationMode.SUGGEST,
                priority=5,
                description="Erster",
                matched_pattern="pattern1",
                score=5.0
            )
        ]
        
        resolved = matcher._resolve_conflicts(matches)
        
        # Sollte Top 2 nach Score zurückgeben
        self.assertEqual(len(resolved), 2)
        self.assertEqual(resolved[0].name, "third")
        self.assertEqual(resolved[1].name, "second")


class TestIntegrationFormatter(unittest.TestCase):
    """Testet die Formatierung von Integrationsvorschlägen."""
    
    def test_format_proposal_with_auto_integrations(self):
        """Testet Formatierung mit auto-Integrationen."""
        proposal = IntegrationProposal(
            auto_integrations=[
                IntegrationMatch(
                    name="test-skill",
                    type=IntegrationType.SKILL,
                    integration_mode=IntegrationMode.AUTO,
                    priority=10,
                    description="Test Skill",
                    matched_pattern="pattern",
                    score=10.0,
                    tools=["tool1", "tool2"]
                )
            ]
        )
        
        formatted = IntegrationFormatter.format_proposal(proposal)
        
        self.assertIn("Test Skill", formatted)
        self.assertIn("automatisch", formatted)
        self.assertIn("test-skill", formatted)
    
    def test_format_proposal_with_suggested_integrations(self):
        """Testet Formatierung mit vorgeschlagenen Integrationen."""
        proposal = IntegrationProposal(
            suggested_integrations=[
                IntegrationMatch(
                    name="suggested-skill",
                    type=IntegrationType.SKILL,
                    integration_mode=IntegrationMode.SUGGEST,
                    priority=8,
                    description="Vorgeschlagener Skill",
                    matched_pattern="pattern",
                    score=8.0
                )
            ]
        )
        
        formatted = IntegrationFormatter.format_proposal(proposal)
        
        self.assertIn("Vorgeschlagener Skill", formatted)
        self.assertIn("vorgeschlagen", formatted)
    
    def test_format_proposal_empty(self):
        """Testet Formatierung mit leeren Vorschlägen."""
        proposal = IntegrationProposal()
        
        formatted = IntegrationFormatter.format_proposal(proposal)
        
        self.assertIn("Keine passenden Integrationen gefunden", formatted)


class TestTaskTypeDetection(unittest.TestCase):
    """Testet die Erkennung des Aufgabentyps."""
    
    def setUp(self):
        self.temp_dir = create_temp_yaml_files()
        self.matcher = IntegrationMatcher(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_detect_migration_type(self):
        """Testet Erkennung von Migration."""
        task = "migriere Vue zu Composition API"
        task_type = self.matcher.detect_task_type(task)
        self.assertEqual(task_type, "migration")
    
    def test_detect_audit_type(self):
        """Testet Erkennung von Audit."""
        task = "auditiere die Codebase auf Sicherheitslücken"
        task_type = self.matcher.detect_task_type(task)
        self.assertEqual(task_type, "audit")
    
    def test_detect_research_type(self):
        """Testet Erkennung von Research."""
        task = "recherchiere die besten Practices"
        task_type = self.matcher.detect_task_type(task)
        self.assertEqual(task_type, "research")
    
    def test_detect_unknown_type(self):
        """Testet Erkennung von unbekanntem Typ."""
        task = "mache irgendetwas völlig unbekanntes"
        task_type = self.matcher.detect_task_type(task)
        self.assertIsNone(task_type)


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    unittest.main()
