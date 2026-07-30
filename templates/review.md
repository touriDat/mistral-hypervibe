# Code Review Task Template

## Task Description
**Review Type:** {{review_type}}
**Target:** {{target}}
**Scope:** {{scope}}
**Focus Areas:** {{focus_areas}}
**Severity Threshold:** {{severity_threshold}}

## Subagent Instructions

### Phase 1: Individual Review (Subagents 1-{{num_agents}})
**Objective:** Review assigned files/modules

**Instructions for each Subagent:**
1. You are assigned to review: `{{assigned_files}}`
2. Follow the review checklist for {{review_type}}:

**Review Checklist:**
{{review_checklist}}

3. For each finding:
   - **Type**: Bug / Style / Performance / Security / Best Practice / Documentation
   - **Severity**: ⭐ (Critical) / ⭐⭐ (High) / ⭐⭐⭐ (Medium) / ⭐⭐⭐⭐ (Low)
   - **Location**: file:line:column
   - **Description**: Clear explanation
   - **Suggestion**: How to fix/improve
   - **Priority**: Must fix / Should fix / Nice to have

4. Calculate metrics:
   - Cyclomatic complexity
   - Code duplication
   - Function length
   - Comment ratio

**Output Format:**
```markdown
## Code Review: {{assigned_files}}

### Overall Assessment
- **Quality Score:** {{quality_score}}/10
- **Maintainability:** {{maintainability_score}}/10
- **Readability:** {{readability_score}}/10
- **Recommendation:** {{recommendation}} (Approve/Merge with changes/Request changes)

### Findings Summary
| Type | Critical | High | Medium | Low | Total |
|------|----------|------|--------|-----|-------|
| Bug | {{bug_critical}} | {{bug_high}} | {{bug_medium}} | {{bug_low}} | {{bug_total}} |
| Style | {{style_critical}} | {{style_high}} | {{style_medium}} | {{style_low}} | {{style_total}} |
| Performance | {{perf_critical}} | {{perf_high}} | {{perf_medium}} | {{perf_low}} | {{perf_total}} |
| Security | {{sec_critical}} | {{sec_high}} | {{sec_medium}} | {{sec_low}} | {{sec_total}} |
| Best Practice | {{bp_critical}} | {{bp_high}} | {{bp_medium}} | {{bp_low}} | {{bp_total}} |
| Documentation | {{doc_critical}} | {{doc_high}} | {{doc_medium}} | {{doc_low}} | {{doc_total}} |

### Detailed Findings

#### 🔴 Critical Issues (Must Fix)
1. **[{{issue1_type}}]** `{{issue1_location}}`
   - **Severity:** ⭐
   - **Description:** {{issue1_description}}
   - **Suggestion:** {{issue1_suggestion}}
   - **Impact:** {{issue1_impact}}

2. **[{{issue2_type}}]** `{{issue2_location}}`
   - **Severity:** ⭐
   - **Description:** {{issue2_description}}
   - **Suggestion:** {{issue2_suggestion}}

#### 🟠 High Priority Issues (Should Fix)
{{high_findings}}

#### 🟡 Medium Priority Issues
{{medium_findings}}

#### 🟢 Low Priority Issues (Nice to Have)
{{low_findings}}

### Code Metrics
```
{{metrics_output}}
```

### Positive Aspects
✅ {{positive1}}
✅ {{positive2}}
✅ {{positive3}}

### Suggestions for Improvement
💡 {{suggestion1}}
💡 {{suggestion2}}
```

---

### Phase 2: Consolidation (Subagent {{consolidation_agent}})
**Objective:** Consolidate all individual reviews

**Instructions:**
1. Aggregate findings from all Subagents
2. Remove duplicates
3. Resolve conflicting opinions (note rationale)
4. Calculate overall metrics
5. Create unified findings list

**Output Format:**
```markdown
## Consolidated Review Report

### Overall Statistics
- **Files Reviewed:** {{total_files}}
- **Total Findings:** {{total_findings}}
- **Average Quality Score:** {{avg_quality_score}}/10
- **Critical Issues:** {{critical_count}}
- **High Priority Issues:** {{high_count}}

### Duplicate Findings
- {{duplicate_count}} duplicates removed
- Consolidated from {{original_count}} to {{final_count}} unique findings

### Conflicting Opinions
| File | Subagent A | Subagent B | Resolution |
|------|------------|------------|------------|
{{conflicts}}

### Unified Findings List
{{unified_findings}}
```

---

### Phase 3: Final Report (Subagent {{report_agent}})
**Objective:** Create comprehensive review report

**Instructions:**
1. Combine all consolidated data
2. Create executive summary
3. Generate action items
4. Provide merge recommendation

**Output Format:**
```markdown
# {{review_type}} Review - Final Report

## Executive Summary

**Review Date:** {{date}}
**Reviewer:** HyperVibe ({{subagent_count}} Subagents)
**Target:** {{target}}

### Overall Assessment
**Quality Score:** {{overall_quality}}/10
**Recommendation:** {{merge_recommendation}}

| Category | Score | Grade |
|----------|-------|-------|
| Code Quality | {{quality_score}}/10 | {{quality_grade}} |
| Maintainability | {{maintainability_score}}/10 | {{maintainability_grade}} |
| Security | {{security_score}}/10 | {{security_grade}} |
| Performance | {{performance_score}}/10 | {{performance_grade}} |
| Documentation | {{documentation_score}}/10 | {{documentation_grade}} |

### Critical Issues Blocking Merge
{{blocking_issues}}

### Summary Statistics
| Severity | Count | Percentage |
|----------|-------|------------|
| Critical (⭐) | {{critical_total}} | {{critical_percent}}% |
| High (⭐⭐) | {{high_total}} | {{high_percent}}% |
| Medium (⭐⭐⭐) | {{medium_total}} | {{medium_percent}}% |
| Low (⭐⭐⭐⭐) | {{low_total}} | {{low_percent}}% |

### Findings by Category

#### 🐛 Bugs ({{bug_total}})
{{bug_findings}}

#### 🎨 Style Issues ({{style_total}})
{{style_findings}}

#### ⚡ Performance Issues ({{perf_total}})
{{perf_findings}}

#### 🔒 Security Issues ({{sec_total}})
{{sec_findings}}

#### 📚 Best Practice Violations ({{bp_total}})
{{bp_findings}}

#### 📖 Documentation Issues ({{doc_total}})
{{doc_findings}}

## Action Items

### Must Fix Before Merge
- [ ] {{action1}}
- [ ] {{action2}}

### Should Fix Before Merge
- [ ] {{action3}}
- [ ] {{action4}}

### Nice to Have
- [ ] {{action5}}
- [ ] {{action6}}

## Code Metrics Summary

### Complexity
- **Average Cyclomatic Complexity:** {{avg_complexity}}
- **Max Complexity:** {{max_complexity}} ({{max_complexity_file}})
- **Functions > 20 lines:** {{long_functions}}

### Duplication
- **Duplicate Lines:** {{duplicate_lines}}
- **Duplicate Files:** {{duplicate_files}}

### Size
- **Total Lines:** {{total_lines}}
- **Average File Size:** {{avg_file_size}} lines
- **Largest File:** {{largest_file}} ({{largest_file_lines}} lines)

## Recommendations

### For the Author
{{author_recommendations}}

### For the Team
{{team_recommendations}}

### Long-term Improvements
{{longterm_recommendations}}

## Conclusion
{{conclusion}}

---

**Merge Decision:** {{final_decision}}
**Confidence:** {{confidence_score}}/10
```
