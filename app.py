import streamlit as st
import os
import requests
from dotenv import load_dotenv
import google.genai as genai
import time

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# Optional: URL for the local API backend (FastAPI). If set, Streamlit can POST to it.
API_BACKEND_URL = os.getenv("API_BACKEND_URL", "http://localhost:8000")


# Configure Google GenAI client
client = genai.Client(api_key=api_key)
MODEL_NAME = 'gemini-2.5-flash'

# ===== PROMPT TEMPLATES =====
GENERATE_DAX_PROMPT = """You are DAXGenie, an expert Power BI DAX assistant with deep knowledge of DAX patterns, time intelligence, calculations, and best practices.

A Power BI analyst needs help with the following calculation:

"{user_request}"

Provide your response in EXACTLY this format (use markdown):

### DAX Formula
```dax
[Working DAX formula here]
```

### How It Works
[Plain English explanation in 2-4 sentences. Avoid jargon. Focus on what each part of the formula does.]

### Things to Watch Out For
- [Common pitfall 1]
- [Common pitfall 2]
- [Optional: performance or accuracy tip]

### Example Usage
[Briefly describe how a Power BI user would use this measure in a report — what visual would it appear in, what would it show]

Important rules:
- Use modern DAX syntax (DAX 2.0+)
- Include comments inside complex formulas using -- 
- If the request is ambiguous, make reasonable assumptions and state them clearly
- Use Calendar table conventions (Calendar[Date], DimDate) for time intelligence
- Output ONLY the sections above. Do not add extra commentary."""

EXPLAIN_DAX_PROMPT = """You are DAXGenie, an expert Power BI DAX assistant who excels at making complex formulas understandable.

A Power BI analyst wants to understand the following DAX formula:

```dax
{dax_formula}
```

Provide your response in EXACTLY this format (use markdown):

### What This Formula Does
[1-2 sentence high-level summary in plain English. What business question does this answer?]

### Step-by-Step Breakdown
[Walk through the formula piece by piece. For each function or operation:
- Name the function
- Explain what it does in plain English
- Note any important behavior]

### Result
[What does this formula return? A number, a percentage, a date? What context does it depend on?]

### Common Use Cases
[2-3 bullet points of real-world scenarios where this formula would be used]

Important rules:
- Be specific, not vague
- Assume the reader knows Power BI basics but not advanced DAX
- If you notice anything unusual or potential issues with the formula, flag it
- Output ONLY the sections above."""


# ===== HELPER FUNCTION =====
def call_gemini(prompt: str) -> str:
    """Send prompt to Gemini and return the response."""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return response.text or ""
    except Exception as e:
        return f"❌ Error calling Gemini: {str(e)}"


def call_api(endpoint: str, text: str) -> str:
    """Call the local FastAPI backend and return the `result` string or raise."""
    url = f"{API_BACKEND_URL.rstrip('/')}/{endpoint.lstrip('/') }"
    try:
        r = requests.post(url, json={"text": text}, timeout=30)
    except Exception as e:
        return f"❌ Error calling local API at {url}: {e}"
    if r.status_code != 200:
        return f"❌ API returned {r.status_code}: {r.text}"
    data = r.json()
    return data.get("result", "")


def check_backend_health() -> tuple[bool, str]:
    """Call the local FastAPI health endpoint and return status and message."""
    url = f"{API_BACKEND_URL.rstrip('/')}/healthz"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return False, f"HTTP {r.status_code}"
        data = r.json()
        if data.get("status") == "ok":
            return True, "Online"
        return False, f"Unexpected response: {data}"
    except Exception as e:
        return False, str(e)


