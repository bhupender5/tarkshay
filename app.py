import os
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.ingestion.parser import parse_transcript
from src.ingestion.intent_extractor import extract_intents
from src.ingestion.audio_transcriber import transcribe_audio

from src.agents.pm_agent import run_pm_agent
from src.agents.architect_agent import run_architect_agent
from src.agents.qa_agent import run_qa_agent

from src.execution.ticket_generator import generate_tickets
from src.execution.spec_generator import (
    generate_system_spec,
    generate_readme
)
from src.execution.webhook_client import send_to_webhook


# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# Streamlit Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="Autonomous Meeting-to-Action Engine",
    layout="wide"
)


# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("🤖 Autonomous Meeting-to-Action Engine")

st.markdown("""
Upload a meeting transcript or audio file and let AI agents:
- Extract action items
- Generate technical specs
- Create markdown tickets
- Run QA governance checks
- Deliver webhook payloads
""")


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("Pipeline Status")


# ---------------------------------------------------
# File Upload
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Meeting File",
    type=["txt", "mp3", "wav"]
)


# ---------------------------------------------------
# Run Pipeline
# ---------------------------------------------------

if uploaded_file:

    if st.button("Run Pipeline"):

        try:

            # ---------------------------------------------------
            # Save Uploaded File
            # ---------------------------------------------------

            file_extension = uploaded_file.name.split(".")[-1]

            temp_path = f"temp_{uploaded_file.name}"

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            st.success("File uploaded successfully")

            # ---------------------------------------------------
            # Audio Transcription
            # ---------------------------------------------------

            if file_extension in ["mp3", "wav"]:

                st.info("Transcribing audio using Whisper...")

                transcript_text = transcribe_audio(temp_path)

                transcript_path = "output/generated_transcript.txt"

                Path("output").mkdir(
                    exist_ok=True
                )

                with open(
                    transcript_path,
                    "w",
                    encoding="utf-8"
                ) as f:

                    f.write(transcript_text)

                file_path = transcript_path

                st.sidebar.success("Audio Transcription Complete")

            else:

                file_path = temp_path

            # ---------------------------------------------------
            # Parse Transcript
            # ---------------------------------------------------

            st.info("Parsing transcript...")

            utterances = parse_transcript(file_path)

            if not utterances:

                st.error(
                    "No valid transcript content found."
                )

                st.stop()

            st.sidebar.success("Transcript Parsed")

            with st.expander("Parsed Transcript"):

                for utt in utterances:

                    st.write(
                        f"[{utt.timestamp}] "
                        f"{utt.speaker}: "
                        f"{utt.text}"
                    )

            # ---------------------------------------------------
            # Intent Extraction
            # ---------------------------------------------------

            st.info("Extracting intents...")

            intents = extract_intents(utterances)

            st.sidebar.success(
                "Intent Extraction Complete"
            )

            with st.expander("Extracted Intents"):

                st.json(intents)

            # ---------------------------------------------------
            # PM Agent
            # ---------------------------------------------------

            st.info("Running PM Agent...")

            pm_output = run_pm_agent(intents)

            st.sidebar.success("PM Agent Complete")

            with st.expander("PM Agent Output"):

                st.json(pm_output)

            # ---------------------------------------------------
            # Architect Agent
            # ---------------------------------------------------

            st.info("Running Architect Agent...")

            architect_output = run_architect_agent(
                intents
            )

            st.sidebar.success(
                "Architect Agent Complete"
            )

            with st.expander(
                "Architect Output"
            ):

                st.markdown(architect_output)

            # ---------------------------------------------------
            # QA Agent
            # ---------------------------------------------------

            st.info("Running QA Agent...")

            qa_output = run_qa_agent(
                pm_output,
                architect_output
            )

            st.sidebar.success(
                "QA Agent Complete"
            )

            with st.expander("QA Output"):

                st.json(qa_output)

            # ---------------------------------------------------
            # HITL Approval
            # ---------------------------------------------------

            if (
                qa_output["status"]
                == "HUMAN_APPROVAL_REQUIRED"
            ):

                st.warning(
                    "⚠️ High-risk action detected"
                )

                col1, col2 = st.columns(2)

                with col1:

                    approve = st.button(
                        "Approve"
                    )

                with col2:

                    reject = st.button(
                        "Reject"
                    )

                if reject:

                    st.error(
                        "Execution rejected by user."
                    )

                    st.stop()

                if not approve:

                    st.info(
                        "Waiting for approval..."
                    )

                    st.stop()

            # ---------------------------------------------------
            # Generate Tickets
            # ---------------------------------------------------

            st.info("Generating tickets...")

            generate_tickets(pm_output)

            st.sidebar.success(
                "Ticket Generation Complete"
            )

            # ---------------------------------------------------
            # Generate Spec + README
            # ---------------------------------------------------

            st.info(
                "Generating specs and README..."
            )

            generate_system_spec(
                architect_output
            )

            generate_readme(
                project_name="Meeting-to-Action Engine",
                architect_output=architect_output
            )

            st.sidebar.success(
                "Spec Generation Complete"
            )

            # ---------------------------------------------------
            # Webhook Delivery
            # ---------------------------------------------------

            st.info("Sending webhook payload...")

            payload = {
                "pm_output": pm_output,
                "architect_output": architect_output,
                "qa_output": qa_output
            }

            webhook_url = os.getenv(
                "WEBHOOK_URL"
            )

            webhook_response = send_to_webhook(
                payload,
                webhook_url
            )

            st.sidebar.success(
                "Webhook Delivery Complete"
            )

            with st.expander(
                "Webhook Response"
            ):

                st.json(webhook_response)

            # ---------------------------------------------------
            # Final Success
            # ---------------------------------------------------

            st.success(
                "✅ Full pipeline executed successfully!"
            )

        except Exception as e:

            st.error(
                f"Pipeline failed: {str(e)}"
            )