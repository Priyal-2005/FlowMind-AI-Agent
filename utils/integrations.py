"""
Mock Integrations — Slack & Email Simulation

Simulates external service integrations (Slack, Email) for
the autonomous decision engine. Actions are logged to the
audit trail and shown as Streamlit toasts in the UI.
"""

import streamlit as st

class MockIntegrations:
    """Mock layer for simulating real-world actions like Slack/Email."""
    
    def __init__(self, logger=None):
        self.logger = logger

    def send_slack_message(self, owner: str, message: str) -> None:
        """Simulate transmitting a Slack notification to the owner."""
        log_msg = f"📱 [Slack] Message sent to {owner}: {message}"
        print(log_msg)
        
        if self.logger:
            self.logger.log(
                "Integrations",
                f"Slack Notification → @{owner}",
                message,
                severity="ACTION"
            )
            
        try:
            st.toast(log_msg, icon="💬")
        except Exception:
            pass

    def send_email(self, owner: str, subject: str, body: str) -> None:
        """Simulate sending an email escalation."""
        log_msg = f"📧 [Email] Sent to {owner} | Subject: {subject}"
        print(log_msg)
        
        if self.logger:
            self.logger.log(
                "Integrations",
                f"Email escalation sent to {owner}: {subject}",
                f"{body[:150]}...",
                severity="ESCALATION"
            )
            
        try:
            st.toast(log_msg, icon="✉️")
        except Exception:
            pass
