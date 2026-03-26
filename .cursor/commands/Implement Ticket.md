---
name: Implement ticket (Backend Vet LangChain)
description: Structured workflow to implement a ticket with CAC using the Backend Vet LangChain Engineer agent.
agent: Backend Vet LangChain Engineer
---

You are executing a **structured implementation workflow** for a single ticket whose description and CAC (Customer/Clinic Acceptance Criteria) are provided in the conversation.

Follow this exact sequence every time this command is run:

1. **Read the ticket and CAC**
   - Carefully read the ticket description, linked context, and CAC.
   - Summarize in your own words:
     - The problem or feature.
     - The explicit CAC items.
     - Any implicit constraints (performance, safety, UX, veterinary/legal constraints).

2. **Create a plan**
   - Draft a short, ordered implementation plan as a checklist (3–10 items max).
   - Include:
     - Code changes (files/modules to touch).
     - Any LangChain architecture decisions (RAG vs tools vs router).
     - Tests you will add or update.
   - Confirm the plan with the user only if the scope is ambiguous or risky; otherwise proceed.

3. **Ask questions if needed**
   - If critical details are missing (requirements, API contracts, domain rules), ask **concise, numbered questions**.
   - Group questions to minimize back-and-forth.
   - Clearly state what you can already proceed with and what is blocked on answers.

4. **Move the ticket to “In Progress”**
   - As soon as you start implementing, explicitly state that the ticket should be moved from **“To Do” → “In Progress”** in the user’s tracking system (e.g., Jira, Linear, GitHub Projects).
   - If the user’s tool and ticket ID are known, reference them in your message (e.g., “Move `VET-123` to In Progress.”).

5. **Develop the code**
   - Implement changes step by step, following:
     - Project Python rules in `.cursor/rules/Python.mdc`.
     - Veterinary and LangChain guidance from the `vet-langchain-chatbots` skill.
   - Prefer:
     - Small, focused functions and modules.
     - Clear system prompts and tool definitions for LangChain.
     - Comprehensive tests with `pytest`.
   - Use the IDE tools (Read, ApplyPatch, Shell, ReadLints) to:
     - Edit code safely.
     - Run tests and linters where appropriate.
   - Provide brief progress updates as you complete major checklist items.

6. **Create a PR with a good description**
   - Create or ensure you are on a feature branch named after the ticket (e.g., `feat/VET-123-short-slug`).
   - Summarize changes in the PR description:
     - **Summary**: 1–3 bullet points describing the main changes.
     - **Details**: Architectural notes (e.g., LangChain agent type, new tools, prompts).
     - **Testing**: How you tested (commands, scenarios).
     - **CAC mapping**: Explicitly note how each CAC item is satisfied.

7. **Move the ticket to “In Review”**
   - After the PR is created and ready for review, explicitly instruct that the ticket should be moved from **“In Progress” → “In Review”**.
   - Include:
     - Ticket ID.
     - PR URL.
     - Any special review notes (e.g., areas with more risk, schema changes).

Throughout this workflow:
- Be concise, structured, and transparent about progress.
- Default to **actionable implementations** (not just suggestions).
- Respect veterinary safety, legal boundaries, and customer-service tone as defined in the attached skills and rules.

