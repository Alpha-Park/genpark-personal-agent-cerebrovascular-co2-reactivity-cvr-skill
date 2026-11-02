---
name: genpark-personal-agent-cerebrovascular-co2-reactivity-cvr-skill
description: Deterministic evaluation of cerebrovascular CO2 reactivity (CVR), Transcranial Doppler Breath-Holding Index (BHI), and cerebral microvascular reserve.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Cerebrovascular CO2 Reactivity (CVR) & Breath-Holding Index Skill

## Overview
The `genpark-personal-agent-cerebrovascular-co2-reactivity-cvr-skill` delivers neurovascular compliance analytics to sovereign personal agents. Cerebral arterioles dilate in response to hypercapnia (elevated arterial $PCO_2$) to protect cortical perfusion. The Breath-Holding Index (BHI), measured via middle cerebral artery Transcranial Doppler (TCD) ultrasonography during voluntary apnea, quantifies cerebral vasomotor reserve. Blunted reactivity signals microvascular rarefaction, endothelial dysfunction, and increased ischemic risk.

## Physiological Model & Mathematics
1. **Breath-Holding Index ($BHI$)**:
   $$BHI = \frac{CBFv_{\text{hypercapnia}} - CBFv_{\text{baseline}}}{CBFv_{\text{baseline}}} \times \frac{100}{\Delta T_{\text{apnea}}} \quad (\%/\text{second})$$
   - **Normal Vasomotor Reserve**: $BHI \ge 1.20\%/\text{s}$.
   - **Borderline Reactivity**: $0.70 - 1.19\%/\text{s}$.
   - **Impaired Vasomotor Reserve**: $< 0.69\%/\text{s}$.
2. **Cerebrovascular Vasomotor Reserve Index ($CVRI$)**:
   Translates BHI slope into a standardized 0 to 100 neurovascular health metric.

## Tools & Endpoints
- `calculate_breath_holding_index`: Computes percentage velocity surge, BHI rate (%/s), and cerebrovascular reserve score.
