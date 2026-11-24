import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="AI Equity Research Analyzer", page_icon="📊")
st.title("📊 AI Annual Report & Concall Analyzer")
st.write("Kisi bhi Indian company ki Annual Report ya Earnings Call PDF upload karein.")

api_key = st.secrets.get("GEMINI_API_KEY") or st.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.file_uploader("Upload PDF (Annual Report / Concall Transcript)", type=["pdf"])

if uploaded_file and api_key:
    if st.button("Analyze Document"):
        with st.spinner("AI document read kar raha hai... (30-60 seconds lag sakte hain)"):
            client = genai.Client(api_key=api_key)
            pdf_bytes = uploaded_file.getvalue()
            
            prompt = """
            You are a Senior Equity Research Analyst at an Indian PMS/Mutual Fund.
            Analyze the attached financial document (Annual Report or Earnings Call Transcript) and provide a crisp, institutional-grade summary with these exact sections:
            1. **Executive Summary & Business Overview** (3-4 bullet points)
            2. **Key Financial Highlights & Ratios** (Revenue, EBITDA, PAT, Margins, Debt/Equity in a clean Markdown table)
            3. **Management Guidance & Growth Outlook** (Future revenue/margin targets, demand trends)
            4. **Capex Plans & Capacity Expansion** (Specific numbers, timelines, funding)
            5. **Key Red Flags & Risks** (Governance, margin pressure, debt, working capital, regulatory risks)
            Keep it concrete, cite exact numbers from the document, and avoid fluff.
            """
            
            models_to_try = ["gemini-4-hydrogen", "gemini-3.8-flash", "gemini-4-neon"]
            success = False
            
            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[
                            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                            prompt
                        ]
                    )
                    st.success(f"Analysis Complete! (Powered by {model_name})")
                    st.markdown(response.text)
                    success = True
                    break
                except Exception as e:
                    continue
            
            if not success:
                st.warning("Abhi Google ke free servers par traffic bahut zyada hai. Please 2 minute baad dobara try karein ya ek chhota Concall PDF upload karein.")
