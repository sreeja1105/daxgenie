import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

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
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error calling Gemini: {str(e)}"


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
    ["✨ Generate a DAX formula", "🔍 Explain an existing DAX formula"],
    horizontal=True
)

st.write("")

# ===== GENERATE MODE =====
if mode == "✨ Generate a DAX formula":
    user_request = st.text_area(
        "Describe the calculation you need in plain English:",
        placeholder="Example: Calculate year-over-year sales growth percentage, with rolling 3-month average for smoothing",
        height=130
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_clicked = st.button("✨ Generate DAX", type="primary", use_container_width=True)
    
    if generate_clicked:
        if user_request.strip():
            with st.spinner("🧞 DAXGenie is thinking..."):
                prompt = GENERATE_DAX_PROMPT.format(user_request=user_request)
                response = call_gemini(prompt)
            st.markdown(response)
        else:
            st.warning("Please describe what you need first.")

# ===== EXPLAIN MODE =====
else:
    dax_formula = st.text_area(
        "Paste the DAX formula you want to understand:",
        placeholder="Example: CALCULATE(SUM(Sales[Amount]), DATEADD(Calendar[Date], -1, YEAR))",
        height=130
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        explain_clicked = st.button("🔍 Explain DAX", type="primary", use_container_width=True)
    
    if explain_clicked:
        if dax_formula.strip():
            with st.spinner("🧞 DAXGenie is analyzing your formula..."):
                prompt = EXPLAIN_DAX_PROMPT.format(dax_formula=dax_formula)
                response = call_gemini(prompt)
            st.markdown(response)
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