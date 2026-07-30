# Tooling Task Template

## Task Description
**Tooling Type:** {{tooling_type}}
**Objective:** {{objective}}
**Scope:** {{scope}}
**Tools/Technologies:** {{tools}}

## Subagent Instructions

### Phase 1: Environment Analysis (Subagent 1)
**Objective:** Analyze current tooling environment

**Instructions:**
1. Analyze current state of: `{{scope}}`
2. Identify:
   - Current tools and versions
   - Configuration files
   - Dependency tree
   - Build process
   - Deployment pipeline
3. Document current setup
4. Identify pain points

**Output Format:**
```markdown
## Environment Analysis Report

### Current Tooling Stack
| Tool | Version | Purpose | Config File |
|------|---------|---------|-------------|
{{tooling_stack}}

### Configuration Files
```
{{config_files}}
```

### Dependency Analysis
```
{{dependency_tree}}
```

### Build Process
```mermaid
graph TD
{{build_graph}}
```

### Deployment Pipeline
{{deployment_pipeline}}

### Pain Points Identified
1. **{{pain1}}**
   - **Impact:** {{impact1}}
   - **Current Workaround:** {{workaround1}}
   
2. **{{pain2}}**
   - **Impact:** {{impact2}}
   - **Current Workaround:** {{workaround2}}

### Performance Metrics
- **Build Time:** {{build_time}}
- **Test Time:** {{test_time}}
- **Deploy Time:** {{deploy_time}}
- **CI/CD Duration:** {{cicd_duration}}
```

---

### Phase 2: Task Execution (Subagents 2-{{num_agents}})
**Objective:** Execute assigned tooling tasks

**Instructions for each Subagent:**
1. You are assigned: `{{assigned_task}}`
2. Execute with caution:
   - Backup before changes
   - Test in isolation when possible
   - Document all changes
3. For changes:
   - Explain what was changed
   - Why it was changed
   - Impact of the change
4. For installations:
   - Document exact commands
   - Note version installed
   - Verify compatibility

**Safety Rules:**
- ❌ Do NOT run `rm -rf` or similar destructive commands
- ❌ Do NOT modify production configs without backup
- ✅ DO test changes in development first
- ✅ DO document rollback procedures

**Output Format:**
```markdown
## Task Execution: {{assigned_task}}

### Pre-Execution Checklist
- [x] Backups created
- [x] Current state documented
- [x] Impact analysis complete
- [x] Rollback plan ready

### Execution Steps
1. **Step 1:** {{step1}}
   ```bash
   {{step1_command}}
   ```
   **Result:** {{step1_result}}
   
2. **Step 2:** {{step2}}
   ```bash
   {{step2_command}}
   ```
   **Result:** {{step2_result}}

### Changes Made
| File | Change | Reason | Impact |
|------|--------|--------|--------|
{{changes_table}}

### Verification
- **Tests Passed:** {{tests_passed}} / {{tests_total}}
- **Build Status:** {{build_status}}
- **Deployment Test:** {{deploy_test}}

### Issues Encountered
{{issues_encountered}}

### Rollback Information
- **Rollback Command:** {{rollback_command}}
- **Time to Rollback:** {{rollback_time}}
- **Data Loss Risk:** {{data_loss_risk}}
```

---

### Phase 3: Integration & Testing (Subagent {{integration_agent}})
**Objective:** Test tooling changes in integrated environment

**Instructions:**
1. Verify all changes work together
2. Test:
   - Local development
   - Build process
   - Test suite
   - Deployment (staging if available)
3. Check for:
   - Broken dependencies
   - Version conflicts
   - Performance regressions
   - Security issues
4. Document test results

**Output Format:**
```markdown
## Integration & Testing Report

### Integration Status
- **All Changes Integrated:** {{integration_status}}
- **Conflicts Found:** {{conflict_count}}
- **Conflicts Resolved:** {{conflict_resolved}}

### Test Results

#### Local Development
- **Status:** {{local_status}}
- **Issues:** {{local_issues}}
- **Time to Start:** {{start_time}}

#### Build Process
- **Status:** {{build_status}}
- **Duration:** {{build_duration}}
- **Errors:** {{build_errors}}
- **Warnings:** {{build_warnings}}

#### Test Suite
- **Tests Run:** {{tests_run}}
- **Passed:** {{tests_passed}}
- **Failed:** {{tests_failed}}
- **Success Rate:** {{test_success_rate}}%

#### Deployment Test
- **Status:** {{deploy_status}}
- **Duration:** {{deploy_duration}}
- **Errors:** {{deploy_errors}}

### Performance Comparison
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Build Time | {{build_before}} | {{build_after}} | {{build_change}} |
| Test Time | {{test_before}} | {{test_after}} | {{test_change}} |
| Bundle Size | {{bundle_before}} | {{bundle_after}} | {{bundle_change}} |

### Security Scan
- **Vulnerabilities Found:** {{vuln_count}}
- **Severity Distribution:**
  - Critical: {{critical_vulns}}
  - High: {{high_vulns}}
  - Medium: {{medium_vulns}}
  - Low: {{low_vulns}}

### Compatibility Check
- **Node.js Version:** {{node_version}} (Required: {{node_required}})
- **OS Compatibility:** {{os_compat}}
- **Dependency Conflicts:** {{dep_conflicts}}
```

