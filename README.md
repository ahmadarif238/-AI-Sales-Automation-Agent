# 🤖 Lindy Sales Automation Agent

An AI-powered, agent-of-agents system to automate B2B lead generation, enrichment, outreach, and sales forecasting — all in one pipeline.

Built in Python using DuckDuckGo Search, Gmail SMTP/IMAP, and LLaMA 3 via [Groq Cloud](https://console.groq.com/).

---

## ⚙️ Setup & Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/lindy_sales_agents.git
cd lindy_sales_agents

2. Create Your .env File

Duplicate the template:

cp .env.example .env
Then fill in your credentials:

EMAIL_ADDRESS → Your Gmail address

EMAIL_PASSWORD → Gmail App Password (not raw password)

GROQ_API_KEY → Get one at console.groq.com

🔐 Your .env file is ignored via .gitignore. Never commit real credentials.

3. Install Python Dependencies

pip install -r requirements.txt

4. Agent Architecture
This project is an "Agent of Agents" — each sub-agent handles a specialized task in the B2B sales flow:

Agent Script	Role
lead_generator.py	Searches the web for relevant companies (via DuckDuckGo)
enrichment_agent.py	Scrapes websites for contact emails
lead_scorer.py	Scores leads based on email quality and relevance
engagement_agent.py	Sends personalized emails using Gmail SMTP
email_reply_collector.py	Tracks email replies using Gmail IMAP
sales_forecasting_agent.py	Uses Groq's LLaMA 3 to categorize leads as hot, warm, or cold

Each of these agents is orchestrated into a single seamless workflow.


5. 🚀 How to Run
🔁 CLI Pipeline (Interactive)
python main.py
You’ll be prompted to enter a search query like:

AI tools for B2B companies

The pipeline will:

Search → Scrape → Score → Email → Track replies → Forecast sales


6. 📊 Web App (Streamlit Dashboard)
streamlit run streamlit_app.py
From the browser UI, you can:

Enter a search query

View pipeline logs live

See a pie chart of lead forecasts

Explore detailed lead & reply tables

🧠 Powered by Groq Cloud
The final forecasting step uses Groq's blazing fast inference engine to run Meta’s LLaMA 3–70B model and classify leads as:

🔥 Hot

🌡️ Warm

❄️ Cold

Groq enables zero-shot reasoning at unmatched speed and cost.

💡 Notes & Future Ideas
You can easily plug in LangChain or Autogen for even more dynamic agents.

Add tracking pixel API for open rate detection.

Extend with Notion/CRM integration or Slack alerts.

🧑‍💻 Built By
Arif Ahmad Khan
Machine Learning Engineer & AI Automation Builder
🔗 LinkedIn | 🌐 Portfolio


