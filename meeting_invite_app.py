import streamlit as st

# --- Setup ---
st.set_page_config(page_title="Meeting Invite Generator", layout="centered")
st.title("📅 Meeting Invite Generator")

# --- Input: Slack Emails ---
st.header("Step 1: Paste Slack Emails")
slack_emails_raw = st.text_area("Paste emails from Slack channel (separated by spaces or commas)", height=100)
slack_emails = [email.strip() for email in slack_emails_raw.replace(",", " ").split() if "@" in email]

# --- Input: Additional Custom Invitees ---
st.header("Step 2: Add Custom Invitees (optional)")
custom_emails_raw = st.text_input("Enter additional emails (comma or space-separated)")
custom_emails = [email.strip() for email in custom_emails_raw.replace(",", " ").split() if "@" in email]

# Combine all emails
all_invitees = sorted(set(slack_emails + custom_emails))

# --- Input: Meeting/Appointment Subject ---
st.header("Step 3: Enter Subject (manual entry)")
subject = st.text_input("Subject", placeholder="e.g. Kickoff Call: Project X")

# --- Input: Meeting Type & Template ---
st.header("Step 4: Select Meeting Type")
meeting_type = st.selectbox("Choose meeting type", ["Scoping", "Kickoff", "Readout", "QA Review", "Post-Mortem", "Custom"])

# Meeting template dictionary
templates = {
    "Scoping": """Agenda:

1. Team Introductions
2. Overview of Architecture Diagram
3. Application Live Demo
4. In-Scope Items (APIs, Code Packages, Logs, Devices, etc.)
5. Q&A
6. Timeline & Next Steps""",
    
    "Kickoff": """Agenda:

1. Tester Introductions
2. Overview of SOW
3. Identify pending access requests & documentation
4. Timeline & logistics
5. Q&A""",
    
    "Readout": """Agenda:

1. Pentest Overview (In-Scope Items)
2. Summary of Pentest Observations
3. Summary of Pentest Findings & Recommendations
4. Next Steps & Remediation Process (SLAs)""",
    
    "QA Review": """This is the QA appointment hold for your engagement. 

Please reach out to your assigned QA Reviewer on or before the assigned QA date to ensure the final report is reviewed prior to the readout meeting. 

Thank you and please reach out to your EM if you have any questions or concerns.
    """,
    
    "Post-Mortem": """Agenda:
    
1. Pros & Cons (e.g., access issues, poor builder team communication, scoping, etc.)
2. EM Support
3. Skills Recap
4. Future Goals""",
    
    "Custom": ""  # Placeholder for custom agenda
}

# Text area to show/edit template
st.subheader("Step 5: Customize Agenda")
agenda_template = st.text_area("Meeting Agenda", templates[meeting_type], height=150)

# --- Output ---
st.header("📤 Invite Summary")

if st.button("Generate Invite Content"):
    if not all_invitees:
        st.warning("⚠️ No invitees found. Please paste Slack emails or add custom invitees.")
    else:
        st.success("✅ Invite content generated below!")
        
        st.subheader("To:")
        st.code("; ".join(all_invitees), language="text")  # Outlook format with semicolons

        st.subheader("Subject:")
        st.code(subject if subject else "No subject provided", language="text")

        st.subheader("Body:")
        st.code(agenda_template, language="markdown")

# --- Optional Tips ---
with st.expander("ℹ️ How to use this"):
    st.markdown("""
    1. Copy Slack emails from a channel (like from a CSV export or user list).
    2. Paste them into the Slack email field.
    3. Add any other emails if needed.
    4. Choose your meeting type (or write your own agenda).
    5. Click **Generate Invite** and copy into Outlook.
    """)
