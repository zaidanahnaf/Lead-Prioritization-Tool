# LeadQualiScore – Interview Submission Report

## Approach

This project was developed as a strategic enhancement to SaaSquatchLeads, aiming to solve two key pain points in enriched lead data:

1. **Lack of prioritization** – All leads are treated equally, regardless of relevance or completeness.
2. **Data inconsistency** – Many enriched results are incomplete, duplicated, or inconsistent across fields.

The goal was to build a lightweight scoring and validation tool that helps users focus on leads with the highest potential business value.

---

## Model Selection

Due to the 5-hour time constraint and to ensure explainability, I opted for a **rule-based scoring model**, structured as a proxy for a future supervised classification system.

The scoring logic mimics the behavior of a trained model by combining multiple business-relevant features into a weighted sum:

| Feature                   | Weight | Rationale                             |
|---------------------------|--------|----------------------------------------|
| Industry match            | 30     | Strong indicator of market fit         |
| Company size              | 5–25   | Larger orgs → higher deal potential    |
| Revenue (parsed)          | 15–25  | Proxy for buying power                 |
| Owner title (C-level)     | 10–20  | Shows decision-maker accessibility     |
| Email / LinkedIn present  | 10+    | Critical for contactability            |

---

## Data Preprocessing

- **Revenue Parsing:** Dollar values like `$4.7M` were normalized into floats.
- **Categorical Normalization:** Text fields like `Industry` and `Owner Title` were lowercased and stripped to avoid mismatch.
- **Missing Handling:** `NaN`, `'N/A'`, and empty strings treated as null.

A sample dataset was used to simulate real output from SaaSquatchLeads, with intentionally mixed-quality entries (missing fields, bad formatting, etc.) to stress-test the tool.

---

## Performance Evaluation

While no predictive ML model was trained, **performance was qualitatively measured** by:

- Distribution of scores across leads
- Presence of clear segmentation between low-, mid-, and high-priority entries
- Detection of incomplete records using flagging logic

A notebook walkthrough was provided (`demo.ipynb`) showing the logic, score distribution plot, and top leads preview.

---

## Rationale & Future Path

This scoring system solves a real bottleneck today: helping sales operators and analysts decide **who to contact first**.  

In the future, this logic can evolve into a data-driven model trained on:
- Email open/reply rates
- Conversion success
- Pipeline velocity by segment

This lays the groundwork for a smarter, ML-enhanced prioritization engine integrated directly into the lead enrichment platform.

---

**Author:** Dhafa Zaidan Ahnaf 
Machine Learning Engineer Intern Applicant – Caprae Capital  
Submission built in < 5 hours as instructed.
