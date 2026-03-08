# Voizegen Backend 

Hey team! This is the backend for Voizegen — our AI-powered social speech rehearsal app for children on the autism spectrum. This README will walk you through everything you need to know to get up and running, even if this is your first time working on a backend project.

---

## What Does the Backend Actually Do?

Think of the backend as the **brain behind the scenes**. The frontend (React app) is what the child and parent see and interact with. The backend is what the frontend talks to in order to get data and process speech.

Right now the backend does three things:

1. **Gives the frontend the curriculum** — the sections, units and lessons that show up on the learning map
2. **Gives the frontend the exercises** — the actual phoneme cards a child practices in a lesson
3. **Checks if a child's speech matches** — receives audio from the mic, processes it, and returns whether they got it right

---

## Project Structure (What Each File Does)

```
voizegen-backend/
├── app/
│   ├── main.py              ← The front door. App starts here. All routes registered here.
│   ├── database.py          ← Sets up the connection to our shared database
│   ├── models/
│   │   ├── user.py          ← Defines the "users" and "children" tables
│   │   ├── curriculum.py    ← Defines the "sections", "units", "lessons" tables
│   │   └── exercise.py      ← Defines the "phoneme_exercises" table
│   ├── routes/
│   │   ├── curriculum.py    ← Handles GET /curriculum requests
│   │   ├── exercises.py     ← Handles GET /lessons/{id}/exercises requests
│   │   └── speech.py        ← Handles POST /speech/check requests
│   ├── schemas/             ← Coming in Sprint 3 (Pydantic validation)
│   └── services/            ← Coming in Sprint 3 (Whisper AI logic)
├── seed.py                  ← One-time script that fills the DB with sample data
├── .env                     ← YOUR secret keys (never shared, never committed to GitHub)
├── .env.example             ← Template showing what goes in .env (safe to commit)
├── .gitignore               ← Tells Git to ignore venv/, .env, and cache files
└── requirements.txt         ← List of all Python packages this project needs
```

---

## 🗄️ Database Structure

We're using **PostgreSQL** hosted on **Supabase** (free). Everyone on the team connects to the **same shared database** — do not create your own Supabase project.

The curriculum is structured like a tree:

```
Section
  └── Unit
        └── Lesson
              └── PhonemeExercise
```

**Example of real data in our DB right now:**
```
📚 Section:  "Phoneme Practice"
    └── 📖 Unit: "Basic Sounds"
          └── 📝 Lesson: "Starter Phonemes"
                ├── 🔊 Exercise: "sh" → Say the sound: SH (like in 'shoe')
                ├── 🔊 Exercise: "ch" → Say the sound: CH (like in 'chair')
                ├── 🔊 Exercise: "th" → Say the sound: TH (like in 'think')
                ├── 🔊 Exercise: "ee" → Say the sound: EE (like in 'feet')
                └── 🔊 Exercise: "oo" → Say the sound: OO (like in 'moon')
```

---

## Getting Set Up (Step by Step)

Follow these steps in order. Don't skip any.

### Step 1 — Clone the repo

```bash
git clone https://github.com/daviskennedy10/voizegen-backend
cd voizegen-backend
```

### Step 2 — Create a virtual environment

A virtual environment is an isolated box of Python packages just for this project. It prevents conflicts with other Python projects on your machine.

```bash
python3 -m venv venv
```

### Step 3 — Activate the virtual environment

```bash
source venv/bin/activate
```

You will know it worked when you see `(venv)` at the start of your terminal prompt.

> **Important:** You need to run this command every single time you open a new terminal tab to work on this project. If you ever see a `ModuleNotFoundError`, this is almost always why.

### Step 4 — Install all dependencies

```bash
pip install -r requirements.txt
```

This reads `requirements.txt` and installs every package the project needs automatically.

### Step 5 — Set up your `.env` file

This file holds your secret credentials. It is **never committed to GitHub** for security reasons.

```bash
cp .env.example .env
```

Now open `.env` in VS Code and fill in the values:

```
DATABASE_URL=        ← Ill send the one i have to you (do NOT create your own Supabase project)
OPENAI_API_KEY=      ← ill also send this too
SECRET_KEY=          ← Any long random string, e.g. "voizegen_secret_2026"
```

> 📩 **if i forget, please ask me** for the `DATABASE_URL` and `OPENAI_API_KEY`. Everyone shares the same database so we're all looking at the same data.

### Step 6 — Run the server

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

### Step 7 — Verify everything works

Open your browser and visit:

- `http://localhost:8000/health` → should show `{"status": "ok"}`
- `http://localhost:8000/docs` → should show the full interactive API docs

If both of those work, you are fully set up.

---

## 🔌 API Endpoints

You can test all of these directly at `http://localhost:8000/docs` — no extra tools needed. Just click an endpoint, hit **Try it out**, fill in the fields, and click **Execute**.

