# Refactoring Task Template

## Task Description
**Refactoring Type:** {{refactoring_type}}
**Objective:** {{objective}}
**Scope:** {{scope}}
**Target Code:** {{target_code}}
**Constraints:** {{constraints}}

## Subagent Instructions

### Phase 1: Code Analysis (Subagent 1)
**Objective:** Analyze code to be refactored

**Instructions:**
1. Analyze target code: `{{target_code}}`
2. Identify:
   - Code smells
   - Anti-patterns
   - Duplication
   - Complex methods/functions
   - Poor naming
   - Tight coupling
   - Magic numbers/strings
3. Calculate metrics:
   - Cyclomatic complexity
   - Code duplication
   - Function lengths
   - Class sizes
   - Dependency graph
4. Document current structure

**Output Format:**
```markdown
## Code Analysis Report: {{target_code}}

### Code Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Cyclomatic Complexity | {{complexity}} | <10 | {{complexity_status}} |
| Lines of Code | {{loc}} | <{{target_loc}} | {{loc_status}} |
| Duplication | {{duplication}}% | <5% | {{dup_status}} |
| Functions | {{function_count}} | - | - |
| Classes | {{class_count}} | - | - |
| Dependencies | {{dep_count}} | <{{target_deps}} | {{dep_status}} |

### Code Smells Identified

#### 🔴 Critical (Must Fix)
1. **{{smell1}}** in `{{smell1_location}}`
   - **Type:** {{smell1_type}}
   - **Impact:** {{smell1_impact}}
   - **Example:**
     ```{{language}}
     {{smell1_example}}
     ```
   
2. **{{smell2}}** in `{{smell2_location}}`
   - **Type:** {{smell2_type}}
   - **Impact:** {{smell2_impact}}

#### 🟠 High Priority
{{high_smells}}

#### 🟡 Medium Priority
{{medium_smells}}

### Structure Analysis

#### Dependency Graph
```mermaid
graph TD
{{dependency_graph}}
```

#### Class/Module Size
{{size_analysis}}

#### Method Length Distribution
{{method_length_distribution}}

### Pain Points
1. **{{pain1}}**
   - **Location:** {{pain1_location}}
   - **Impact:** {{pain1_impact}}
   - **Current Workaround:** {{pain1_workaround}}

2. **{{pain2}}**
   - **Location:** {{pain2_location}}
   - **Impact:** {{pain2_impact}}

### Refactoring Opportunities

#### High Impact
1. **{{opportunity1}}**
   - **Estimated Effort:** {{effort1}}
   - **Expected Benefit:** {{benefit1}}
   - **ROI:** {{roi1}}

2. **{{opportunity2}}**
   - **Estimated Effort:** {{effort2}}
   - **Expected Benefit:** {{benefit2}}

#### Medium Impact
{{medium_opportunities}}

### Risk Assessment
- **Risk of Breaking Changes:** {{breaking_risk}}/10
- **Test Coverage:** {{coverage}}%
- **Rollback Difficulty:** {{rollback_difficulty}}/10
- **Recommended Approach:** {{recommended_approach}}
```

---

### Phase 2: Refactoring Planning (Subagent 2)
**Objective:** Create detailed refactoring plan

**Instructions:**
1. Based on analysis, create step-by-step plan
2. Prioritize refactorings by impact/effort
3. Group related changes
4. Identify dependencies between refactorings
5. Create timeline
6. Define success criteria

