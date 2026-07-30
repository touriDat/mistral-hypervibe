#!/usr/bin/env python3
"""
HyperVibe - Intelligenter Workflow-Orchestrator

Eine vereinfachte Version, die sofort funktioniert.
"""

import re
import time
import uuid
import os
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import IntegrationMatcher
try:
    from .integration_matcher import (
        IntegrationMatcher, 
        IntegrationFormatter,
        IntegrationProposal,
        IntegrationType,
        IntegrationMode
    )
except ImportError:
    # Fallback für direkte Ausführung
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from integration_matcher import (
        IntegrationMatcher, 
        IntegrationFormatter,
        IntegrationProposal,
        IntegrationType,
        IntegrationMode
    )


# ============================================================================
# ENUMS
# ============================================================================

class TaskType(Enum):
    MIGRATION = "migration"
    AUDIT = "audit"
    RESEARCH = "research"
    REVIEW = "review"
    TESTING = "testing"
    SCRAPING = "scraping"
    TOOLING = "tooling"
    REFACTORING = "refactoring"
    UNKNOWN = "unknown"


class ComplexityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class TaskAnalysis:
    raw_task: str
    type: TaskType = TaskType.UNKNOWN
    scope: Optional[str] = None
    complexity: ComplexityLevel = ComplexityLevel.MEDIUM
    confidence: float = 0.0
    
    def complexity_stars(self) -> str:
        return {
            ComplexityLevel.LOW: "⭐",
            ComplexityLevel.MEDIUM: "⭐⭐",
            ComplexityLevel.HIGH: "⭐⭐⭐"
        }.get(self.complexity, "⭐")


@dataclass
class SubAgent:
    id: str
    name: str
    description: str
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None


@dataclass
class WorkflowPlan:
    task_analysis: TaskAnalysis
    subagents: List[SubAgent] = field(default_factory=list)
    strategy: str = "parallel"
    estimated_duration: int = 0
    estimated_tokens: int = 0
    integration_proposal: Optional[IntegrationProposal] = None
    integrations_enabled: bool = True


@dataclass
class ExecutionResult:
    workflow_plan: WorkflowPlan
    success: bool = True
    results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    total_duration: float = 0.0


# ============================================================================
# PATTERN MATCHING
# ============================================================================

