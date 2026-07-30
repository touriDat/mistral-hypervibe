# Testing Task Template

## Task Description
**Testing Type:** {{testing_type}}
**Scope:** {{scope}}
**Test Framework:** {{framework}}
**Coverage Target:** {{coverage_target}}%

## Subagent Instructions

### Phase 1: Test Discovery (Subagent 1)
**Objective:** Discover all tests in scope

**Instructions:**
1. Find all test files in: `{{scope}}`
2. Identify test framework: {{framework}} (or auto-detect)
3. Categorize tests:
   - Unit tests
   - Integration tests
   - E2E tests
   - Snapshot tests
4. Check current coverage (if coverage reports exist)
5. Identify flaky/failing tests from recent runs

**Output Format:**
```markdown
## Test Discovery Report

### Test Files Found
- **Total:** {{test_file_count}} files
- **Unit Tests:** {{unit_test_count}}
- **Integration Tests:** {{integration_test_count}}
- **E2E Tests:** {{e2e_test_count}}
- **Snapshot Tests:** {{snapshot_test_count}}

### Test Framework
- **Primary:** {{framework}}
- **Version:** {{framework_version}}
- **Configuration:** {{config_file}}

### Current Coverage (if available)
```
{{current_coverage}}
```

### Test File Locations
```
{{test_locations}}
```

### Recently Failing Tests
{{failing_tests}}

### Flaky Tests
{{flaky_tests}}
```

---

### Phase 2: Test Execution (Subagents 2-{{num_execution_agents}})
**Objective:** Execute assigned test suites

**Instructions for each Subagent:**
1. You are assigned test files: `{{assigned_tests}}`
2. Execute tests with command: `{{test_command}}`
3. Capture:
   - Pass/fail status
   - Execution time
   - Error messages
   - Stack traces
4. For failures, analyze:
   - Root cause
   - Is it a test bug or code bug?
   - Severity

**Output Format:**
```markdown
## Test Execution: {{assigned_tests}}

### Summary
- **Tests Run:** {{tests_run}}
- **Passed:** {{passed}}
- **Failed:** {{failed}}
- **Skipped:** {{skipped}}
- **Duration:** {{duration}}
- **Success Rate:** {{success_rate}}%

### Passed Tests
{{passed_tests}}

### Failed Tests
| # | Test | Error | Root Cause | Severity |
|---|------|-------|------------|----------|
{{failed_tests}}

### Skipped Tests
{{skipped_tests}}

### Performance Metrics
- **Average Test Time:** {{avg_time}}ms
- **Slowest Test:** {{slowest_test}} ({{slowest_time}}ms)
- **Tests > 1000ms:** {{slow_tests}}

### Recommendations
💡 {{recommendation1}}
💡 {{recommendation2}}
```

---

### Phase 3: Coverage Analysis (Subagent {{coverage_agent}})
**Objective:** Analyze test coverage

**Instructions:**
1. Generate coverage report: `{{coverage_command}}`
2. Analyze:
   - Overall coverage percentage
   - Coverage by file/module
   - Uncovered lines/branches
   - Complex code without tests
3. Identify:
   - Most covered files
   - Least covered files
   - Critical paths without coverage

**Output Format:**
```markdown
## Coverage Analysis Report

### Overall Coverage
- **Statements:** {{statement_coverage}}%
- **Branches:** {{branch_coverage}}%
- **Functions:** {{function_coverage}}%
- **Lines:** {{line_coverage}}%
- **Target:** {{coverage_target}}%

### Coverage by Directory
| Directory | Coverage | Files |
|-----------|----------|-------|
{{coverage_by_dir}}

### Top 5 Most Covered Files
{{most_covered}}

### Top 5 Least Covered Files
{{least_covered}}

### Uncovered Code Analysis

#### Critical Uncovered Paths
{{critical_uncovered}}

#### Complex Code Without Tests
{{complex_uncovered}}

### Coverage Gaps
```
{{coverage_gaps}}
```

### Recommendations
1. **Add tests for:**
   - {{recommend1}}
   - {{recommend2}}
2. **Refactor for testability:**
   - {{refactor1}}
   - {{refactor2}}
```

---

### Phase 4: Performance & Optimization (Subagent {{perf_agent}})
**Objective:** Analyze test performance

**Instructions:**
1. Identify slow tests ({{slow_threshold}}ms)
2. Analyze test setup/teardown times
3. Check for:
   - Unnecessary mocking
   - Heavy computations in tests
   - External API calls
   - Large test fixtures