**Output Format:**
```markdown
## Refactoring Plan

### Goal
{{refactoring_goal}}

### Success Criteria
- [ ] {{criteria1}}
- [ ] {{criteria2}}
- [ ] {{criteria3}}

### Prioritized Refactorings

#### Phase 1: High Impact / Low Effort (Quick Wins)
1. **{{refactor1}}**
   - **Files:** {{refactor1_files}}
   - **Changes:** {{refactor1_changes}}
   - **Effort:** {{refactor1_effort}}
   - **Benefit:** {{refactor1_benefit}}
   - **Dependencies:** {{refactor1_deps}}
   
2. **{{refactor2}}**
   - **Files:** {{refactor2_files}}
   - **Changes:** {{refactor2_changes}}
   - **Effort:** {{refactor2_effort}}

#### Phase 2: High Impact / High Effort (Major Improvements)
{{phase2_refactors}}

#### Phase 3: Medium Impact (Nice to Have)
{{phase3_refactors}}

### Dependencies
```mermaid
graph LR
{{dependency_graph}}
```

### Timeline Estimate
| Phase | Refactorings | Effort | Duration |
|-------|--------------|--------|----------|
| 1 | {{phase1_count}} | {{phase1_effort}} | {{phase1_duration}} |
| 2 | {{phase2_count}} | {{phase2_effort}} | {{phase2_duration}} |
| 3 | {{phase3_count}} | {{phase3_effort}} | {{phase3_duration}} |

### Risk Mitigation
1. **Backup Strategy:** {{backup_strategy}}
2. **Test Strategy:** {{test_strategy}}
3. **Rollback Plan:** {{rollback_plan}}
4. **Incremental Approach:** {{incremental_approach}}
```

---

### Phase 3: Implementation (Subagents 3-{{num_impl_agents}})
**Objective:** Implement assigned refactorings

**Instructions for each Subagent:**
1. You are assigned refactorings: `{{assigned_refactors}}`
2. For each refactoring:
   - Create backup
   - Implement changes incrementally
   - Test after each change
   - Document changes
3. Follow the plan from Phase 2
4. Run tests frequently
5. Update documentation

**Refactoring Rules:**
- ✅ Make small, focused changes
- ✅ Keep tests passing
- ✅ Don't mix unrelated changes
- ❌ Don't change behavior
- ❌ Don't remove tests

**Output Format:**
```markdown
## Implementation Report: {{assigned_refactors}}

### Refactoring 1: {{refactor_name}}

#### Changes Made
- **File:** {{file1}}
- **Before:**
  ```{{language}}
  {{before1}}
  ```
- **After:**
  ```{{language}}
  {{after1}}
  ```
- **Reason:** {{reason1}}
- **Impact:** {{impact1}}

#### Tests
- **Before:** {{tests_before}} passed
- **After:** {{tests_after}} passed
- **New Tests Added:** {{new_tests}}

#### Issues Encountered
{{issues1}}

### Refactoring 2: {{refactor2_name}}
{{refactor2_details}}

### Summary
- **Refactorings Completed:** {{completed}}
- **Tests Passing:** {{tests_passing}}
- **Tests Failing:** {{tests_failing}}
- **Time Spent:** {{time_spent}}
```

---

### Phase 4: Validation & Testing (Subagent {{validation_agent}})
**Objective:** Validate all refactorings

**Instructions:**
1. Review all implemented changes
2. Verify:
   - All tests pass
   - No breaking changes
   - Code quality improved
   - Performance not degraded
3. Run:
   - Unit tests
   - Integration tests
   - Linting
   - Build process
4. Compare metrics before/after

**Output Format:**
```markdown
## Validation & Testing Report

### Test Results

#### Before Refactoring
- **Tests:** {{tests_before}}
- **Passed:** {{passed_before}}
- **Failed:** {{failed_before}}
- **Coverage:** {{coverage_before}}%

#### After Refactoring
- **Tests:** {{tests_after}}
- **Passed:** {{passed_after}}
- **Failed:** {{failed_after}}
- **Coverage:** {{coverage_after}}%

### Code Quality Metrics
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Cyclomatic Complexity | {{complexity_before}} | {{complexity_after}} | {{complexity_change}} |
| Lines of Code | {{loc_before}} | {{loc_after}} | {{loc_change}} |
| Duplication | {{dup_before}}% | {{dup_after}}% | {{dup_change}}% |
| Functions | {{func_before}} | {{func_after}} | {{func_change}} |
| Classes | {{class_before}} | {{class_after}} | {{class_change}} |

### Performance Comparison
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Build Time | {{build_before}} | {{build_after}} | {{build_change}} |
| Test Time | {{test_before}} | {{test_after}} | {{test_change}} |

### Issues Found
{{validation_issues}}

### Rollback Information
- **Rollback Needed:** {{rollback_needed}}
- **Rollback Reason:** {{rollback_reason}}
- **Rollback Time:** {{rollback_time}}
```

