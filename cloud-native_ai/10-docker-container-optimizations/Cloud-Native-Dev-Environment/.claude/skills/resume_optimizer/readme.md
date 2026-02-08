![Banner](./header.jpg)

````md
# linkedin_job_resume_optimizer

## Overview

`linkedin_job_resume_optimizer` is an agentic skill designed to bridge the gap between **LinkedIn job market demand** and a candidate’s **existing professional profile**.  
It automates job discovery, resume optimization, interview preparation, and LinkedIn profile alignment — while strictly maintaining **truthfulness and professional integrity**.

The skill is intended for candidates who want to:
- Target relevant roles efficiently
- Optimize resumes for ATS and recruiter expectations
- Prepare for interviews with role-specific questions
- Improve LinkedIn profiles to match real market signals

---

## Core Features

### 1. LinkedIn Job Discovery
- Searches LinkedIn for roles aligned with the candidate’s background
- Identifies high-relevance positions based on skills, experience, and role keywords
- Can prioritize filters such as:
  - Remote vs on-site
  - Location (e.g., US, EU, global)
  - Seniority level
  - Industry/domain

---

### 2. Resume Optimization (Honest Alignment)
- Analyzes job descriptions and extracts:
  - Required skills
  - Preferred skills
  - Keywords and role language
- Optimizes the provided resume to:
  - Improve ATS keyword matching
  - Align phrasing with job requirements
  - Highlight relevant achievements
- **Does NOT fabricate experience or skills**
- Preserves factual accuracy and professional credibility

---

### 3. Interview Question Generation
- Generates role-specific interview questions based on:
  - Job descriptions
  - Optimized resume content
- Covers:
  - Technical questions
  - Behavioral questions
  - Scenario-based and situational questions
- Helps candidates prepare with realistic expectations

---

### 4. LinkedIn Profile Optimization
- Recommends updates for:
  - Headline
  - About/Summary section
  - Experience descriptions
  - Skills section
- Aligns profile language with:
  - Target roles
  - Resume updates
  - Current market terminology
- Focuses on recruiter and hiring-manager visibility

---

## Inputs

- Resume file (local path, e.g. `.docx`)
- Candidate context (implicit or explicit)
- Optional constraints (role type, geography, seniority, etc.)

---

## Outputs

- Shortlist of relevant LinkedIn roles
- Optimized resume content (truthful and role-aligned)
- Targeted interview questions
- Actionable LinkedIn profile update suggestions

---

## Usage Instructions

When using this skill:
1. Clearly specify the resume file path.
2. Allow the skill to first identify suitable roles.
3. Ensure optimization is **truthful and experience-based**.
4. Optionally constrain scope (e.g., number of roles, geography).

---

## Usage Examples

### Example 1 — End-to-end optimization
```text
Use the linkedin_job_resume_optimizer skill to find relevant LinkedIn roles, optimize the resume at
/mnt/d/path/to/resume.docx to honestly match required skills, then generate interview questions and LinkedIn profile update suggestions.
````

---

### Example 2 — Role-focused optimization

```text
Using linkedin_job_resume_optimizer, target remote senior product roles, optimize the resume at
/mnt/d/path/to/resume.docx for ATS alignment, and prepare role-specific interview questions.
```

---

### Example 3 — LinkedIn-first strategy

```text
Search for suitable LinkedIn jobs using linkedin_job_resume_optimizer, then recommend LinkedIn profile headline and summary updates based on the identified roles and existing resume.
```

---

## Design Principles

* **Truth over inflation**: No fabricated skills or experience
* **Market-driven**: Optimization reflects real job requirements
* **Reusable**: Suitable for iterative job searches
* **ATS-aware**: Language and structure optimized for screening systems

---

## Intended Use Cases

* Job seekers targeting competitive roles
* Career pivots requiring language alignment (not skill fabrication)
* Resume refinement for ATS-heavy hiring pipelines
* LinkedIn profile modernization

---

## Notes

This skill is designed to be used iteratively.
As market conditions or target roles change, the process can be repeated with updated constraints or resumes.

---

```

---

### Next optional upgrades (if you want)
- Add a **limitations section** (what the skill explicitly does not do)
- Add a **privacy & data handling note**
- Convert this into a **README.md** with badges and diagrams
- Generate a **`claude.md` instruction block** that enforces honest optimization

Tell me the next enhancement you want.
```