4. Provide optimization suggestions

**Output Format:**
```markdown
## Test Performance Analysis

### Slow Tests (>{{slow_threshold}}ms)
| Test | Duration | Issue | Recommendation |
|------|----------|-------|----------------|
{{slow_tests_table}}

### Setup/Teardown Analysis
- **Average Setup Time:** {{avg_setup}}ms
- **Average Teardown Time:** {{avg_teardown}}ms
- **Total Overhead:** {{total_overhead}}ms

### Bottlenecks Identified
1. **{{bottleneck1}}** ({{bottleneck1_time}}ms)
   - {{bottleneck1_analysis}}
   
2. **{{bottleneck2}}** ({{bottleneck2_time}}ms)
   - {{bottleneck2_analysis}}

### Optimization Opportunities
🚀 **{{optimization1}}**
   - Potential time savings: {{savings1}}ms
   - Implementation: {{impl1}}

🚀 **{{optimization2}}**
   - Potential time savings: {{savings2}}ms
   - Implementation: {{impl2}}
```

---

### Phase 5: Final Report (Subagent {{report_agent}})
**Objective:** Create comprehensive testing report

**Instructions:**
1. Aggregate all test results
2. Calculate overall metrics
3. Generate action plan
4. Provide quality assessment

**Output Format:**
```markdown
# {{testing_type}} Testing - Final Report

## Executive Summary

**Date:** {{date}}
**Duration:** {{total_duration}}
**Subagents Used:** {{subagent_count}}

### Overall Results
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Tests Run | {{total_tests}} | - | ✅ |
| Passed | {{total_passed}} | {{total_tests}} | {{pass_rate_status}} |
| Failed | {{total_failed}} | 0 | {{fail_status}} |
| Coverage | {{total_coverage}}% | {{coverage_target}}% | {{coverage_status}} |
| Avg. Duration | {{avg_duration}}ms | <{{target_duration}}ms | {{duration_status}} |

## Test Results

### Summary by Type
| Type | Run | Passed | Failed | Success Rate |
|------|-----|--------|--------|--------------|
| Unit | {{unit_run}} | {{unit_passed}} | {{unit_failed}} | {{unit_rate}}% |
| Integration | {{integration_run}} | {{integration_passed}} | {{integration_failed}} | {{integration_rate}}% |
| E2E | {{e2e_run}} | {{e2e_passed}} | {{e2e_failed}} | {{e2e_rate}}% |

### Failed Tests ({{total_failed}})
{{failed_tests_summary}}

### Flaky Tests ({{flaky_count}})
{{flaky_tests_summary}}

## Coverage Analysis

### Current Coverage: {{total_coverage}}%
```
{{coverage_summary}}
```

### Coverage by Module
{{coverage_by_module}}

### Uncovered Critical Paths
{{critical_uncovered_summary}}

## Performance Analysis

### Test Suite Performance
- **Total Execution Time:** {{total_time}}
- **Average Test Time:** {{avg_test_time}}ms
- **Slowest Test:** {{slowest_test}} ({{slowest_time}}ms)

### Performance Issues
{{performance_issues}}

## Quality Assessment

### Test Quality Score: {{quality_score}}/10

| Category | Score | Notes |
|----------|-------|-------|
| Coverage | {{coverage_score}}/10 | {{coverage_notes}} |
| Reliability | {{reliability_score}}/10 | {{reliability_notes}} |
| Performance | {{perf_score}}/10 | {{perf_notes}} |
| Maintainability | {{maintainability_score}}/10 | {{maintainability_notes}} |

## Action Plan

### 🔴 Critical (Fix Immediately)
- [ ] {{critical_action1}}
- [ ] {{critical_action2}}

### 🟠 High Priority (Fix This Week)
- [ ] {{high_action1}}
- [ ] {{high_action2}}

### 🟡 Medium Priority (Fix This Month)
- [ ] {{medium_action1}}
- [ ] {{medium_action2}}

### 🟢 Low Priority (Backlog)
- [ ] {{low_action1}}

## Recommendations

### For Developers
{{dev_recommendations}}

### For the Team
{{team_recommendations}}

### For CI/CD
{{cicd_recommendations}}

## Next Steps
1. Fix critical test failures
2. Address flaky tests
3. Implement coverage improvements
4. Optimize slow tests

---

**Overall Test Health:** {{health_score}}/10 ({{health_assessment}})
```
