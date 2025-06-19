# LeadQualiScore: Smart Lead Scoring & Validator for SaaSquatchLeads

A lightweight tool designed to enhance the lead qualification experience for SaaSquatchLeads users by scoring and validating enriched company data. Built within 5 hours as part of Caprae Capital's pre-work challenge.

---

## 🚀 Purpose

SaaSquatchLeads delivers enriched lead data through scraping and API aggregation. However, many leads suffer from incomplete or inconsistent enrichment, such as missing employee counts, invalid emails, or unclear business type.

This tool addresses that gap by:
- Scoring each lead based on business relevance and data completeness
- Flagging incomplete or risky leads
- Empowering users to filter and export high-quality leads only

---

## 💡 Key Features

- ✅ **Smart Lead Scoring**: Assigns each lead a score (0–10) based on:
  - Industry match
  - Revenue presence
  - Valid employee count
  - Business type clarity
  - Enrichment completeness

- ⚠️ **Data Integrity Validator**:
  - Detects suspicious fields (e.g. “Employees = 0” + “Revenue = $4.7B”)
  - Flags empty or vague descriptions like “Expertise not mentioned”

- 📊 **Interactive UI with Streamlit**:
  - Upload CSV
  - View & filter leads by score or flags
  - Export refined leads for outreach

---

## 📁 Project Structure

LeadQualiScore/
│
├── app/                   # Kode utama
│   ├── main.py            # Streamlit app
│   ├── utils.py           # Scoring & validator functions
│   └── sample_leads.csv   # Dummy data
│
├── notebook/              # (optional) Jupyter walkthrough
│   └── demo.ipynb
│
├── README.md              # Petunjuk penggunaan
├── report.md              # 1-pager untuk Caprae
├── requirements.txt       # Dependencies
└── .gitignore


---

## ⚙️ How to Run

1. Clone repo:
```bash
git clone https://github.com/yourusername/leadqualiscore.git
cd leadqualiscore

pip install -r requirements.txt

streamlit run app/main.py
```
