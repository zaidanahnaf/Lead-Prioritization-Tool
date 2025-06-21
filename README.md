# LeadQualiScore: A Lightweight Lead Scoring & Validation Tool

This tool was developed for Caprae Capital's internship challenge to simulate an intelligent lead prioritization layer on top of data outputs from SaaSquatchLeads.com. 

It evaluates leads based on business relevance and data completeness, helping operators focus on outreach-worthy targets. Built entirely within a 5-hour code window.

---

## 🚀 Purpose

While SaaSquatchLeads enriches business data across multiple sources, many lead outputs remain noisy, incomplete, or hard to qualify. 

This tool helps answer:  
**"Which leads are worth pursuing first?"**

By assigning scores and quality flags, it brings clarity and speed into the lead selection process.

---

## 🧠 Key Features

- ✅ **Lead Scoring System**  
  Ranks leads from 0–100 based on:
  - Industry fit (e.g. SaaS, FinTech, etc.)
  - Company size (employee count)
  - Estimated revenue
  - Title seniority (CEO, Founder, etc.)
  - Data availability (email, LinkedIn)

- 🛑 **Data Integrity Flags**  
  Flags incomplete or questionable fields such as:
  - Missing owner email or name
  - Zero employees + high revenue
  - Blank company LinkedIn

- 🔍 **Interactive UI (Streamlit)**  
  - Upload your enriched leads CSV
  - Filter leads by score, industry, or flags
  - Export cleaned, prioritized results

```

LeadQualiScore/
│
├── app/                   # Main code
│   ├── main.py            # Streamlit app
│   ├── utils.py           # Scoring & validator functions
│   └── sample_leads.csv   # Dummy data
│
├── notebook/              # Jupyter walkthrough
│   └── demo.ipynb
│
├── LICENSE
├── README.md              # Guide
├── report.md              # 1-pager for Caprae
├── requirements.txt       # Dependencies
└── .gitignore

```

---

## ⚙️ How to Run

1. Clone this repo:
```bash
git clone https://github.com/zaidanahnaf/leadqualiscore.git
cd leadqualiscore

pip install -r requirements.txt

streamlit run app/main.py
```

---

## 🧪 Demo Dataset
If you don’t have access to real enriched data, you can use the included `sample_leads.csv` for simulation.

## 📹 Video Walkthrough
[]()

---

## 🧠 Tech Stack
- Python
- Pandas
- Streamlit
- Regex
- scikit-learn (for future upgrade to ML model)

---

## 🔄 Upgrade Path
While this version uses rule-based scoring for speed and clarity, it is designed to be model-ready. The logic can easily be replaced with a supervised classifier trained on historical outreach results.

---

## ⚠️ Usage Disclaimer

This tool was developed under a time constraint as part of a technical interview challenge.  
All logic and design decisions belong to the author.

Please do not reproduce, commercialize, or reuse without permission.  
© 2025 Dhafa Zaidan Ahnaf

---

## 🙋 About the Author
Dhafa Zaidan Ahnaf
Machine Learning Engineer Intern Applicant
[LinkedIn](https://www.linkedin.com/in/dhafazaidan/)
