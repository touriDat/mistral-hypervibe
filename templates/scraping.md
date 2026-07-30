# Scraping Task Template

## Task Description
**Scraping Type:** {{scraping_type}}
**Targets:** {{targets}}
**Data to Extract:** {{extraction_targets}}
**Output Format:** {{output_format}}

## Subagent Instructions

### Phase 1: Target Analysis (Subagent 1)
**Objective:** Analyze scraping targets

**Instructions:**
1. Analyze targets: `{{targets}}`
2. For each target:
   - Determine type (website, API, file, etc.)
   - Check for rate limits/robots.txt
   - Identify authentication requirements
   - Estimate data volume
   - Check for anti-scraping measures
3. Select appropriate tools:
   - Simple HTML: cheerio
   - Dynamic content: puppeteer/playwright
   - API: direct fetch
   - Files: fs/stream

**Output Format:**
```markdown
## Target Analysis Report

### Targets Summary
| # | Target | Type | Auth Required | Rate Limited | Anti-Scraping |
|---|--------|------|---------------|--------------|---------------|
{{targets_table}}

### Tool Recommendations
- **Primary Tool:** {{primary_tool}}
- **Fallback Tool:** {{fallback_tool}}
- **Alternative Tools:** {{alternative_tools}}

### Risk Assessment
- **Legal Risk:** {{legal_risk}} (Check terms of service)
- **Technical Risk:** {{technical_risk}} (Rate limits, blocks)
- **Ethical Risk:** {{ethical_risk}} (Respectful scraping)

### Rate Limit Analysis
{{rate_limit_analysis}}

### Authentication Requirements
{{auth_requirements}}
```

---

### Phase 2: Scraping Execution (Subagents 2-{{num_scraping_agents}})
**Objective:** Execute scraping on assigned targets

**Instructions for each Subagent:**
1. You are assigned targets: `{{assigned_targets}}`
2. Use tool: {{tool}}
3. For each target:
   - Respect robots.txt
   - Implement delays between requests ({{delay_ms}}ms)
   - Handle errors gracefully
   - Retry on failures (max {{max_retries}} attempts)
   - Extract data: {{extraction_targets}}
4. Store raw data for validation

**Scraping Rules:**
- **Max requests per second:** {{requests_per_second}}
- **Timeout:** {{timeout_ms}}ms
- **User-Agent:** {{user_agent}}
- **Headers:** {{headers}}

**Output Format:**
```markdown
## Scraping Results: {{assigned_targets}}

### Summary
- **Targets Scraped:** {{targets_scraped}}
- **Requests Made:** {{requests_made}}
- **Data Extracted:** {{data_count}} items
- **Success Rate:** {{success_rate}}%
- **Duration:** {{duration}}

### Extracted Data
```json
{{extracted_data}}
```

### Issues Encountered
| # | Target | Issue | Status | Solution |
|---|--------|-------|--------|----------|
{{issues_table}}

### Statistics
- **Average Request Time:** {{avg_time}}ms
- **Total Data Size:** {{data_size}}
- **Duplicates Found:** {{duplicates}}

### Quality Metrics
- **Data Completeness:** {{completeness}}%
- **Data Accuracy:** {{accuracy}}% (estimated)
- **Error Rate:** {{error_rate}}%
```

---

### Phase 3: Data Validation (Subagent {{validation_agent}})
**Objective:** Validate extracted data

**Instructions:**
1. Validate all extracted data against schema: `{{schema}}`
2. Check for:
   - Missing required fields
   - Data type mismatches
   - Duplicate entries
   - Inconsistent data
   - Outliers/errors
3. Clean data where possible
4. Flag invalid entries for review

**Output Format:**
```markdown
## Data Validation Report

### Schema Compliance
- **Valid Items:** {{valid_count}} ({{valid_percent}}%)
- **Invalid Items:** {{invalid_count}} ({{invalid_percent}}%)
- **Partially Valid:** {{partial_count}} ({{partial_percent}}%)

### Validation Issues

#### ❌ Invalid Items ({{invalid_count}})
| # | Item | Issue | Field | Value |
|---|------|-------|-------|-------|
{{invalid_items}}

#### ⚠️ Partially Valid Items ({{partial_count}})
{{partial_items}}

#### ✅ Valid Items ({{valid_count}})
- Sample: {{valid_sample}}

### Data Quality Metrics
| Metric | Value | Target |
|--------|-------|--------|
| Completeness | {{completeness_score}}% | 100% |
| Uniqueness | {{uniqueness_score}}% | 100% |
| Consistency | {{consistency_score}}% | 100% |
| Accuracy | {{accuracy_score}}% | >95% |

### Duplicates Removed
- **Total Duplicates:** {{duplicate_count}}
- **Duplicate Fields:** {{duplicate_fields}}

### Cleaning Actions Performed
{{cleaning_actions}}

### Recommendations
💡 {{recommendation1}}
💡 {{recommendation2}}
```