class PatternMatcher:
    """Einfache Pattern-Matching-Engine."""
    
    # Einfache Pattern ohne komplexe Regex
    TASK_PATTERNS = {
        TaskType.MIGRATION: [
            ('migriere', 10), ('portiere', 10), ('wechsle', 9), ('upgrade', 9), ('update', 8),
            ('migration', 10), ('konvertiere', 9)
        ],
        TaskType.AUDIT: [
            ('auditiere', 10), ('prüfe', 10), ('untersuche', 9), ('analysiere', 8),
            ('audit', 10), ('sicherheits', 9), ('ds gvo', 9)
        ],
        TaskType.RESEARCH: [
            ('recherchiere', 10), ('finde', 9), ('ermittle', 8), ('sammle', 8),
            ('recherche', 10), ('dokumentiere', 8), ('wie funktioniert', 7)
        ],
        TaskType.REVIEW: [
            ('review', 10), ('begutachte', 10), ('prüfe', 9), ('durchsicht', 8),
            ('code review', 10)
        ],
        TaskType.TESTING: [
            ('teste', 10), ('führe aus', 9), ('run', 9), ('execute', 8),
            ('test', 10), ('coverage', 9), ('jest', 8), ('vitest', 8)
        ],
        TaskType.SCRAPING: [
            ('scrape', 10), ('extrahiere', 10), ('hole', 9), ('sammle', 8),
            ('scraping', 10)
        ],
        TaskType.TOOLING: [
            ('konfiguriere', 10), ('setze up', 9), ('repariere', 9), ('fixe', 8),
            ('behebe', 8), ('build', 9), ('pipeline', 8), ('ci/cd', 8)
        ],
        TaskType.REFACTORING: [
            ('refactore', 10), ('restrukturiere', 9), ('optimier', 8),
            ('verbessere', 8), ('refactoring', 10)
        ]
    }
    
    def analyze_task(self, task: str) -> TaskAnalysis:
        """Analysiert eine Aufgabe."""
        task_lower = task.lower()
        
        best_match = None
        best_score = 0
        
        for task_type, keywords in self.TASK_PATTERNS.items():
            for keyword, score in keywords:
                if keyword in task_lower:
                    if score > best_score:
                        best_score = score
                        best_match = task_type
        
        # Falls kein Match, versuche es mit Typ-Erkennung
        if best_match is None:
            for task_type, keywords in self.TASK_PATTERNS.items():
                for keyword, score in keywords:
                    if keyword in task_lower:
                        best_match = task_type
                        best_score = score
                        break
                if best_match:
                    break
        
        # Bestimme Scope
        scope = self._determine_scope(task_lower, best_match or TaskType.UNKNOWN)
        
        # Bestimme Komplexität
        complexity = self._determine_complexity(task_lower)
        
        # Berechne Confidence
        confidence = min(1.0, best_score / 10.0) if best_match else 0.0
        
        return TaskAnalysis(
            raw_task=task,
            type=best_match or TaskType.UNKNOWN,
            scope=scope,
            complexity=complexity,
            confidence=confidence
        )
    
    def _determine_scope(self, task: str, task_type: TaskType) -> Optional[str]:
        """Bestimmt den Scope."""
        # Suche nach Technologien
        tech_keywords = {
            'vue': 'Vue', 'nuxt': 'Nuxt', 'react': 'React', 'angular': 'Angular',
            'typescript': 'TypeScript', 'javascript': 'JavaScript', 'node': 'Node.js',
            'python': 'Python', 'java': 'Java', 'go': 'Go', 'rust': 'Rust',
            'mapbox': 'Mapbox', 'api': 'API', 'web': 'Web'
        }
        
        for keyword, scope in tech_keywords.items():
            if keyword in task:
                return scope
        
        # Suche nach "alle", "die", etc.
        if any(kw in task for kw in ['alle ', 'die ', 'das gesamte ', 'sämtliche ']):
            return "komplettes Projekt"
        
        return f"{task_type.value} task" if task_type != TaskType.UNKNOWN else None
    
    def _determine_complexity(self, task: str) -> ComplexityLevel:
        """Bestimmt die Komplexität."""
        # Prüfe auf Komplexitätsindikatoren
        high_indicators = ['alle', 'sämtliche', 'komplett', 'umfassend', 'vollständig']
        low_indicators = ['einfach', 'klein', 'einzelne', 'schnell']
        
        if any(ind in task for ind in high_indicators):
            return ComplexityLevel.HIGH
        elif any(ind in task for ind in low_indicators):
            return ComplexityLevel.LOW
        else:
            return ComplexityLevel.MEDIUM


# ============================================================================
# WORKFLOW EXECUTOR
# ============================================================================

