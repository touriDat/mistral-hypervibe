# Migration Task Template

## Task Description
**Migration Type:** {{migration_type}}
**Source:** {{source}}
**Target:** {{target}}
**Scope:** {{scope}}
**Files Affected:** {{file_count}} files in {{directories}}

## Subagent Instructions

### Phase 1: Analysis (Subagent 1)
**Objective:** Analyze current patterns and dependencies

**Instructions:**
1. Scan all files in the scope: `{{directories}}`
2. Identify current patterns of `{{source}}`
3. Document dependencies and potential breaking changes
4. Create a migration strategy document
5. Identify files that can be migrated in parallel vs. sequentially

**Output Format:**
```markdown
## Migration Analysis: {{migration_type}}

### Current State
- **Files using {{source}}:** {{file_count}}
- **Main patterns identified:**
  {{patterns_list}}

### Dependencies
{{dependencies}}

### Migration Strategy
1. **Parallelizable files:** {{parallel_files}}
2. **Sequential files (dependencies):** {{sequential_files}}
3. **Risk assessment:** {{risk_level}}

### Estimated Effort
- **Time:** {{estimated_time}}
- **Complexity:** {{complexity_stars}}
```

---

### Phase 2: Migration (Subagents 2-{{num_migration_agents}})
**Objective:** Migrate files in chunks of {{chunk_size}}

**Instructions for each Subagent:**
1. You are responsible for migrating files: `{{files_chunk}}`
2. Follow the migration strategy from Phase 1
3. For each file:
   - Backup the original
   - Apply migration rules
   - Test the migrated code (if possible)
   - Document changes
4. Report:
   - Successfully migrated files
   - Files with issues (and why)
   - Warnings/Notes

**Migration Rules for {{migration_type}}:**
{{migration_rules}}

**Output Format:**
```markdown
## Migration Chunk {{chunk_number}}: {{files_chunk}}

### Successfully Migrated
- [ ] file1.js → file1.ts
- [ ] file2.js → file2.ts

### Issues Encountered
| File | Issue | Status |
|------|-------|--------|
| file3.js | Complex type inference | ⚠️ Needs review |

### Notes
{{notes}}
```

---

### Phase 3: Validation (Subagent {{validation_agent}})
**Objective:** Validate all migrations

**Instructions:**
1. Check all migrated files for:
   - Syntax errors
   - Type errors (if TypeScript)
   - Broken imports
   - Missing dependencies
2. Run available linters/tests
3. Create validation report

**Output Format:**
```markdown
## Migration Validation Report

### Summary
- **Total files:** {{file_count}}
- **Successfully migrated:** {{success_count}}
- **With issues:** {{issue_count}}
- **Not migrated:** {{failed_count}}

### Validation Results

#### ✅ Passed
{{passed_files}}

#### ⚠️ Issues Found
{{issues_found}}

#### ❌ Failed
{{failed_files}}

### Recommendations
{{recommendations}}
```

---

### Phase 4: Final Report (Subagent {{report_agent}})
**Objective:** Create comprehensive migration report

**Instructions:**
1. Aggregate all reports from previous phases
2. Create summary statistics
3. Document lessons learned
4. Provide next steps

**Output Format:**
```markdown
# {{migration_type}} Migration - Final Report

## Executive Summary
- **Started:** {{start_time}}
- **Completed:** {{end_time}}
- **Duration:** {{duration}}
- **Files Processed:** {{file_count}}
- **Success Rate:** {{success_rate}}%

## Statistics
| Metric | Value |
|--------|-------|
| Files migrated | {{success_count}} |
| Files with issues | {{issue_count}} |
| Files failed | {{failed_count}} |
| Subagents used | {{subagent_count}} |
| Estimated tokens | {{token_count}} |

## Issues Summary
{{issues_summary}}

## Files Changed
{{git_diff_summary}}

## Lessons Learned
{{lessons_learned}}

## Next Steps
{{next_steps}}
```
