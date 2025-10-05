# Prompt Playbook v1

## Objective
Capture empirical observations comparing prompt variants and model behaviors. Use this as a living artifact you will refine in future weeks.

## How to Use This File
1. After each script run, append rows to the Results Table.
2. Tag failure modes (see legend) so patterns emerge quickly.
3. Summarize insights after completing stretch assignments.

## Scoring Rubric (1–5)
| Score | Instruction Adherence | Reasoning Depth | Style / Persona | Format Fidelity |
|-------|-----------------------|-----------------|-----------------|-----------------|
| 1 | Misses key directives | Single sentence | Ignores persona | Broken / ignores |
| 3 | Mostly follows | Some steps implicit | Partial persona | Minor drift |
| 5 | Precise & complete | Clear multi-step chain | Fully consistent | Exact, parsable |

## Failure Mode Tags
hallucination, verbosity, shallow, drift (format), persona-loss, json-break, constraint-fail

## Results Table (Populate During Lab)
| Prompt Pattern | Example Used | Model | Adherence (1–5) | Reasoning (1–5) | Style (1–5) | Format (1–5) | Failure Modes | Notes | Reuse? (Y/N) |
|----------------|--------------|-------|------------------|-----------------|-------------|--------------|---------------|-------|--------------|
| Few-Shot | Elvish word creation | llama3 | 4 | 4 | 5 | 4 | verbosity | Added lore beyond prompt; creative but exceeded scope. | N |
| Few-Shot | Elvish word creation | mistral | 3 | — | 4 | 3 | verbosity, format | Gave multiple words instead of one; partially adhered. | N |
| Few-Shot | Elvish word creation | gpt-3.5 | 5 | — | 5 | 5 | — | Perfect single example, concise. | N |
| Few-Shot | Elvish word creation | gemini-pro | 5 | — | 5 | 5 | — | Simple and correct, balanced brevity. | N |
| Role | Personal trainer 5-day plan | llama3 | 5 | — | 5 | 5 | — | Comprehensive, persona-consistent and detailed. | N |
| Role | Personal trainer 5-day plan | mistral | 5 | — | 4 | 5 | — | Clear persona; reasonable plan, fewer details. | N |
| Role | Personal trainer 5-day plan | gpt-3.5 | 5 | — | 3 | 5 | — | Accurate, compact. | N |
| Role | Personal trainer 5-day plan | gemini-pro | 5 | 5 | 5 | 5 | verbosity | Long but highly contextual and motivational. | N |
| Chain-of-Thought | Order words by length | llama3 | 4 | 3 | 4 | 5 | shallow, hallucination | Miscounted “mouse” letters (3 vs. 5); reasoning slight flaw. | N |
| Chain-of-Thought | Order words by length | mistral | 5 | 5 | 5 | 5 | — | Correct reasoning, clear step-by-step. | N |
| Chain-of-Thought | Order words by length | gpt-3.5 | 5 | 4 | 4 | 5 | shallow | Correct but minimal reasoning. | N |
| Chain-of-Thought | Order words by length | gemini-pro | 5 | 5 | 5 | 5 | — | Clear, thorough step explanation. | N |
| Structured Output | Countries & capitals JSON | llama3 | 5 | — | 4 | 5 | — | Correct JSON; clean output. | N |
| Structured Output | Countries & capitals JSON | mistral | 5 | — | 5 | 5 | — | Valid JSON, consistent order. | N |
| Structured Output | Countries & capitals JSON | gpt-3.5 | 5 | — | 5 | 5 | — | Correct JSON, concise. | N |
| Structured Output | Countries & capitals JSON | gemini-pro | 5 | — | 5 | 5 | — | Correct JSON. | N |
| Negative Prompting | Mistakes when learning to code | llama3 | 5 | — | 4 | 5 | verbosity | Followed “no positive tips” rule; slightly long. | N |
| Negative Prompting | Mistakes when learning to code | mistral | 5 | — | 4 | 5 | verbosity | Clean list, no positivity creep. | N |
| Negative Prompting | Mistakes when learning to code | gpt-3.5 | 5 | — | 3 | 5 | — | Concise and compliant. Missing end dots. | N |
| Negative Prompting | Mistakes when learning to code | gemini-pro | 5 | — | 4 | 5 | — | Perfectly compliant, varied phrasing. | N |


## Model Summary (After Initial Pass)
| Capability | Best Model(s) | Evidence Snippet | Notes |
|-------------|----------------|------------------|-------|
| **Explanatory Clarity** | **Gemini Pro, GPT-3.5** | “Therefore, the final order… cat, mouse, elephant.” | Clear, natural reasoning without over-explaining. |
| **Chain-of-Thought** | **Gemini Pro, Mistral** | Both provided full step-by-step enumeration with correct logic. | Gemini slightly more didactic. |
| **JSON Adherence** | **GPT-3.5, Gemini Pro, Mistral** | All produced perfectly parsable JSON arrays. | No format drift or syntax errors. |
| **Persona Control** | **Gemini Pro, Llama3** | “As your personal trainer, I’ve designed…” | Maintained role and motivational tone. |
| **Instruction Strictness** | **GPT-3.5** | Consistently followed every rule precisely (no extra fluff). | Most literal adherence overall. |

## Insight Log
Record notable surprises, regressions, or improvements.
- Day 1: Llama3 often over-explains or embellishes creatively; good for flavor, weaker for constraint-following.
- Day 2:
- Day 3:

---

### 1. Role Prompting

*   **Best Practice:**
    *   Clearly define the persona or role you want the AI to adopt. This helps to set the context, tone, and level of detail in the response.
*   **Example:**
    *   Instead of "Explain black holes," use "You are an astrophysicist. Explain the concept of a black hole to a curious 10-year-old."

---

### 2. Few-Shot Learning

*   **Best Practice:**
    *   Provide a few examples of the desired input and output format. This is especially useful for tasks like classification, summarization, or code generation.
*   **Example:**
    *   When asking for a summary, provide one or two examples of a text and its corresponding summary before providing the text you want to be summarized.

---

### 3. Chain-of-Thought (CoT)

*   **Best Practice:**
    *   Encourage the model to "think step by step" or to "show its work." This is particularly effective for complex reasoning tasks, such as math problems or logic puzzles.
*   **Example:**
    *   Append "Let's think step by step" to your prompt when you need the model to reason through a problem.

---

### 4. Anti-Patterns to Avoid
## Reflection (End of Week)
Answer briefly:
1. Which two prompt patterns yielded the largest delta between models?
    Few-shot prompt.
2. Which failure mode was most frequent? Root cause?
    Verbosity. Some models tend to over-explain their outputs.
3. Default model choice for: explanation / reasoning / structure.
    Gemini Pro.
4. Open questions heading into Week 2.
*   **Ambiguity:**
    *   Avoid vague or open-ended questions. Be as specific as possible.
*   **Leading Questions:**
    *   Don't phrase your prompt in a way that suggests a desired answer.
*   **Overly Complex Prompts:**
    *   Break down complex tasks into smaller, more manageable prompts.

---
