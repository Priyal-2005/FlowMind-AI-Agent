"""
Sample Workflow Inputs for FlowMind AI Demo

Three realistic enterprise scenarios:
1. Sprint Planning (Simple) — clear tasks, owners, deadlines
2. Q4 Product Review (With Blockers) — dependencies, blockers, tight deadlines
3. Crisis Response (Missing Owners) — urgency, missing assignments, conflicting priorities
"""

SAMPLE_INPUTS = {
    "Sprint Planning — Simple Meeting": {
        "description": "A clean sprint planning meeting with clear action items, owners, and deadlines.",
        "icon": "📋",
        "transcript": """
Sprint Planning Meeting — Engineering Team
Date: Monday Morning
Participants: Raj, Sarah, Mike, Priya

Raj: Alright team, let's plan this sprint. We have the dashboard redesign, API optimization, and the new authentication module to handle.

Sarah: I'll take the dashboard redesign. I've already done the wireframes and I can have the frontend components ready by end of Day 2. I'll use the new design system we agreed on last week.

Raj: Perfect. Make sure to include the dark mode toggle — product really wants that. Mike, how about the API optimization?

Mike: I'll handle the API optimization. The response times are currently at 800ms, we need to bring them under 200ms. I should be able to finish the database query optimization by Day 1, and the caching layer by Day 2.

Raj: Great. What about the authentication module?

Priya: I'll work on the authentication module. I need to implement OAuth2 with Google and GitHub providers. I'll have the Google integration done by Day 1 and GitHub by Day 2. Full testing by Day 3.

Raj: Excellent. I'll handle the deployment pipeline updates and the CI/CD configuration. Should be done by Day 2.

Sarah: One thing — we decided to go with React Server Components for the dashboard instead of client-side rendering. That's a firm decision from the architecture review.

Raj: Confirmed. Also, we agreed to deprecate the v1 API endpoints by end of this sprint. Mike, make sure the migration guide is updated.

Mike: Will do. I'll update the API documentation as part of my task.

Raj: Alright, let's execute. Daily standups at 9 AM. Any blockers, flag them immediately.
""",
    },

    "Q4 Product Review — With Blockers": {
        "description": "A product review meeting with blockers, dependencies, and pressure.",
        "icon": "🚧",
        "transcript": """
Q4 Product Review — Cross-functional Meeting
Date: Wednesday Afternoon
Participants: Raj, Sarah, Mike, Priya, Anil

Raj: Team, we need to review Q4 deliverables. The board presentation is in 3 days. Let's go around.

Sarah: The customer portal redesign is 60% done. But I'm blocked on the payment integration — I need the Stripe API keys from the finance team. I've been waiting for two days and nobody has responded. Without those keys, I can't test the checkout flow.

Raj: That's critical. We need to escalate that today. Anil, can you follow up with finance?

Anil: I'll chase the finance team, but honestly I'm also dealing with the compliance audit. The security review needs to be completed by Day 1, and I have three other tasks on my plate already.

Mike: On the backend side, I need to finish the data migration script. It depends on Sarah's payment schema being finalized first. So I'm technically blocked too. Once I get the schema, I can have the migration ready by Day 2.

Priya: The mobile app push notifications are ready, but we can't deploy until Mike's data migration is complete. So there's a chain of dependencies here: Sarah's payment → Mike's migration → my deployment.

Raj: This dependency chain is concerning. What about the analytics dashboard?

Sarah: That's also on me. I should have it done by Day 3 but it's lower priority than the payment integration.

Raj: We decided to postpone the social media integration to next quarter. That's final. Also, we're going with Firebase for push notifications instead of our custom solution.

Anil: I also need to prepare the security compliance report. There's a blocker — the penetration testing results from the vendor haven't arrived yet. They were supposed to come last week.

Raj: So we have two critical blockers: Stripe API keys and penetration test results. Both are external dependencies. This is going to be tight.

Mike: Also, I just realized the database server needs to be upgraded before the migration. That's another task that nobody has been assigned to.

Raj: We need someone on that urgently. And the API documentation update — who's handling that?

Raj: Let's also not forget the performance benchmarks need to be run before the board presentation.
""",
    },

    "Crisis Response — Missing Owners": {
        "description": "An urgent crisis meeting with missing assignments, conflicting priorities, and high stakes.",
        "icon": "🚨",
        "transcript": """
Emergency Response Meeting — System Outage
Date: Thursday, 2:00 PM (Urgent)
Participants: Raj, Sarah, Mike, Priya

Raj: Everyone, we have a critical situation. The production system went down 30 minutes ago. Customer complaints are flooding in. We need to move fast.

Mike: I've identified the issue — the database connection pool is exhausted. We need to increase the pool size and restart the services immediately.

Raj: Mike, handle the immediate database fix right now. This is P0, must be done today.

Sarah: The frontend is showing 502 errors to users. Someone needs to put up a maintenance page while Mike fixes the backend.

Raj: Good call. Sarah, can you handle the maintenance page?

Sarah: I'm already on three other things but yes, I'll do it right now.

Priya: We also need to send a customer communication email about the outage. Our SLA requires notification within 1 hour.

Raj: Absolutely critical. Someone needs to draft that email immediately.

Mike: After the immediate fix, we need a root cause analysis document. The post-mortem should cover why the connection pool wasn't monitored.

Raj: Agreed. We also need to set up monitoring alerts so this doesn't happen again. We should implement automated scaling for the connection pool.

Sarah: The load balancer configuration also needs to be reviewed. I suspect it's not distributing traffic properly.

Raj: Good point. And we need to update the incident response runbook with lessons from today.

Priya: One more thing — the backup system hasn't been tested in months. We need to verify our disaster recovery plan is actually functional. This is urgent but nobody has time for it right now.

Raj: We decided that all production deployments will require a pre-deployment checklist going forward. Also, we're implementing mandatory service health checks before any release.

Mike: The database fix is my top priority. But the monitoring setup, the scaling implementation, and the runbook update — those need owners. Right now they're just floating.

Raj: You're right. We need to figure out assignments. The load balancer review, the disaster recovery test, and the monitoring alerts — these all need to happen by Day 2 at the latest.

Priya: I can take the customer communication. But the DR test, the monitoring setup, and the runbook update are still unassigned. That's three critical tasks with no owners.

Raj: Let's flag those and figure it out. We can't let anything fall through the cracks on this. Every minute of downtime costs us $5,000.
""",
    },
}

# Backward compatibility alias
TRANSCRIPTS = SAMPLE_INPUTS


def get_input_names() -> list:
    """Return list of available input names."""
    return list(SAMPLE_INPUTS.keys())


# Backward compatibility alias
get_transcript_names = get_input_names


def get_input(name: str) -> dict:
    """Get a specific input by name."""
    return SAMPLE_INPUTS.get(name, {})


# Backward compatibility alias
get_transcript = get_input
