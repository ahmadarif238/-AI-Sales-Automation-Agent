import pandas as pd
import requests
import os
from dotenv import load_dotenv
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Load leads
leads_df = pd.read_csv("data/leads_enriched.csv")
try:
    replies_df = pd.read_csv("data/replies.csv", encoding='utf-8')
except FileNotFoundError:
    replies_df = pd.DataFrame(columns=["from", "subject", "body"])

# Create email → reply dictionary
replies_dict = {}
for _, row in replies_df.iterrows():
    sender = str(row.get("from", "")).split("<")[-1].strip(">").lower()
    body = row.get("body", "")
    if sender and "@" in sender:
        replies_dict[sender] = body

def categorize_lead(email, reply_text):
    if not reply_text or pd.isna(reply_text):
        return "cold", "No reply received yet."

    prompt = f"""
Lead: {email}
Sent: 2025-07-08
Reply Received: Yes
Reply: "{reply_text}"

Task:
Based on this information, categorize this lead as "hot", "warm", or "cold" and explain why.

Respond in JSON:
{{"category": "...", "reason": "..."}}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful sales assistant that classifies leads based on engagement."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        import json
        parsed = json.loads(content)
        return parsed["category"], parsed["reason"]
    except Exception as e:
        return "unknown", f"Error: {str(e)}"

# Process each lead
results = []
for _, row in leads_df.iterrows():
    email_raw = row.get("emails", "")
    if pd.isna(email_raw) or "@" not in email_raw:
        continue

    email = str(email_raw).split(",")[0].strip().lower()
    if "@" not in email:
        continue

    reply = replies_dict.get(email, "")
    category, reason = categorize_lead(email, reply)
    results.append({"email": email, "category": category, "reason": reason})

# Save results
forecast_df = pd.DataFrame(results)
forecast_df.to_csv("data/leads_forecasted.csv", index=False)
print("[✓] Forecast saved to data/leads_forecasted.csv")