---

### Phase 4: Data Transformation (Subagent {{transform_agent}})
**Objective:** Transform raw data into desired output format

**Instructions:**
1. Transform validated data from: `{{input_format}}`
2. To desired output: `{{output_format}}`
3. Apply transformations:
   {{transformations}}
4. Validate transformed data
5. Generate output files

**Output Format:**
```markdown
## Data Transformation Report

### Transformations Applied
1. **{{transform1}}**
   - Input: {{transform1_input}}
   - Output: {{transform1_output}}
   - Records Affected: {{transform1_count}}

2. **{{transform2}}**
   - Input: {{transform2_input}}
   - Output: {{transform2_output}}
   - Records Affected: {{transform2_count}}

### Output Files Generated
| File | Format | Records | Size |
|------|--------|---------|------|
{{output_files}}

### Transformation Statistics
- **Input Records:** {{input_count}}
- **Output Records:** {{output_count}}
- **Transformation Time:** {{transform_time}}
- **Success Rate:** {{transform_success_rate}}%

### Validation of Transformed Data
{{transform_validation}}
```

---

### Phase 5: Final Report (Subagent {{report_agent}})
**Objective:** Create comprehensive scraping report

**Instructions:**
1. Aggregate all scraping results
2. Calculate overall statistics
3. Create data summary
4. Generate insights

**Output Format:**
```markdown
# {{scraping_type}} Scraping - Final Report

## Executive Summary

**Scraping Date:** {{date}}
**Duration:** {{total_duration}}
**Subagents Used:** {{subagent_count}}

### Overall Results
| Metric | Value |
|--------|-------|
| Targets Scraped | {{total_targets}} |
| Requests Made | {{total_requests}} |
| Data Extracted | {{total_data}} items |
| Success Rate | {{overall_success_rate}}% |
| Data Quality | {{data_quality_score}}/10 |

## Targets Overview

### Successfully Scraped ({{successful_targets}})
{{successful_targets_list}}

### Partially Scraped ({{partial_targets}})
{{partial_targets_list}}

### Failed Targets ({{failed_targets}})
{{failed_targets_list}}

## Data Summary

### Extracted Data Preview
```json
{{data_preview}}
```

### Data Statistics
- **Total Records:** {{total_records}}
- **Unique Records:** {{unique_records}}
- **Data Fields:** {{field_count}}
- **Average Record Size:** {{avg_record_size}} bytes

### Field Distribution
| Field | Present | Missing | Type | Sample Value |
|-------|---------|---------|------|--------------|
{{field_distribution}}

## Quality Assessment

### Data Quality Score: {{quality_score}}/10

| Category | Score | Notes |
|----------|-------|-------|
| Completeness | {{completeness_score}}/10 | {{completeness_notes}} |
| Uniqueness | {{uniqueness_score}}/10 | {{uniqueness_notes}} |
| Consistency | {{consistency_score}}/10 | {{consistency_notes}} |
| Accuracy | {{accuracy_score}}/10 | {{accuracy_notes}} |

## Performance Metrics

### Scraping Performance
- **Total Execution Time:** {{total_time}}
- **Average Request Time:** {{avg_request_time}}ms
- **Requests per Second:** {{requests_per_second_actual}}
- **Error Rate:** {{error_rate}}%

### Resource Usage
- **Memory Used:** {{memory_used}}
- **Disk I/O:** {{disk_io}}
- **Network Transfer:** {{network_transfer}}

## Issues & Challenges

### Technical Issues
{{technical_issues}}

### Data Issues
{{data_issues}}

### Rate Limit Issues
{{rate_limit_issues}}

## Recommendations

### For Next Scraping Session
🔄 {{recommendation1}}
🔄 {{recommendation2}}

### For Data Maintenance
📊 {{maintenance1}}
📊 {{maintenance2}}

### For Improving Quality
✨ {{quality1}}
✨ {{quality2}}

## Output Files

### Generated Files
{{output_files_list}}

### File Locations
- **Raw Data:** {{raw_data_path}}
- **Processed Data:** {{processed_data_path}}
- **Report:** {{report_path}}

## Next Steps
1. Review extracted data
2. Address validation issues
3. Store data in target system
4. Schedule regular updates (if applicable)

---

**Scraping Success:** {{success_assessment}}
```
