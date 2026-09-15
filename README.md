# Job Scraping Resume Parser

A Python application that extracts structured candidate data from PDF resumes. Upload a resume through the web UI or API to get contact details, organizations, locations, and skills.

**Live app:** [https://job-scraping-f4xh.onrender.com/](https://job-scraping-f4xh.onrender.com/)

## Features

- PDF text extraction with PyMuPDF
- Contact extraction (name, email, phone) via regex and heuristics
- Organization and location detection with rule-based extractors
- Skill matching with spaCy PhraseMatcher
- Web UI for drag-and-drop resume upload
- REST API for programmatic parsing

## Tech Stack

- **Python 3.12**
- **FastAPI** + **Uvicorn** — web server and API
- **spaCy** (`en_core_web_sm`) — NLP entity recognition
- **PyMuPDF** — PDF parsing
- **Render** — deployment

## Project Structure

```
├── web/
│   ├── server.py          # FastAPI app and API routes
│   └── static/            # Web UI (HTML, CSS, JS)
├── parser/
│   ├── resume_parser.py   # Main parsing orchestrator
│   ├── pdf_parser.py      # PDF text extraction
│   ├── text_cleaner.py    # Text normalization
│   └── parser.py          # Legacy section-based parser
├── extractors/
│   ├── contact_extractors.py
│   ├── name_extractor.py
│   ├── organization_extractor.py
│   └── location_extractor.py
├── nlp/
│   ├── spacy_parser.py    # spaCy NER
│   ├── skill_matcher.py   # Skill phrase matching
│   └── skills.py          # Skill dictionary
├── models/
│   └── candidate.py       # CandidateProfile dataclass
├── test/                  # Local test scripts
├── main.py                # CLI entry point
├── requirements.txt
└── render.yaml            # Render deployment config
```

## Local Setup

```bash
# Clone the repository
git clone git@github.com:AtharvaChitnis/job_scraping.git
cd job_scraping

# Checkout the web UI branch
git checkout api/v2

# Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate    # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the web app
uvicorn web.server:app --reload --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### CLI

```bash
python main.py
```

Parses `resume.pdf` in the project root and prints extracted fields to the terminal.

## API

### Health Check

```
GET /health
```

**Response:**
```json
{ "status": "ok" }
```

### Parse Resume

```
POST /api/v1/parse
Content-Type: multipart/form-data
```

**Form field:** `file` (PDF)

**Response:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+1 555-123-4567",
  "organizations": ["Acme Corp", "State University"],
  "locations": ["San Francisco"],
  "skills": ["Python", "SQL", "FastAPI"]
}
```

**Example with curl:**

```bash
curl -X POST https://job-scraping-f4xh.onrender.com/api/v1/parse \
  -F "file=@resume.pdf"
```

## Deployment (Render)

The app is deployed on [Render](https://render.com) from the `api/v2` branch.

| Setting | Value |
|---|---|
| **Build Command** | `pip install --upgrade pip && pip install -r requirements.txt` |
| **Start Command** | `uvicorn web.server:app --host 0.0.0.0 --port $PORT` |
| **Python Version** | `3.12.8` |

Alternatively, deploy using the included `render.yaml` blueprint.

## Branches

| Branch | Description |
|---|---|
| `main` | Initial parser commit |
| `api/v1` | Modular parsing pipeline (CLI) |
| `api/v2` | Web UI + API + deployment config |

## License

MIT
