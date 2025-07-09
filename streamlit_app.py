import streamlit as st
import pandas as pd
import subprocess
import os
import io
import plotly.express as px

st.set_page_config(page_title="Lindy Sales Agents Dashboard", layout="wide")
st.title("🤖 Lindy Sales Automation Agents")

# --- Get user query ---
query = st.text_input("🔍 Enter your lead search query (e.g., 'AI tools for B2B companies')")

# --- Run all agents ---
if st.button("🚀 Run Full Pipeline") and query:
    st.info("Running agents...")

    # Start the subprocess with universal_newlines=False so we can wrap with utf-8
    process = subprocess.Popen(
        ["python", "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1
    )

    # Send the query input
    try:
        process.stdin.write((query + "\n").encode("utf-8"))
        process.stdin.flush()
        process.stdin.close()
    except Exception as e:
        st.error(f"Failed to send input: {e}")

    # Wrap stdout to ensure UTF-8 decoding
    # Wrap stdout to ensure UTF-8 decoding
    stdout = io.TextIOWrapper(process.stdout, encoding='utf-8', errors='replace')


    # Read and display the output
    output = ""
    for line in stdout:
        st.text(line.strip())
        output += line

    process.wait()
    st.success("✅ Pipeline completed")

# --- Show latest forecast ---
forecast_path = "data/leads_forecasted.csv"
if os.path.exists(forecast_path):
    df = pd.read_csv(forecast_path)
    st.subheader("📈 Lead Forecast")

    # Pie chart
    fig = px.pie(df, names='category', title='Lead Categories', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.subheader("📋 Detailed Forecast")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ Run the pipeline first to generate forecast data.")

# --- Optional debug info ---
with st.expander("🔍 Debug Info"):
    if os.path.exists("data/leads_enriched.csv"):
        st.write("Leads Enriched:")
        st.dataframe(pd.read_csv("data/leads_enriched.csv"))
    if os.path.exists("data/replies.csv"):
        st.write("Email Replies:")
        st.dataframe(pd.read_csv("data/replies.csv"))
