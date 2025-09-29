# Participant Solutions for the 12-Week Agentic AI Program

This repository is a template for participants of the 12-Week Agentic AI Program. It provides a structured space for you to complete and submit your weekly lab assignments and deliverables.

> Quick Links: [Setup](./SETUP.md) • [Program Overview](./PROGRAM_OVERVIEW.md) • [Contributing](./CONTRIBUTING.md) • [Docs Index](./docs/INDEX.md)

## How to Use This Repository

1.  **Create Your Own Repository:** Click the "Use this template" button on the main page of this repository to create your own private copy. Name it something like `[your-name]-agentic-ai-solutions`.

2.  **Clone Your New Repository:** Clone your newly created repository to your local machine.

3.  **Add Your Work:** As you complete each week's lab, place your deliverables inside the corresponding `solutions/weekX_...` folder.

    *   For example, after completing the Week 1 lab, you will add your modified `multi_model_prompt_lab.py` and your updated `PROMPT_PLAYBOOK.md` to the `solutions/week1_prompt_engineering/` directory.

4.  **Commit and Push:** Regularly commit and push your changes to your repository. This will serve as your submission and a portfolio of your work throughout the program.

5.  **Explore Shared Utilities:** Reusable code lives in `src/` (prompt templating, basic agent shell, metrics, tool registry). Keep week-specific experiments inside each `solutions/weekX_...` folder—promote only stable helpers into `src/`.

6.  **Learn the Structure:** See `PROGRAM_OVERVIEW.md` for weekly themes and `docs/` for deeper guides (agents, safety, evaluation, cost, patterns).

## Folder Structure

```
.
├── README.md                     # You are here
├── SETUP.md                      # Environment & tooling setup
├── PROGRAM_OVERVIEW.md           # 12-week roadmap & rubric dimensions
├── CONTRIBUTING.md               # Conventions (commits, style, prompts)
├── .env.example                  # Template for environment variables
├── src/                          # Reusable library code
│   ├── prompt/templating.py      # Prompt assembly helpers
│   ├── llm/clients.py            # Lightweight model client factory
│   ├── agents/base.py            # Minimal agent shell & event log
│   ├── eval/metrics.py           # Core evaluation metrics
│   └── tools/registry.py         # Tool registration & spec export
├── solutions/                    # Your weekly lab outputs
│   ├── week1_prompt_engineering/
│   ├── week2_context_engineering/
│   ├── week3_mcp_intro/
│   ├── week4_agent_experience/
│   ├── week5_role_and_skill_definition/
│   ├── week6_reasoning_and_planning/
│   ├── week7_autonomy_and_control/
│   ├── week8_devops_for_agents/
│   ├── week9_observability_and_monitoring/
│   ├── week10_project_kickoff/
│   ├── week11_build_and_integrate/
│   └── week12_demo_day/
├── docs/                         # Extended guides & references
│   ├── INDEX.md                  # Documentation table
│   ├── agent_design.md
│   ├── evaluation_guide.md
│   ├── prompt_patterns.md
│   ├── safety_guide.md
│   ├── cost_tracking.md
│   ├── glossary.md / faq.md
│   └── advanced/                 # Optional deep dives (RAG, Toolformer...)
├── templates/                    # Reusable Markdown scaffolds
│   └── week_folder/README.template.md
├── tests/                        # Unit tests for reusable code
│   └── test_prompt_templating.py
├── Makefile                      # Convenience tasks (lint, test, format)
├── pre-commit-config.yaml        # Lint/format hooks (enable with pre-commit)
└── .github/workflows/ci.yml      # CI pipeline (lint + tests)
```

## Getting Started Quickly
1. Read `SETUP.md` and configure your virtual environment.
2. Copy `.env.example` → `.env` and supply needed API keys.
3. Open `solutions/week1_prompt_engineering/` and follow its lab instructions.
4. Track prompt iterations in `PROMPT_PLAYBOOK.md` (Week 1) and reflections each week.
5. Promote stable, reusable logic into `src/` to keep solutions clean.

## Documentation & Learning Path
Central index: `docs/INDEX.md`
- Prompt craft patterns: `docs/prompt_patterns.md`
- Agent architecture: `docs/agent_design.md`
- Evaluation methodology: `docs/evaluation_guide.md`
- Safety & governance: `docs/safety_guide.md`
- Cost awareness: `docs/cost_tracking.md`
- Advanced topics: `docs/advanced/`

## Contributing Conventions
Use Conventional Commit prefixes (e.g., `feat:`, `docs:`, `refactor:`). Keep experimental spikes isolated (`exp:`) and graduate them once stable.

## Next Steps / Suggested Workflow
1. Baseline implementation
2. Evaluate (golden set & metrics)
3. Iterate + document changes
4. Add instrumentation & guardrails
5. Optimize cost & latency
6. Prepare demo narrative

Good luck, and happy building! 🚀
