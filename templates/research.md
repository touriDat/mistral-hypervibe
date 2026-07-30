# Research Task Template

## Task Description
**Research Type:** {{research_type}}
**Topic:** {{topic}}
**Scope:** {{scope}}
**Depth:** {{depth_level}} (shallow/medium/deep)

## Subagent Instructions

### Phase 1: Source Discovery (Subagent 1)
**Objective:** Identify relevant sources for research

**Instructions:**
1. Analyze the topic: `{{topic}}`
2. Identify relevant sources:
   - Official documentation
   - Community resources (GitHub, forums)
   - Blog posts/tutorials
   - API specifications
   - Related libraries/tools
3. Prioritize sources by relevance and authority
4. Filter out outdated or unreliable sources

**Output Format:**
```markdown
## Sources for: {{topic}}

### Tier 1: Official Documentation (Priority: ⭐⭐⭐⭐⭐)
1. [{{source1_title}}]({{source1_url}}) - {{source1_description}}
2. [{{source2_title}}]({{source2_url}}) - {{source2_description}}

### Tier 2: Community Resources (Priority: ⭐⭐⭐⭐)
1. [{{source3_title}}]({{source3_url}}) - {{source3_description}}
2. [{{source4_title}}]({{source4_url}}) - {{source4_description}}

### Tier 3: Blog Posts/Articles (Priority: ⭐⭐⭐)
{{tier3_sources}}

### Tier 4: Other (Priority: ⭐⭐)
{{tier4_sources}}

### Excluded Sources
{{excluded_sources}}

### Search Queries Used
{{search_queries}}
```

---

### Phase 2: Content Extraction (Subagents 2-{{num_extraction_agents}})
**Objective:** Extract and summarize information from assigned sources

**Instructions for each Subagent:**
1. You are assigned sources: `{{assigned_sources}}`
2. For each source:
   - Read/comprehend the content
   - Extract key information relevant to: `{{topic}}`
   - Identify important code examples, concepts, best practices
   - Note any contradictions or opinions
3. Create structured summary

**Focus Areas for {{research_type}}:**
{{focus_areas}}

**Output Format:**
```markdown
## Content Summary: {{assigned_sources}}

### Key Concepts
1. **{{concept1}}**
   - {{concept1_description}}
   - **Relevance:** {{concept1_relevance}}/10
   
2. **{{concept2}}**
   - {{concept2_description}}
   - **Relevance:** {{concept2_relevance}}/10

### Code Examples
```{{language}}
{{code_example1}}
```

### Best Practices
{{best_practices}}

### Warnings/Contraindications
{{warnings}}

### Open Questions
{{open_questions}}

### Source Reliability
- **Authority:** {{authority_score}}/10
- **Currency:** {{currency_score}}/10 (Last updated: {{last_updated}})
- **Bias:** {{bias_notes}}
```

---

### Phase 3: Cross-Referencing (Subagent {{crossref_agent}})
**Objective:** Cross-reference findings from all sources

**Instructions:**
1. Compare findings from all content extraction agents
2. Identify:
   - Contradictions between sources
   - Overlapping information
   - Gaps in coverage
3. Resolve contradictions (note which source is more authoritative)
4. Create unified knowledge base

**Output Format:**
```markdown
## Cross-Reference Analysis

### Contradictions Found
| Topic | Source A | Source B | Resolution |
|-------|----------|----------|------------|
{{contradictions}}

### Consensus Points
{{consensus_points}}

### Coverage Gaps
{{coverage_gaps}}

### Unified Knowledge
{{unified_knowledge}}
```

---

### Phase 4: Synthesis & Recommendations (Subagent {{synthesis_agent}})
**Objective:** Synthesize research into actionable recommendations

**Instructions:**
1. Combine all validated information
2. Create structured guide/recommendation
3. Prioritize by importance/relevance
4. Include practical examples

**Output Format for {{research_type}}:**
```markdown
# {{topic}} - Research Synthesis

## Quick Answer
{{quick_answer}}

## Deep Dive

### {{section1_title}}
{{section1_content}}

### {{section2_title}}
{{section2_content}}

## Comparison Matrix (if applicable)
| Feature | Option A | Option B | Recommendation |
|---------|----------|----------|----------------|
{{comparison_matrix}}

## Best Practices
1. **{{practice1}}**
   {{practice1_details}}
   
2. **{{practice2}}**
   {{practice2_details}}

## Common Pitfalls
⚠️ **{{pitfall1}}**
{{pitfall1_details}}

⚠️ **{{pitfall2}}**
{{pitfall2_details}}

## Recommended Approach
{{recommended_approach}}

## Implementation Example
```{{language}}
{{implementation_example}}
```

## Further Reading
- [{{resource1}}]({{resource1_url}}) - {{resource1_desc}}
- [{{resource2}}]({{resource2_url}}) - {{resource2_desc}}

## Sources Cited
{{sources_cited}}
```
