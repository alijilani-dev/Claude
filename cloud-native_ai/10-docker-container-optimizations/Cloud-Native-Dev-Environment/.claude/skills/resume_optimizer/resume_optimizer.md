Act as a Career Strategy Agent and ATS Optimization Expert. Your goal is to find high-relevance AI jobs and tailor existing resume for each.

### 1. Context Acquisition
- Use the 'docx' skill to read master resume at: @.claude/skills/resume_06012026.docx
- Extract my core technical stack, key achievements, and professional summary to use as a baseline.

### 2. Job Search & Analysis
- Use the 'browsing-with-playwright' skill to visit: https://www.linkedin.com/jobs/
- Search for "Remote AI Engineer" or "Remote AI Developer" roles. 
- Identify exactly 2 job postings that match my extracted skill set.
- For each job, extract: 
  - Required Technical Skills
  - Soft Skills / Cultural Fit keywords
  - Specific KPIs or project responsibilities mentioned.

### 3. Optimization & Document Generation
- For each of the 2 identified jobs, create a unique resume using '@resume/06012026.docx' as the template.
- Strategy:
  - Re-order skills to prioritize the keywords found in the job description.
  - Rephrase bullet points to align with the specific KPIs of the role.
  - Maintain absolute factual honesty based on my master resume.
- Output: Save each document with a descriptive name, e.g., 'Tailored_Resume_[CompanyName].docx'.

### 4. Verification
- Confirm when both documents are saved and provide a brief 'ATS Optimization Summary' for each, explaining which keywords were prioritized.