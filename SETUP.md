# Environment Setup

Follow these steps to get a reproducible environment for the Agentic AI Program.

## 1. Prerequisites
- Python 3.11+ installed (`python --version`)
- Git
- (Optional) VS Code with recommended extensions (see below)

## 2. Clone Your Repo
```
git clone <your-fork-url>
cd <your-repo>
```

## 3. Create Virtual Environment
Choose ONE approach:

### Option A: venv
```
python -m venv .venv
source .venv/bin/activate
```

### Option B: uv (fast dependency management)
Install uv once:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Then:
```
uv venv
source .venv/bin/activate
```

## 4. Install Dependencies
Initially only Week 1 minimal requirements:
```
pip install -r solutions/week1_prompt_engineering/requirements.txt
```
Later you can consolidate into a top-level `requirements.txt` or adopt Poetry/uv.

## 5. Environment Variables
Duplicate `.env.example` → `.env` and fill in provider keys you actually use.
```
cp .env.example .env
```
Load automatically (Recommended on macOS/Linux):
```
export $(grep -v '^#' .env | xargs)
```
(Consider using direnv for automatic loading.)

## 6. Recommended VS Code Extensions
- ms-python.python
- ms-python.debugpy
- charliermarsh.ruff
- ms-toolsai.jupyter
- GitHub.copilot (optional)

## 7. Pre-commit Hooks (Optional Early) 
Later we can enable:
```
pip install pre-commit
pre-commit install
```

## 8. Running a Week Lab
Each week lives under `solutions/weekX_*`. Read its `README.md` (or `LAB.md`).

## 9. Testing (Once tests exist)
```
pytest -q
```

## 10. Troubleshooting
| Issue | Resolution |
|-------|------------|
| Module not found | Activate venv or `pip install -e .` if package layout added |
| API key error | Ensure exported correct variable name |
| Rate limit | Implement exponential backoff / caching |

## 11. Next Steps
- Fill out `PROMPT_PLAYBOOK.md` as you iterate.
- Record evaluation outputs under `eval/results/` (to be added).

Happy building! 🎯
