<div align="center">

# 🧞 DAXGenie

### AI-powered DAX formula assistant for Power BI analysts

*Generate complex DAX formulas from plain English. Explain existing formulas in seconds. Free & open source.*

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-daxgenie--sreeja.streamlit.app-1d4ed8?style=for-the-badge)](https://daxgenie-sreeja.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/AI-Google_Gemini_2.5-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[🌐 Try the Live Demo](https://daxgenie-sreeja.streamlit.app)** · **[💼 Connect on LinkedIn](https://www.linkedin.com/in/kotha-sreeja)** · **[⭐ Star this Repo](https://github.com/sreeja1105/daxgenie)**

</div>

---

## 🎯 What is DAXGenie?

DAXGenie is a free, open-source AI assistant built to help **Power BI analysts** work faster with DAX formulas — without paying for enterprise licenses.

If you've ever stared at a DAX formula trying to understand what it does, or struggled to write one for a specific business question, DAXGenie is for you.

### 🌟 Two Powerful Modes

🔹 **Generate Mode** — Describe a calculation in plain English. Get a working DAX formula with explanation.

🔹 **Explain Mode** — Paste an existing DAX formula. Get a step-by-step breakdown of what it does and how it works.

---

## 📸 See It In Action

### Generate Mode — Plain English to DAX

> *"Year-over-year sales growth percentage, only counting weekdays"*

DAXGenie generates a proper `VAR / RETURN` structure with `SAMEPERIODLASTYEAR`, weekday filtering, and `DIVIDE` for safe division — exactly how a senior analyst would write it.

<img width="724" height="883" alt="Screenshot 2026-06-04 081346" src="https://github.com/user-attachments/assets/d49a72a4-d2ab-4978-98fe-a0aad4b2b31e" />


### Explain Mode — DAX to Plain English

> Paste: `CALCULATE(SUM(Sales[Amount]), DATEADD(Calendar[Date], -1, YEAR))`

DAXGenie walks through every function, explains filter context, and shows the business meaning.

<img width="801" height="848" alt="Screenshot 2026-06-04 081241" src="https://github.com/user-attachments/assets/175f2c73-dc2b-44c6-9d4a-8589d91d6205" />


---

## ✨ Features

- 🎯 **DAX Generation** — Plain English → working DAX formulas with comments
- 🔍 **DAX Explanation** — Step-by-step breakdown of existing formulas
- 💡 **Best Practices Built-in** — Suggestions follow Power BI / DAX conventions (Calendar tables, VAR/RETURN, DIVIDE)
- ⚠️ **Pitfall Warnings** — Highlights common DAX mistakes
- 🌐 **100% Free** — No subscription, no API costs for users
- 🔓 **Open Source** — Fork it, extend it, contribute back

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend** | Python 3.12 |
| **AI Model** | Google Gemini 2.5 Flash |
| **Deployment** | Streamlit Community Cloud |
| **License** | MIT |

---

## 🚀 Run Locally

Want to run DAXGenie on your own machine? It takes 3 minutes.

### Prerequisites
- Python 3.10+
- A free [Google Gemini API key](https://aistudio.google.com/apikey)

### Setup

```bash
# Clone the repo
git clone https://github.com/sreeja1105/daxgenie.git
cd daxgenie

# Create virtual environment
python -m venv venv
source venv/bin/activate    # Mac/Linux
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
echo "GEMINI_API_KEY=your-key-here" > .env

# Run the app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 💡 Why DAXGenie?

Most BI analysts spend hours wrestling with DAX. Microsoft Copilot is great but locked behind enterprise licenses.

DAXGenie was built to bridge the gap — bringing modern AI to the daily workflow of every Power BI analyst, for free.

It's also a demonstration of how Power BI expertise and AI engineering can come together to solve real problems.

---

## 👩‍💻 About the Author

<div align="center">

### **Kotha Sreeja**
*Microsoft Certified Power BI Data Analyst*  
*MSc Business Analytics & Data Science*

Software engineer with 3+ years of experience in Python backend, SQL, full-stack development, and modern data tooling. Currently focused on the intersection of Business Intelligence and AI engineering.

**[🔗 LinkedIn](https://www.linkedin.com/in/kotha-sreeja)** &nbsp;&nbsp;·&nbsp;&nbsp; **[🔗 GitHub](https://github.com/sreeja1105)**

</div>

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for features, find a bug, or want to improve the prompts:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

You're free to use, modify, and distribute this project. If you build something cool with it, I'd love to hear about it!

---

## ⭐ Show Your Support

If DAXGenie helped you, please consider:

- ⭐ **Starring this repo** on GitHub
- 🔗 **Sharing it** with other Power BI analysts
- 💬 **Connecting with me** on [LinkedIn](https://www.linkedin.com/in/kotha-sreeja)
- 🐛 **Reporting bugs** or suggesting features via [Issues](https://github.com/sreeja1105/daxgenie/issues)

---

<div align="center">

**Made for the Power BI community by [Kotha Sreeja](https://www.linkedin.com/in/kotha-sreeja)** 🧞

</div>