---

### `GET /health`
Just confirms the server is alive.

```json
{ "status": "ok", "message": "Voizegen backend is running" }
```

---

### `GET /curriculum`
Returns the full learning map — sections, units and lessons all nested together.

```json
[
  {
    "id": "3a769e90-...",
    "title": "Phoneme Practice",
    "units": [
      {
        "id": "415d4166-...",
        "title": "Basic Sounds",
        "lessons": [
          {
            "id": "319dd697-...",
            "title": "Starter Phonemes",
            "type": "phoneme"
          }
        ]
      }
    ]
  }
]
```

---

### `GET /lessons/{lesson_id}/exercises`
Returns all exercises for a specific lesson. Copy a lesson `id` from the curriculum response and paste it in.

```
GET /lessons/319dd697-3dda-49f1-a4fa-76e0c631cfd1/exercises
```

```json
[
  { "id": "...", "phoneme": "sh", "instruction_text": "Say the sound: SH (like in 'shoe')", "matched": null },
  { "id": "...", "phoneme": "ch", "instruction_text": "Say the sound: CH (like in 'chair')", "matched": null }
]
```

---

### `POST /speech/check`
The most important endpoint. Receives an audio file, checks it against the target phoneme, and returns whether the child matched it.

| Field | Type | Required | What it is |
|---|---|---|---|
| `exercise_id` | string | yes | The UUID of the exercise being attempted |
| `audio` | file | yes | The audio recording (.wav or .webm) |
| `mock` | boolean | no | Set to `true` to skip Whisper and simulate a match (Sprint 2 default) |

**Response:**
```json
{
  "exercise_id": "cdce55f1-...",
  "heard": "sh",
  "target": "sh",
  "matched": true,
  "mode": "mock"
}
```

>  **Sprint 2 note:** We're using `mock: true` for the demo which simulates a correct match without calling the Whisper API. Live Whisper integration is Sprint 3.

---

##  Frontend Integration

If you're on the frontend team and want to connect to the backend during local development, both devices need to be on the **same WiFi network**.

Point your fetch calls at:
```
http://localhost:8000
```

**Hardcode this lesson ID for now** to load the phoneme exercises:
```
319dd697-3dda-49f1-a4fa-76e0c631cfd1
```

**Example fetch call:**
```javascript
// Get all exercises for the starter lesson
const res = await fetch('http://localhost:8000/lessons/319dd697-3dda-49f1-a4fa-76e0c631cfd1/exercises')
const exercises = await res.json()
```

---

## 🌿 Git Branching Rules (Please Follow These)

To avoid overwriting each other's work, follow this simple rule: **nobody pushes directly to `main`.**

```bash
# 1. Always start by pulling the latest main
git checkout main
git pull

# 2. Create your own branch for your feature
git checkout -b feature/your-feature-name
# e.g. git checkout -b feature/auth-endpoint

# 3. Do your work, then commit
git add .
git commit -m "short description of what you did"

# 4. Push your branch
git push origin feature/your-feature-name

# 5. Go to GitHub and open a Pull Request to merge into main
```

---

## What's Done vs 🔜 What's Coming

### Done (Sprint 1 and 2 — Demo Ready)
- FastAPI server running and connected to shared Supabase database
- All 5 database tables created (users, sections, units, lessons, phoneme_exercises)
- Database seeded with sample curriculum and 5 phoneme exercises
- `GET /curriculum` endpoint working
- `GET /lessons/{id}/exercises` endpoint working
- `POST /speech/check` endpoint working (mock mode for Sprint 2)
- GitHub repo set up with team collaborators

### Coming in Sprint 3
- Live OpenAI Whisper integration (replace mock mode with real speech processing)
- Google OAuth login → validate token → issue JWT session
- Protect endpoints so only logged-in parents can access data
- Connect child session results to parent dashboard
- Retry and friction detection logic
- Deploy to Railway for a public URL (no more localhost)

---

## Common Mistakes to Avoid

| Mistake | What happens | Fix |
|---|---|---|
| Forgetting `source venv/bin/activate` | ModuleNotFoundError on everything | Run `source venv/bin/activate` first |
| Running `seed.py` more than once | Duplicate data in the database | Only run it once. Clear Supabase data first if needed |
| Committing `.env` | Your database password ends up on GitHub | It is in `.gitignore` — just never force-add it |
| Creating your own Supabase project | You won't see the shared team data | DM Chidubem for the shared `DATABASE_URL` |
| Pushing directly to `main` | Risk of breaking things for everyone | Always use a feature branch and pull request |

---

## Team



---

## Questions?

i will send on the keys directly for the `DATABASE_URL`, `OPENAI_API_KEY`, or any setup issues.

---

*Voizegen — CSCI 577a Software Engineering, Spring 2026, USC*