class WorkflowExecutor:
    """Orchestriert Workflows."""
    
    TASK_STRATEGIES = {
        TaskType.MIGRATION: {"default_agents": 4, "parallel": True},
        TaskType.AUDIT: {"default_agents": 3, "parallel": True},
        TaskType.RESEARCH: {"default_agents": 3, "parallel": True},
        TaskType.REVIEW: {"default_agents": 2, "parallel": True},
        TaskType.TESTING: {"default_agents": 2, "parallel": False},
        TaskType.SCRAPING: {"default_agents": 4, "parallel": True},
        TaskType.TOOLING: {"default_agents": 2, "parallel": False},
        TaskType.REFACTORING: {"default_agents": 3, "parallel": True},
        TaskType.UNKNOWN: {"default_agents": 2, "parallel": True},
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialisiert den WorkflowExecutor."""
        self.config_dir = config_dir or os.path.dirname(os.path.dirname(__file__))
        self.integration_matcher = IntegrationMatcher(self.config_dir)
    
    def create_workflow_plan(
        self, 
        task: str, 
        enable_integrations: bool = True
    ) -> WorkflowPlan:
        """Erstellt einen Workflow-Plan mit optionaler Integration."""
        # Analysiere die Aufgabe
        pattern_matcher = PatternMatcher()
        task_analysis = pattern_matcher.analyze_task(task)
        
        # Hole Strategie
        strategy_config = self.TASK_STRATEGIES.get(
            task_analysis.type, self.TASK_STRATEGIES[TaskType.UNKNOWN]
        )
        is_parallel = strategy_config["parallel"]
        default_agents = strategy_config["default_agents"]
        
        # Erstelle Integrationsvorschlag (falls aktiviert)
        integration_proposal = None
        if enable_integrations:
            try:
                integration_proposal = self.integration_matcher.create_proposal(task)
            except Exception as e:
                print(f"⚠️  Fehler beim Erstellen des Integrationsvorschlags: {e}")
        
        # Erstelle Subagents
        subagents = []
        for i in range(default_agents):
            subagent = SubAgent(
                id=f"agent_{i+1}",
                name=f"Subagent {i+1}",
                description=f"Arbeitet an Teilaufgabe {i+1} von {default_agents}"
            )
            subagents.append(subagent)
        
        # Schätze Ressourcen
        complexity_multiplier = {
            ComplexityLevel.LOW: 1,
            ComplexityLevel.MEDIUM: 2,
            ComplexityLevel.HIGH: 3
        }.get(task_analysis.complexity, 2)
        
        estimated_duration = default_agents * 5 * complexity_multiplier
        estimated_tokens = default_agents * 10000 * complexity_multiplier
        
        return WorkflowPlan(
            task_analysis=task_analysis,
            subagents=subagents,
            strategy="parallel" if is_parallel else "sequential",
            estimated_duration=estimated_duration,
            estimated_tokens=estimated_tokens,
            integration_proposal=integration_proposal,
            integrations_enabled=enable_integrations
        )
    
    def format_workflow_plan(self, workflow_plan: WorkflowPlan) -> str:
        """Formatiert den Workflow-Plan."""
        lines = []
        
        lines.append("🔍 **Aufgabenanalyse**")
        lines.append("")
        lines.append(f"- Typ: {workflow_plan.task_analysis.type.value}")
        lines.append(f"- Scope: {workflow_plan.task_analysis.scope or 'Nicht spezifiziert'}")
        lines.append(f"- Komplexität: {workflow_plan.task_analysis.complexity_stars()}")
        lines.append("")
        
        # Zeige Integrationsvorschläge an (falls verfügbar)
        if workflow_plan.integration_proposal and workflow_plan.integrations_enabled:
            lines.append(IntegrationFormatter.format_proposal(workflow_plan.integration_proposal))
        
        lines.append("📋 **Vorgeschlagener Plan**")
        lines.append("")
        
        strategy_text = "Parallel" if workflow_plan.strategy == "parallel" else "Sequentiell"
        lines.append(f"Strategie: {strategy_text}")
        lines.append("")
        
        for i, subagent in enumerate(workflow_plan.subagents, 1):
            lines.append(f"{i}. **Subagent {i}**: {subagent.description}")
        lines.append("")
        
        lines.append("⚠️ **Ressourcen-Schätzung**")
        lines.append("")
        lines.append(f"- Geschätzte Dauer: {workflow_plan.estimated_duration} Minuten")
        lines.append(f"- Geschätzte Tokens: ~{workflow_plan.estimated_tokens:,}")
        lines.append("")
        
        lines.append("✅ **Plan bestätigen?** (Y/n)")
        
        return "\n".join(lines)
    
    def execute_workflow(
        self,
        workflow_plan: WorkflowPlan,
        on_progress: Optional[Callable] = None,
        auto_confirm: bool = True
    ) -> ExecutionResult:
        """Führt einen Workflow aus (simuliert)."""
        start_time = time.time()
        result = ExecutionResult(workflow_plan=workflow_plan)
        
        if not auto_confirm:
            plan_output = self.format_workflow_plan(workflow_plan)
            print(plan_output)
            user_input = input(" Deine Wahl (Y/n): ").strip().lower()
            if user_input in ['n', 'no', 'nein']:
                return ExecutionResult(workflow_plan=workflow_plan, success=False)
        
        # Simuliere Ausführung
        print("🚀 Führe Workflow aus...")
        
        if workflow_plan.strategy == "parallel":
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for subagent in workflow_plan.subagents:
                    future = executor.submit(self._simulate_subagent, subagent)
                    futures.append((future, subagent))
                
                for future, subagent in futures:
                    subagent.result = future.result()
                    if on_progress:
                        on_progress(1)
        else:
            for subagent in workflow_plan.subagents:
                subagent.result = self._simulate_subagent(subagent)
                if on_progress:
                    on_progress(1)
        
        result.total_duration = time.time() - start_time
        result.success = True
        
        # Zeige Ergebnisse
        print("\n✅ Workflow abgeschlossen!")
        print(f"   Dauer: {result.total_duration:.2f} Sekunden")
        print(f"   Subagents: {len(workflow_plan.subagents)}")
        
        return result
    
    def _simulate_subagent(self, subagent: SubAgent) -> Dict[str, Any]:
        """Simuliert einen Subagent."""
        import random
        time.sleep(0.3)  # Simuliere Arbeit
        return {
            "subagent_id": subagent.id,
            "status": "completed",
            "message": f"Subagent {subagent.id} hat seine Aufgabe abgeschlossen"
        }


# ============================================================================
# HAUPTKLASSE
# ============================================================================

class HyperVibe:
    """Hauptklasse für HyperVibe."""
    
    def __init__(self, verbose: bool = False, config_dir: Optional[str] = None):
        self.verbose = verbose
        self.config_dir = config_dir or os.path.dirname(os.path.dirname(__file__))
        self.executor = WorkflowExecutor(self.config_dir)
        self.integration_matcher = IntegrationMatcher(self.config_dir)
    
    def process_task(
        self,
        task: str,
        auto_confirm: bool = False,
        execute: bool = True
    ) -> Optional[ExecutionResult]:
        """Verarbeitet eine Aufgabe von Anfang bis Ende."""
        # Erstelle Workflow-Plan
        workflow_plan = self.executor.create_workflow_plan(task)
        
        if self.verbose:
            print(f"🔄 Aufgabe: {task}")
            print(f"   Typ: {workflow_plan.task_analysis.type.value}")
            print(f"   Scope: {workflow_plan.task_analysis.scope}")
            print(f"   Komplexität: {workflow_plan.task_analysis.complexity_stars()}")
        
        # Führe Workflow aus
        if execute:
            result = self.executor.execute_workflow(
                workflow_plan,
                on_progress=lambda x: None,
                auto_confirm=auto_confirm
            )
            return result
        else:
            # Nur Plan anzeigen
            print(self.executor.format_workflow_plan(workflow_plan))
            return None
    
    def analyze_only(self, task: str) -> TaskAnalysis:
        """Führt nur die Aufgabenanalyse aus."""
        matcher = PatternMatcher()
        return matcher.analyze_task(task)


# ============================================================================
# CLI
# ============================================================================

def main():
    """CLI-Einstiegspunkt."""
    import argparse
    
    parser = argparse.ArgumentParser(description="HyperVibe - Intelligenter Workflow-Orchestrator")
    parser.add_argument("task", nargs="?", default=None, help="Die Aufgabe")
    parser.add_argument("--auto", action="store_true", help="Automatische Bestätigung")
    parser.add_argument("--no-execute", action="store_true", help="Nur Plan erstellen")
    parser.add_argument("-v", "--verbose", action="store_true", help="Ausführlich")
    
    args = parser.parse_args()
    
    hv = HyperVibe(verbose=args.verbose)
    
    if args.task is None:
        print("🎉 **Willkommen bei HyperVibe!**")
        print("\nVerwendung: hypervibe <Aufgabe>")
        print("Beispiele:")
        print("  - hypervibe migriere Vue zu Composition API")
        print("  - hypervibe auditiere die Codebase")
        print("  - hypervibe recherchiere Mapbox v3")
        return
    
    result = hv.process_task(
        task=args.task,
        auto_confirm=args.auto,
        execute=not args.no_execute
    )
    
    return result


if __name__ == "__main__":
    main()