---

### Phase 5: Final Report (Subagent {{report_agent}})
**Objective:** Create comprehensive refactoring report

**Instructions:**
1. Aggregate all changes
2. Calculate final metrics
3. Document lessons learned
4. Create maintenance guide

**Output Format:**
```markdown
# {{refactoring_type}} Refactoring - Final Report

## Executive Summary

**Date:** {{date}}
**Objective:** {{objective}}
**Status:** {{status}}

### Overall Impact
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Code Quality | {{quality_before}}/10 | {{quality_after}}/10 | {{quality_improvement}} |
| Maintainability | {{maintain_before}}/10 | {{maintain_after}}/10 | {{maintain_improvement}} |
| Complexity | {{complexity_before}} | {{complexity_after}} | {{complexity_improvement}} |
| Test Coverage | {{coverage_before}}% | {{coverage_after}}% | {{coverage_improvement}}% |
| Build Time | {{build_before}} | {{build_after}} | {{build_improvement}} |

## Changes Summary

### Files Modified
| File | Changes | LOC Before | LOC After | Δ |
|------|---------|------------|-----------|---|
{{files_table}}

### Total Changes
- **Files Changed:** {{files_changed}}
- **Lines Added:** {{lines_added}}
- **Lines Removed:** {{lines_removed}}
- **Net Change:** {{net_change}}
- **Tests Added:** {{tests_added}}

## Refactorings Completed

### High Impact ({{high_count}})
1. **{{high1}}**
   - **Benefit:** {{high1_benefit}}
   - **Effort:** {{high1_effort}}
   
2. **{{high2}}**
   - **Benefit:** {{high2_benefit}}

### Medium Impact ({{medium_count}})
{{medium_list}}

### Low Impact ({{low_count}})
{{low_list}}

## Code Quality Improvements

### Before vs After

#### Complexity Reduction
```
{{complexity_comparison}}
```

#### Duplication Reduction
```
{{duplication_comparison}}
```

#### Size Reduction
```
{{size_comparison}}
```

## Test Results

### Test Suite Status
- **Before:** {{tests_before}} tests, {{passed_before}} passed ({{pass_rate_before}}%)
- **After:** {{tests_after}} tests, {{passed_after}} passed ({{pass_rate_after}}%)
- **New Tests:** {{new_tests}}
- **Removed Tests:** {{removed_tests}}

### Test Coverage
```
{{coverage_comparison}}
```

## Performance Impact

### Build Performance
- **Before:** {{build_before}}
- **After:** {{build_after}}
- **Change:** {{build_change}} ({{build_change_percent}}%)

### Runtime Performance
- **Before:** {{runtime_before}}
- **After:** {{runtime_after}}
- **Change:** {{runtime_change}} ({{runtime_change_percent}}%)

## Lessons Learned

### What Went Well
✅ {{success1}}
✅ {{success2}}
✅ {{success3}}

### Challenges Faced
⚠️ {{challenge1}}
   - **Solution:** {{solution1}}
   
⚠️ {{challenge2}}
   - **Solution:** {{solution2}}

### Surprises
🎉 {{surprise1}}
🎉 {{surprise2}}

## Recommendations

### For the Team
💡 {{team_rec1}}
💡 {{team_rec2}}

### For Future Refactorings
💡 {{future_rec1}}
💡 {{future_rec2}}

### Maintenance
🔧 {{maintenance1}}
🔧 {{maintenance2}}

## Next Steps
1. Monitor refactored code in production
2. Schedule follow-up review in {{followup_period}}
3. Document new patterns/standards
4. Share lessons learned with team

---

**Refactoring Success:** {{success_assessment}}
**Quality Improvement:** {{quality_improvement}}
**Recommendation:** {{final_recommendation}}
```
