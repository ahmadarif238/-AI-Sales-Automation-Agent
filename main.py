import subprocess
import os
import sys

# Ensure console output supports Unicode
sys.stdout.reconfigure(encoding='utf-8')

AGENTS_DIR = "agents"

AGENT_SCRIPTS = [
    "lead_generator.py",
    "enrichment_agent.py",
    "lead_scorer.py",
    "engagement_agent.py",
    "email_reply_collector.py",
    "sales_forecasting_agent.py"
]

def run_pipeline():
    print("\n🔁 Starting Sales Automation Pipeline...\n")

    # Ask user for query input (no emoji to avoid Windows encoding error)
    query = input("Enter your lead search query (e.g., 'AI tools for B2B companies'): ")

    for script in AGENT_SCRIPTS:
        script_path = os.path.join(AGENTS_DIR, script)

        print(f"🚀 Running {script}...")

        # If it's the lead_generator script, pass the query as argument
        if script == "lead_generator.py":
            result = subprocess.run(["python", script_path, query])
        else:
            result = subprocess.run(["python", script_path])

        if result.returncode == 0:
            print(f"✅ {script} completed successfully.\n")
        else:
            print(f"❌ Error in {script}: Exited with code {result.returncode}")
            break

    print("🎉 Pipeline execution finished.\n")

if __name__ == "__main__":
    run_pipeline()
