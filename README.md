# DAXGenie

**AI-powered DAX formula assistant for Power BI analysts**

Generate complex DAX formulas from plain English. Explain existing formulas in seconds. Optimize slow DAX for better performance. Free and open source.

**Live demo:** [daxgenie-sreeja.streamlit.app](https://daxgenie-sreeja.streamlit.app)

---

## What is DAXGenie

DAXGenie is a free, open-source AI assistant built to help Power BI analysts work faster with DAX formulas, without paying for enterprise licenses.

Whether you struggle to understand an existing formula, want to write one for a specific business question, or wonder why your measure is slow, DAXGenie addresses each of these problems with a dedicated mode.

---

## Three Modes

**Generate Mode**
Describe a calculation in plain English. Get a working DAX formula with explanation, pitfalls to watch for, and example usage.

**Explain Mode**
Paste an existing DAX formula. Get a step-by-step breakdown of what each function does, the result it returns, and the business use cases it fits.

**Optimize Mode**
Paste a slow or unsafe DAX formula. Get a performance rating, performance issues identified, best practice violations flagged, and an optimized rewrite with explanations of each change.

---

## Live Deployments

DAXGenie runs on two deployment platforms, demonstrating different architectural approaches.

| Platform | Architecture | URL |
|---|---|---|
| Streamlit Community Cloud | Streamlit with direct Gemini API call | [daxgenie-sreeja.streamlit.app](https://daxgenie-sreeja.streamlit.app) |
| Render | Streamlit and FastAPI backend in a Docker container | [daxgenie.onrender.com](https://daxgenie.onrender.com) |

The Streamlit Cloud deployment uses a serverless approach with direct LLM calls, optimized for instant response time.

The Render deployment showcases a production-style architecture with a separated FastAPI backend, demonstrating Docker containerization and microservices patterns.

---

## Features

- DAX generation from plain English with comments and explanations
- DAX explanation with step-by-step function breakdown
- DAX optimization with performance analysis and rewrite suggestions
- Best practices applied (Calendar tables, VAR/RETURN structures, DIVIDE for safe division)
- Pitfall warnings for common DAX mistakes
- Completely free with no user subscription or API costs
- MIT licensed and open to contributions

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python 3.12 with FastAPI |
| AI model | Google Gemini 2.5 Flash |
| Container | Docker |
| CI/CD | GitHub Actions |
| Deployment | Streamlit Community Cloud and Render |
| License | MIT |

---

## Run Locally

DAXGenie can be set up on a local machine in a few minutes.

### Prerequisites

- Python 3.10 or higher
- A free [Google Gemini API key](https://aistudio.google.com/apikey)

### Setup

```
git clone https://github.com/sreeja1105/daxgenie.git
cd daxgenie

python -m venv venv
source venv/bin/activate    # macOS or Linux
venv\Scripts\activate       # Windows

pip install -r requirements.txt

echo "GEMINI_API_KEY=your-key-here" > .env

streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### Run with FastAPI Backend

To run the Streamlit frontend together with the FastAPI backend locally:

```
# In one terminal, start the FastAPI backend
python api.py

# In another terminal, enable local API mode and start Streamlit
echo "LOCAL_DEV=true" >> .env
streamlit run app.py
```

This will reveal the optional local API toggle in the sidebar.

---

## Why DAXGenie

Most BI analysts spend hours wrestling with DAX. Microsoft Copilot is available, but locked behind enterprise licenses.

DAXGenie was built to bridge that gap, bringing modern AI to the daily workflow of every Power BI analyst, for free.

It also serves as a demonstration of how Power BI expertise and AI engineering can combine to solve real day-to-day problems.

---

## About the Author

**Kotha Sreeja**

Microsoft Certified Power BI Data Analyst
MSc Business Analytics and Data Science

Software engineer with 3+ years of experience in Python backend, SQL, full-stack development, and modern data tooling. Currently focused on the intersection of Business Intelligence and AI engineering.

[LinkedIn](https://www.linkedin.com/in/kotha-sreeja) | [GitHub](https://github.com/sreeja1105)

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

Free to use, modify, and distribute. If you build something with DAXGenie, the author would love to hear about it.

---

## Support

If DAXGenie is useful to you:

- Star the repository on GitHub
- Share it with other Power BI analysts
- Connect with the author on [LinkedIn](https://www.linkedin.com/in/kotha-sreeja)
- Report bugs or suggest features via [Issues](https://github.com/sreeja1105/daxgenie/issues)

---

Built for the Power BI community by [Kotha Sreeja](https://www.linkedin.com/in/kotha-sreeja).