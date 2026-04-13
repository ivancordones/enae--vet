# ENAE VET Chatbot MVP

Implementation for ENAE Session 6 criteria, aligned with the Jira SCRUM board flow (`SCRUM-6` onwards): a deployable, deterministic chatbot focused on reducing friction for sterilization/castration appointment coordination.

## What is implemented

- `POST /api/chat` with JSON input `{ "session_id": "...", "message": "..." }` and output `{ "response": "..." }`.
- `GET /api/health` for deployment/monitor checks.
- Session memory by `session_id` (species, sex, age, heat status, last intent).
- Explicit domain guardrails:
  - sterilization/castration logistics scope
  - emergency triage out of scope
  - human handoff path
  - mandatory analytics note for pets older than 6 years
- Mock availability tool (invoked only for booking/availability intent).
- Lightweight RAG retriever grounded in required source:
  - [Instructions before operation](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)

## Project structure

- `index.html`: simple chat frontend.
- `api/chat.py`: main orchestration endpoint.
- `api/health.py`: health check endpoint.
- `api/domain.py`: intent detection + domain rules + memory entity extraction.
- `api/availability.py`: mock availability tool with clinic constraints.
- `api/rag.py`: fetch/chunk/index/retrieve pipeline for pre-op instructions.
- `requirements.txt`: no external runtime dependencies.

## Local run

1. Install Python 3.11+.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start Vercel dev server:

```bash
npx vercel dev
```

4. Open:
   - UI: `http://localhost:3000`
   - Health: `http://localhost:3000/api/health`

## Deploy on Vercel

```bash
npx vercel
```

For production:

```bash
npx vercel --prod
```

### Environment variables

No secrets are required for this MVP.  
The chatbot works without paid LLM APIs.

## RAG design (required source)

Retriever implementation is in `api/rag.py`.

1. **Fetch**: downloads the required URL via `urllib`.
2. **Clean**: strips scripts/styles/HTML tags to plain text.
3. **Chunk**: fixed-size overlapping chunks (deterministic).
4. **Index**: in-memory lexical scoring via token overlap.
5. **Retrieve**: top-k chunks based on query relevance.
6. **Answering**: response explicitly cites the source URL.

If remote fetch fails, a safe fallback chunk is used so the bot still responds.

## Availability tool logic

Tool implementation: `api/availability.py`.

- Operational surgery days: Monday to Thursday.
- Capacity rule: max 240 minutes/day.
- Dog rule: max 2 dogs/day.
- Time estimate per species/sex:
  - dog male 30 min, dog female 50 min
  - cat male 12 min, cat female 15 min
- In-heat rejection: impossible booking is rejected with explanation.
- Species-specific dropoff windows:
  - cats: 08:00–09:00
  - dogs: 09:00–10:30

The tool is called only when booking/availability intent is detected.

## Conversation intents and test mapping (1–10)

1. Greeting + scope.
2. Sterilization info request.
3. Species memory follow-up.
4. Older pet (>6 years) analytics requirement.
5. Emergency triage and out-of-scope handling.
6. In-heat rule and rejection.
7. Human handoff request.
8. Availability check for surgery day.
9. Booking feasibility with species/day constraints.
10. Pre-operation instructions via RAG source.

## Professor test script (quick)

Use the same `session_id` for turns 1–10.

1. "Hi"
2. "I want sterilization information"
3. "It is a female dog"
4. "She is 8 years old"
5. "She is bleeding and it feels urgent"
6. "Can I book if she is in heat?"
7. "Please connect me with a human"
8. "Check availability for Tuesday"
9. "Check availability for Monday for a dog"
10. "What should I do before surgery regarding food and water?"

## Rubric checklist (ENAE Session 6)

- [x] Session memory with `session_id`.
- [x] Explicit domain/system behavior rules in backend.
- [x] Coherent support for conversations 1–7 without availability tool.
- [x] Vercel-friendly deployment and no secrets in repo.
- [x] Jira alignment in scope (`SCRUM-6` onward implementation focus).
- [x] Demonstrable RAG retriever using required URL.
- [x] Mock availability tool for conversations 8–9.
- [x] Intents documented and mapped to conversations 1–10.

