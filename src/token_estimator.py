#!/usr/bin/env python3
"""
Token Estimator - Schtzt Token- und Zeitverbrauch fr Workflows.

Diese Klasse bietet detaillierte Schtzungen fr:
- Token-Verbrauch basierend auf Aufgabentyp, Komplexitt und Integrationen
- Ausfhrungsdauer
- Subagent-spezifische Schtzungen

Features:
- Konfigurierbare Schtzungen aus config.yaml
- Aufgabentyp-spezifische Multiplikatoren
- Integration-Kosten (Skills und MCPs verbrauchen Tokens)
- Komplexittsbasierte Anpassung
"""

import yaml
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

# Import TaskType for type hints
# Avoid circular import by using string type
TaskTypeStr = str


@dataclass
class TokenEstimate:
    """
    Token- und Zeit-Schtzung fr eine Aufgabe.
    
    Attributes:
        tokens: Geschtzte Token-Anzahl
        duration_minutes: Geschtzte Dauer in Minuten
        breakdown: Detaillierte Aufschlsselung der Kosten
    """
    tokens: int
    duration_minutes: float
    breakdown: Dict[str, Any] = field(default_factory=dict)


class TokenEstimator:
    """
    Schtzt Token- und Zeitverbrauch fr HyperVibe-Workflows.
    
    Diese Klasse verwendet konfigurierbare Schtzungen aus config.yaml
    und berechnet detaillierte Schtzungen basierend auf:
    - Aufgabentyp (Migration, Audit, Research, etc.)
    - Komplexitt (LOW, MEDIUM, HIGH)
    - Anzahl Subagents
    - Aktivierte Integrationen
    
    Beispiel:
        >>> estimator = TokenEstimator()
        >>> estimate = estimator.estimate(
        ...     task_type="migration",
        ...     complexity="high",
        ...     num_agents=4,
        ...     integrations=["mapbox-web-integration-patterns"]
        ... )
        >>> print(f"Tokens: {estimate.tokens:,}")
        >>> print(f"Dauer: {estimate.duration_minutes} Min")
    """
    
    # Standardwerte (knnen aus config.yaml erladen werden)
    DEFAULT_TOKEN_ESTIMATES = {
        'simple': 5000,
        'medium': 15000,
        'complex': 30000
    }
    
    DEFAULT_TIME_ESTIMATES = {
        'simple': 2,
        'medium': 5,
        'complex': 10
    }
    
    # Aufgabentyp-Multiplikatoren
    DEFAULT_TASK_TYPE_MULTIPLIERS = {
        'migration': 1.2,    # Migrationen sind oft komplexer
        'audit': 1.1,        # Audits bentigen oft mehr Analyse
        'research': 0.8,    # Recherche ist oft token-sparsam
        'review': 1.0,
        'testing': 1.3,     # Testing bentigt oft mehr Tokens
        'scraping': 0.9,
        'tooling': 1.1,
        'refactoring': 1.2
    }
    
    # Integration-Kosten (pro Integration)
    DEFAULT_INTEGRATION_COSTS = {
        'skill': 2000,      # Token-Kosten pro Skill
        'mcp': 1500        # Token-Kosten pro MCP
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialisiert den TokenEstimator.
        
        Args:
            config_dir: Verzeichnis mit der config.yaml. Default: aktuelles Verzeichnis.
        """
        self.config_dir = config_dir or os.path.dirname(os.path.dirname(__file__))
        self.token_estimates: Dict[str, int] = {}
        self.time_estimates: Dict[str, int] = {}
        self.task_type_multipliers: Dict[str, float] = {}
        self.integration_costs: Dict[str, int] = {}
        
        self._load_config()
    
    def _load_config(self):
        """Ldt die Konfiguration aus config.yaml."""
        config_path = os.path.join(self.config_dir, 'config.yaml')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config:
                # Token-Schtzungen
                if 'token_estimates' in config:
                    self.token_estimates = config['token_estimates']
                else:
                    self.token_estimates = self.DEFAULT_TOKEN_ESTIMATES
                
                # Zeit-Schtzungen
                if 'time_estimates' in config:
                    self.time_estimates = config['time_estimates']
                else:
                    self.time_estimates = self.DEFAULT_TIME_ESTIMATES
                
                # Task-Type-Multiplikatoren (falls in config)
                # Diese knnen in config.yaml hinzugefgt werden
                
        except FileNotFoundError:
            # Fallback zu Defaults
            self.token_estimates = self.DEFAULT_TOKEN_ESTIMATES
            self.time_estimates = self.DEFAULT_TIME_ESTIMATES
        except Exception as e:
            print(f"⚠️  Warnung: Konnte config.yaml nicht laden: {e}")
            self.token_estimates = self.DEFAULT_TOKEN_ESTIMATES
            self.time_estimates = self.DEFAULT_TIME_ESTIMATES
        
        # Lade Task-Type-Multiplikatoren (Default oder aus config)
        self.task_type_multipliers = self.DEFAULT_TASK_TYPE_MULTIPLIERS
        self.integration_costs = self.DEFAULT_INTEGRATION_COSTS
    
    def _get_complexity_level(self, complexity: str) -> str:
        """
        Konvertiert ComplexityLevel zu einem Schtzungs-Level.
        
        Args:
            complexity: ComplexityLevel als String ("low", "medium", "high")
            
        Returns:
            Schtzungs-Level ("simple", "medium", "complex")
        """
        complexity_map = {
            'low': 'simple',
            'medium': 'medium',
            'high': 'complex'
        }
        return complexity_map.get(complexity.lower(), 'medium')
    
    def estimate(
        self,
        task_type: TaskTypeStr,
        complexity: str = "medium",
        num_agents: int = 1,
        integrations: Optional[list] = None,
        strategy: str = "parallel"
    ) -> TokenEstimate:
        """
        Schtzt Token- und Zeitverbrauch fr eine Aufgabe.
        
        Args:
            task_type: Aufgabentyp ("migration", "audit", "research", etc.)
            complexity: Komplexitt ("low", "medium", "high")
            num_agents: Anzahl der Subagents
            integrations: Liste der aktivierten Integrationen (Names)
            strategy: Ausfhrungsstrategie ("parallel" oder "sequential")
            
        Returns:
            TokenEstimate mit Token-Anzahl, Dauer und Breakdown
            
        Beispiel:
            >>> estimator = TokenEstimator()
            >>> estimate = estimator.estimate(
            ...     task_type="migration",
            ...     complexity="high",
            ...     num_agents=4,
            ...     integrations=["mapbox-web-integration-patterns"]
            ... )
        """
        # Basis-Schtzung nach Komplexitt
        complexity_level = self._get_complexity_level(complexity)
        base_tokens = self.token_estimates.get(complexity_level, self.token_estimates['medium'])
        base_time = self.time_estimates.get(complexity_level, self.time_estimates['medium'])
        
        # Task-Typ-Multiplikator
        task_multiplier = self.task_type_multipliers.get(task_type.lower(), 1.0)
        
        # Basis-Tokens anpassen
        adjusted_tokens_per_agent = int(base_tokens * task_multiplier)
        
        # Gesamt-Tokens (Basis * Anzahl Agents)
        total_base_tokens = adjusted_tokens_per_agent * num_agents
        
        # Integration-Kosten hinzufgen
        integration_token_cost = 0
        integration_time_cost = 0
        integration_breakdown = {}
        
        if integrations:
            for integration in integrations:
                # Bestimme Integration-Typ (Skill oder MCP)
                # Default: Skill
                integration_type = 'skill' if 'skill' in integration.lower() else 'mcp'
                cost = self.integration_costs.get(integration_type, 2000)
                
                integration_token_cost += cost
                integration_time_cost += 1  # Jede Integration fgt ~1 Minute hinz
                integration_breakdown[integration] = {
                    'tokens': cost,
                    'time_minutes': 1
                }
        
        # Gesamt-Tokens
        total_tokens = total_base_tokens + integration_token_cost
        
        # Gesamt-Zeit
        total_time = base_time * num_agents + integration_time_cost
        
        # Parallel/Sequentiell-Anpassung
        if strategy == "parallel":
            # Parallel: Zeit ist etwa base_time (da gleichzeitig)
            # Aber mit einem Overhead-Faktor
            parallel_overhead = 1.2
            total_time = base_time * parallel_overhead + (integration_time_cost / num_agents)
        
        # Erstelle Breakdown
        breakdown = {
            'base': {
                'complexity': complexity_level,
                'tokens_per_agent': adjusted_tokens_per_agent,
                'num_agents': num_agents,
                'total_base_tokens': total_base_tokens,
                'base_time_per_agent': base_time,
                'task_type_multiplier': task_multiplier
            },
            'integrations': integration_breakdown,
            'total_integration_cost': integration_token_cost,
            'strategy': strategy
        }
        
        return TokenEstimate(
            tokens=total_tokens,
            duration_minutes=total_time,
            breakdown=breakdown
        )
    
    def estimate_by_workflow_plan(self, workflow_plan: Any) -> TokenEstimate:
        """
        Schtzt Token- und Zeitverbrauch basierend auf einem WorkflowPlan.
        
        Diese Methode extrahiert die relevanten Informationen aus einem
        WorkflowPlan-Objekt und ruft estimate() auf.
        
        Args:
            workflow_plan: WorkflowPlan-Objekt mit task_analysis und subagents
            
        Returns:
            TokenEstimate mit Token-Anzahl, Dauer und Breakdown
        """
        # Extrahiere Informationen aus dem WorkflowPlan
        task_type = workflow_plan.task_analysis.type.value
        complexity = workflow_plan.task_analysis.complexity.value
        num_agents = len(workflow_plan.subagents)
        strategy = workflow_plan.strategy
        
        # Extrahiere Integrationen
        integrations = []
        if workflow_plan.integration_proposal:
            for integration in workflow_plan.integration_proposal.auto_integrations:
                integrations.append(integration.name)
            for integration in workflow_plan.integration_proposal.suggested_integrations:
                integrations.append(integration.name)
            for integration in workflow_plan.integration_proposal.required_integrations:
                integrations.append(integration.name)
        
        return self.estimate(
            task_type=task_type,
            complexity=complexity,
            num_agents=num_agents,
            integrations=integrations,
            strategy=strategy
        )
    
    def get_token_estimate_range(self, estimate: TokenEstimate) -> tuple:
        """
        Gibt einen Bereich (Min, Max) fr die Token-Schtzung.
        
        Bercksichtigt eine Toleranz von +/- 20%.
        
        Args:
            estimate: TokenEstimate-Objekt
            
        Returns:
            Tuple (min_tokens, max_tokens)
        """
        min_tokens = int(estimate.tokens * 0.8)
        max_tokens = int(estimate.tokens * 1.2)
        return (min_tokens, max_tokens)
    
    def format_estimate(self, estimate: TokenEstimate) -> str:
        """
        Formatiert eine Token-Schtzung fr die Ausgabe.
        
        Args:
            estimate: TokenEstimate-Objekt
            
        Returns:
            Formatierter String
        """
        min_tokens, max_tokens = self.get_token_estimate_range(estimate)
        
        lines = []
        lines.append(f"💰 Token-Schtzung: ~{estimate.tokens:,}")
        lines.append(f"   Bereich: {min_tokens:,} - {max_tokens:,} Tokens")
        lines.append(f"⏱️  Zeit-Schtzung: ~{estimate.duration_minutes:.1f} Minuten")
        
        # Breakdown anzeigen (falls verbose)
        if estimate.breakdown:
            lines.append("")
            lines.append("📊 Aufschlsselung:")
            base = estimate.breakdown.get('base', {})
            if base:
                lines.append(f"   - Basis ({base.get('complexity', 'medium')}): "
                           f"{base.get('tokens_per_agent', 0):,} Tokens/Agent × "
                           f"{base.get('num_agents', 0)} Agents")
                if base.get('task_type_multiplier', 1) != 1:
                    lines.append(f"   - Task-Typ-Multiplikator: ×{base.get('task_type_multiplier', 1)}")
            
            integrations = estimate.breakdown.get('integrations', {})
            if integrations:
                lines.append(f"   - Integrationen: +{estimate.breakdown.get('total_integration_cost', 0):,} Tokens")
        
        return "\n".join(lines)


# Utility-Funktion fr einfache Nutzung
def get_token_estimator(config_dir: Optional[str] = None) -> TokenEstimator:
    """
    Factory-Funktion fr TokenEstimator.
    
    Args:
        config_dir: Verzeichnis mit der config.yaml
        
    Returns:
        TokenEstimator-Instanz
    """
    return TokenEstimator(config_dir)


if __name__ == "__main__":
    # Demo
    estimator = TokenEstimator()
    
    # Test mit verschiedenen Szenarien
    scenarios = [
        {"task_type": "migration", "complexity": "high", "num_agents": 4, "integrations": []},
        {"task_type": "audit", "complexity": "medium", "num_agents": 3, "integrations": ["security-audit"]},
        {"task_type": "research", "complexity": "low", "num_agents": 2, "integrations": []},
        {"task_type": "migration", "complexity": "high", "num_agents": 4, 
         "integrations": ["mapbox-web-integration-patterns", "mapbox-maplibre-migration"]},
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"Szenario {i}: {scenario['task_type']} ({scenario['complexity']})")
        print('='*60)
        
        estimate = estimator.estimate(**scenario)
        print(estimator.format_estimate(estimate))