# ===== STREAMLIT UI =====
st.set_page_config(
    page_title="DAXGenie | AI-powered DAX Assistant",
    page_icon="🧞",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    .stRadio > label {font-weight: 500;}
</style>
""", unsafe_allow_html=True)

# ===== MAIN HEADER =====
st.markdown("""
<div style="text-align: center; padding: 0.5rem 0 0 0;">
    <h1 style="margin-bottom: 0.3rem; color: #1d4ed8;">🧞 DAXGenie</h1>
    <p style="color: #4a4a4a; font-size: 1.15rem; margin: 0;">
        AI-powered DAX formula assistant for Power BI analysts
    </p>
    <p style="color: #888; font-size: 0.9rem; margin-top: 0.3rem;">
        Generate complex DAX from plain English &middot; Explain existing formulas &middot; Free & open source
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ===== MODE SELECTOR =====
mode = st.radio(
    "**What would you like to do?**",
    [" Generate a DAX formula", " Explain an existing DAX formula"],
    horizontal=True
)

# Sidebar option: prefer local API if available
use_api = st.sidebar.checkbox("Use local API backend (FastAPI)", value=False)
st.sidebar.markdown(f"**API URL:** {API_BACKEND_URL}")

if use_api:
    healthy, health_message = check_backend_health()
    if healthy:
        st.sidebar.success(f"Backend health: {health_message}")
    else:
        st.sidebar.error(f"Backend health: {health_message}")

st.write("")

# ===== GENERATE MODE =====
if mode == " Generate a DAX formula":
    # Example prompts to help demo the app quickly
    EXAMPLE_PROMPTS = {
        "": "",
        "Year-over-Year Growth (Sales)": "Calculate year-over-year sales growth percentage for the current selection.",
        "Running Total (Sales)": "Calculate a running total of Sales[Amount] up to the current date",
        "Sales Last 30 Days": "Calculate total sales for the last 30 days ending at the selected date",
        "3-month Rolling Average Sales": "Calculate a 3-month rolling average of Sales[Amount]",
        "Top 5 Products by Sales": "Return the top 5 products by sales amount"
    }

    choice = st.selectbox("Pick a demo prompt (or write your own):", list(EXAMPLE_PROMPTS.keys()))
    if "user_request" not in st.session_state:
        st.session_state["user_request"] = ""
    col_ex, col_btn = st.columns([4,1])
    with col_btn:
        if st.button("Use example prompt") and choice:
            st.session_state["user_request"] = EXAMPLE_PROMPTS[choice]

    user_request = st.text_area(
        "Describe the calculation you need in plain English:",
        value=st.session_state.get("user_request", ""),
        placeholder="Example: Calculate year-over-year sales growth percentage, with rolling 3-month average for smoothing",
        height=130,
        key="user_request_area"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_clicked = st.button(" Generate DAX", type="primary", use_container_width=True)

    if generate_clicked:
        if user_request.strip():
            with st.spinner("🧞 DAXGenie is thinking..."):
                prompt = GENERATE_DAX_PROMPT.format(user_request=user_request)
                start = time.time()
                if use_api:
                    response = call_api("generate", prompt)
                else:
                    response = call_gemini(prompt)
                latency_ms = int((time.time() - start) * 1000)
            st.markdown(response)
            st.caption(f"Response time: {latency_ms} ms")
        else:
            st.warning("Please describe what you need first.")

# ===== EXPLAIN MODE =====
else:
    EXAMPLE_DAX = {
        "": "",
        "Simple SUM example": "SUM(Sales[Amount])",
        "Year-to-date (YTD) Sales": "CALCULATE(SUM(Sales[Amount]), DATESYTD(Calendar[Date]))",
        "Previous Year Sales": "CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date]))"
    }

    choice = st.selectbox("Pick an example DAX formula:", list(EXAMPLE_DAX.keys()))
    if "dax_formula" not in st.session_state:
        st.session_state["dax_formula"] = ""
    col_ex, col_btn = st.columns([4,1])
    with col_btn:
        if st.button("Use example formula") and choice:
            st.session_state["dax_formula"] = EXAMPLE_DAX[choice]

    dax_formula = st.text_area(
        "Paste the DAX formula you want to understand:",
        value=st.session_state.get("dax_formula", ""),
        placeholder="Example: CALCULATE(SUM(Sales[Amount]), DATEADD(Calendar[Date], -1, YEAR))",
        height=130,
        key="dax_formula_area"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        explain_clicked = st.button(" Explain DAX", type="primary", use_container_width=True)

    if explain_clicked:
        if dax_formula.strip():
            with st.spinner("🧞 DAXGenie is analyzing your formula..."):
                prompt = EXPLAIN_DAX_PROMPT.format(dax_formula=dax_formula)
                start = time.time()
                if use_api:
                    response = call_api("explain", prompt)
                else:
                    response = call_gemini(prompt)
                latency_ms = int((time.time() - start) * 1000)
            st.markdown(response)
            st.caption(f"Response time: {latency_ms} ms")
        else:
            st.warning("Please paste a DAX formula first.")

# ===== PROFESSIONAL FOOTER =====
st.write("")
st.write("")
st.divider()
st.markdown("""
<div style="text-align: center; padding: 1rem 0; color: #666; font-size: 0.9rem;">
    Built by <strong style="color: #1d4ed8;">Kotha Sreeja</strong> &middot; 
    <a href="https://www.linkedin.com/in/kotha-sreeja" target="_blank" style="color: #1d4ed8; text-decoration: none;">LinkedIn</a> &middot; 
    <a href="https://github.com/sreeja1105/daxgenie" target="_blank" style="color: #1d4ed8; text-decoration: none;">GitHub</a>
</div>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### About DAXGenie")
    st.markdown("""
    A free, open-source AI tool that helps Power BI analysts work faster with DAX:
    
    • Generate complex DAX from plain English  
    • Decode and explain existing formulas  
    • Built to bridge BI and modern AI
    """)
    
    st.divider()
    
    st.markdown("### About the Author")
    st.markdown("""
    **Kotha Sreeja**  
    *MSc Business Analytics & Data Science*  
    *Microsoft Certified Power BI Data Analyst*
    
    Software engineer with 3+ years of experience in Python backend, SQL, and modern data tooling. Currently focused on the intersection of BI and AI.
    
    🔗 [LinkedIn](https://www.linkedin.com/in/kotha-sreeja)  
    🔗 [GitHub](https://github.com/sreeja1105)
    """)
    
    st.divider()
    
    st.markdown("### Tech Stack")
    st.markdown("""
    • **Backend:** Python  
    • **AI:** Google Gemini API  
    • **Frontend:** Streamlit  
    • **License:** MIT (open source)
    """)
    
    st.divider()
    
    st.markdown("""
    <div style="font-size: 0.75rem; color: #999; text-align: center;">
        Open source &middot; Free to use  
        Designed for the Power BI community
    </div>
    """, unsafe_allow_html=True)