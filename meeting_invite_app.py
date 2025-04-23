import streamlit as st
from datetime import datetime

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

# Templates
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
    "Custom": ""
}

# Editable agenda
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
        st.code("; ".join(all_invitees), language="text")

        st.subheader("Subject:")
        st.code(subject if subject else "No subject provided", language="text")

        st.subheader("Body:")
        st.code(agenda_template, language="markdown")

                       # Generate ICS content
        uid = datetime.now().strftime('%Y%m%dT%H%M%S')
        dtstamp = datetime.now().strftime('%Y%m%dT%H%M%S')
        attendees_block = "\n".join([f"ATTENDEE;CN={email}:mailto:{email}" for email in all_invitees])

        # Escape and format agenda properly
        agenda_lines = agenda_template.strip().split("\n")
        agenda_escaped = "\\n".join([line.strip() for line in agenda_lines])

        ics_content = (
            "BEGIN:VCALENDAR\n"
            "VERSION:2.0\n"
            "PRODID:-//Meeting Invite Generator//EN\n"
            "BEGIN:VEVENT\n"
            f"UID:{uid}@invitegen.com\n"
            f"DTSTAMP:{dtstamp}\n"
            f"SUMMARY:{subject}\n"
            f"DESCRIPTION:{agenda_escaped}\n"
            "LOCATION:\n"
            f"{attendees_block}\n"
            "END:VEVENT\n"
            "END:VCALENDAR"
        )

        st.download_button("📥 Download ICS File", data=ics_content, file_name="meeting_invite.ics", mime="text/calendar")


# --- Help Section ---
with st.expander("ℹ️ How to use this"):
    st.markdown("""
    1. Paste emails from Slack or manually enter them.
    2. Choose a meeting template or enter your own agenda.
    3. Click **Generate Invite**.
    4. Download the .ics file and open it in Outlook — then pick your date/time and send!
    """)
