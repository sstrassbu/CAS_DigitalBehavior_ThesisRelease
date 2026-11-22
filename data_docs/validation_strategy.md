# Validation Strategy

This file documents planned checks for data validity, construct validity, interpretive validity, model comparison, and generalizability.
This document defines how validation will be approached in the project.

## Why this matters

Several models may produce similar observable outputs while relying on different hidden assumptions. Validation therefore needs to go beyond predictive performance alone.

## Validation layers

### 1. Data validity
Questions:
- Are timestamps parsed correctly?
- Are IDs consistent?
- Are intervention variables reliable?
- Are key variables missing or malformed?

### 2. Construct validity
Questions:
- Are theoretical constructs mapped to measured variables in a defensible way?
- Are proxies clearly distinguished from direct observations?
- Are low-confidence mappings labeled as such?

### 3. Behavioral validity
Questions:
- Do the derived summaries and model outputs resemble plausible smartphone behavior?
- Do app-transition structures match empirical patterns?
- Do intervention-response summaries reflect meaningful behavioral variation?

### 4. Interpretive validity
Questions:
- Are labels such as “noise-dominated” or “hub-dependent” psychologically interpretable?
- Do model-derived dimensions align with meaningful behavioral descriptions?

### 5. Model comparison
Questions:
- Which models explain which types of behavioral patterns best?
- Do multiple models fit similar outputs?
- Where does identifiability become a problem?

### 6. Generalizability
Questions:
- Do findings transfer across datasets?
- Do phenotype dimensions remain stable across contexts?
- Are results app-specific or broader?

## Immediate validation tasks

- validate cleaned datasets after preprocessing
- validate harmonization decisions
- audit proxy mappings
- create sanity-check reports for first feature sets

## Later validation tasks

- compare model outputs across frameworks
- evaluate phenotype stability
- assess robustness across datasets and intervention contexts