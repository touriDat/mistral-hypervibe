# Audit Task Template

## Task Description
**Audit Type:** {{audit_type}}
**Scope:** {{scope}}
**Focus Areas:** {{focus_areas}}
**Files/Modules:** {{targets}}

## Subagent Instructions

### Phase 1: Individual Analysis (Subagents 1-{{num_agents}})
**Objective:** Audit assigned files/modules for {{audit_type}}

**Instructions for each Subagent:**
1. You are assigned to audit: `{{assigned_targets}}`
2. Apply {{audit_type}} checklist:

**Checklist for {{audit_type}}:**
{{checklist_items}}

3. For each item found:
   - Document location (file:line)
   - Severity (⭐ Critical, ⭐⭐ High, ⭐⭐⭐ Medium, ⭐⭐⭐⭐ Low)
   - Description
   - Recommendation
4. Assign a risk score (1-10) to each target

**Output Format:**
```markdown
## {{audit_type}} Audit: {{assigned_targets}}

### Summary
- **Files audited:** {{file_count}}
- **Issues found:** {{issue_count}}
- **Overall risk score:** {{risk_score}}/10

### Findings

#### 🔴 Critical (⭐)
| # | Location | Issue | Recommendation |
|---|----------|-------|----------------|
{{critical_findings}}

#### 🟠 High (⭐⭐)
{{high_findings}}

#### 🟡 Medium (⭐⭐⭐)
{{medium_findings}}

#### 🟢 Low (⭐⭐⭐⭐)
{{low_findings}}

### Recommendations
{{recommendations}}
```

---

### Phase 2: Cross-Validation (Subagent {{validation_agent}})
**Objective:** Cross-validate findings across all audits

**Instructions:**
1. Review all individual audit reports
2. Identify duplicate findings
3. Check for false positives
4. Consolidate related issues
5. Assign priority scores

**Output Format:**
```markdown
## Cross-Validation Report

### Duplicates Removed
- {{duplicate_count}} duplicate findings consolidated

### False Positives Identified
{{false_positives}}

### Priority Adjustments
| Original | Adjusted | Reason |
|----------|----------|--------|
{{priority_adjustments}}

### Consolidated Issue List
{{consolidated_issues}}
```

---

### Phase 3: Final Report & Action Plan (Subagent {{report_agent}})
**Objective:** Create comprehensive audit report with action plan

**Instructions:**
1. Aggregate all validated findings
2. Create statistics
3. Generate prioritized action plan
4. Estimate fix efforts

**Output Format:**
```markdown
# {{audit_type}} Audit - Final Report

## Executive Summary
- **Audit Date:** {{date}}
- **Scope:** {{scope}}
- **Total Issues:** {{total_issues}}
- **Risk Level:** {{risk_level}} ({{risk_score}}/10)

## Statistics
| Severity | Count | Percentage |
|----------|-------|------------|
| Critical (⭐) | {{critical_count}} | {{critical_percent}}% |
| High (⭐⭐) | {{high_count}} | {{high_percent}}% |
| Medium (⭐⭐⭐) | {{medium_count}} | {{medium_percent}}% |
| Low (⭐⭐⭐⭐) | {{low_count}} | {{low_percent}}% |

## Top 5 Critical Issues
1. **{{issue1_title}}** ({{issue1_location}})
   - {{issue1_description}}
   - **Fix Effort:** {{issue1_effort}}
   
2. **{{issue2_title}}** ({{issue2_location}})
   - {{issue2_description}}
   - **Fix Effort:** {{issue2_effort}}

{{more_issues}}

## Action Plan

### Immediate Actions (Next 24h)
- [ ] {{action1}}
- [ ] {{action2}}

### Short-term (Next Week)
- [ ] {{action3}}
- [ ] {{action4}}

### Long-term (Next Month)
- [ ] {{action5}}

## Risk Assessment
{{risk_assessment}}

## Next Steps
1. Review this report with the team
2. Assign owners to each action item
3. Schedule fix sessions based on priority
```