---

### Phase 4: Documentation (Subagent {{doc_agent}})
**Objective:** Document all changes and create user guides

**Instructions:**
1. Create/update documentation for:
   - Installation instructions
   - Configuration options
   - Usage examples
   - Troubleshooting guide
2. Document:
   - What changed
   - Why it changed
   - How to use new features
   - Migration guide (if applicable)
3. Create runbooks for common operations

**Output Format:**
```markdown
## Documentation Report

### Documentation Created/Updated
| Document | Type | Location | Status |
|----------|------|----------|--------|
{{docs_table}}

### Installation Guide
```markdown
{{installation_guide}}
```

### Configuration Reference
```yaml
{{configuration_example}}
```

### Usage Examples
```bash
# Example 1: {{example1_name}}
{{example1_command}}

# Example 2: {{example2_name}}
{{example2_command}}
```

### Troubleshooting Guide

#### Common Issues
1. **{{issue1}}**
   - **Cause:** {{cause1}}
   - **Solution:** {{solution1}}
   
2. **{{issue2}}**
   - **Cause:** {{cause2}}
   - **Solution:** {{solution2}}

### Migration Guide (if applicable)
{{migration_guide}}

### Changelog Entry
```
{{changelog_entry}}
```
```

---

### Phase 5: Final Report (Subagent {{report_agent}})
**Objective:** Create comprehensive tooling report

**Instructions:**
1. Aggregate all tooling changes
2. Calculate impact metrics
3. Create rollback plan
4. Document lessons learned

**Output Format:**
```markdown
# {{tooling_type}} Tooling - Final Report

## Executive Summary

**Date:** {{date}}
**Objective:** {{objective}}
**Status:** {{status}}

### Overall Impact
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Build Time | {{build_before}} | {{build_after}} | {{build_improvement}}% |
| Test Success | {{test_before}}% | {{test_after}}% | {{test_improvement}}% |
| Deployment Time | {{deploy_before}} | {{deploy_after}} | {{deploy_improvement}}% |
| Developer Experience | {{dx_before}}/10 | {{dx_after}}/10 | {{dx_improvement}} |

## Changes Summary

### Tools Added/Updated
| Tool | Version | Purpose | Impact |
|------|---------|---------|--------|
{{tools_added}}

### Tools Removed
| Tool | Reason | Replacement | Savings |
|------|--------|-------------|---------|
{{tools_removed}}

### Configuration Changes
{{config_changes}}

## Files Modified

### Configuration Files
```
{{config_files_changed}}
```

### Code Files
```
{{code_files_changed}}
```

### Documentation Files
```
{{doc_files_changed}}
```

## Test Results

### Before Changes
- **Tests:** {{tests_before_total}}
- **Passed:** {{tests_before_passed}}
- **Failed:** {{tests_before_failed}}
- **Coverage:** {{coverage_before}}%

### After Changes
- **Tests:** {{tests_after_total}}
- **Passed:** {{tests_after_passed}}
- **Failed:** {{tests_after_failed}}
- **Coverage:** {{coverage_after}}%

## Performance Impact

### Build Performance
```
{{build_performance}}
```

### Runtime Performance
```
{{runtime_performance}}
```

## Security Impact

### Vulnerabilities
- **Before:** {{vulns_before}}
- **After:** {{vulns_after}}
- **Fixed:** {{vulns_fixed}}
- **New:** {{vulns_new}}

### Security Score
- **Before:** {{security_before}}/10
- **After:** {{security_after}}/10

## Rollback Plan

### If Something Goes Wrong

#### Automatic Rollback
```bash
{{automatic_rollback}}
```

#### Manual Rollback Steps
1. {{rollback_step1}}
2. {{rollback_step2}}
3. {{rollback_step3}}

#### Estimated Rollback Time
- **Time:** {{rollback_time_estimate}}
- **Data Loss:** {{data_loss_estimate}}
- **Downtime:** {{downtime_estimate}}

## Lessons Learned

### What Went Well
✅ {{success1}}
✅ {{success2}}
✅ {{success3}}

### Challenges Faced
⚠️ {{challenge1}}
⚠️ {{challenge2}}

### Improvements for Next Time
💡 {{improvement1}}
💡 {{improvement2}}

## Recommendations

### Immediate Actions
- [ ] {{action1}}
- [ ] {{action2}}

### Short-term Improvements
- [ ] {{improvement_short1}}
- [ ] {{improvement_short2}}

### Long-term Strategy
- [ ] {{strategy1}}
- [ ] {{strategy2}}

## Next Steps
1. Deploy changes to production (if approved)
2. Monitor for issues
3. Schedule follow-up review
4. Update team documentation

---

**Tooling Success:** {{success_assessment}}
**Recommendation:** {{final_recommendation}}
```
