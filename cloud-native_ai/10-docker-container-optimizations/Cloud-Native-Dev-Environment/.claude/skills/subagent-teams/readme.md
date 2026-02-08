![Banner](./header.jpg)

# SubAgent-Teams 🚀

A specialized framework and skill set for **Claude Code** that implements high-efficiency parallel processing and context management through the **Subagent Delegation Strategy**.



## 📖 Overview

As AI-driven development sessions grow, the context window often fills up with raw file content and search results, triggering **auto-compaction**. This leads to a loss of nuance and reasoning quality. 

**SubAgent-Teams** solves this by moving heavy lifting (research, testing, pattern finding) into isolated sub-sessions. The main orchestrator remains "Lean," receiving only synthesized summaries, ensuring consistent high-performance reasoning throughout the entire lifecycle of your project.

## 🏗️ The Four Pillars of Delegation

1.  **Specialization:** Every subagent is assigned a specific, narrow domain.
2.  **Domain-Specific Prompts:** Targeted instructions to ensure the subagent doesn't "drift" from its task.
3.  **Tool Isolation:** Restricting subagent tools to only what is necessary (e.g., the Test Agent doesn't need write access to your `.env`).
4.  **Model Selection:** Smart routing—using Sonnet/Opus for architectural decisions and Haiku for simple, repetitive data retrieval.



## 🛠️ Included Agents

| Agent | Icon | Responsibility | Output |
| :--- | :--- | :--- | :--- |
| **Explore** | 🔍 | Deep-dives into unknown directory structures and library docs. | Structured file maps. |
| **Pattern** | 🕸️ | Identifies architectural patterns and tech debt in the codebase. | Logic & Style summaries. |
| **Test** | ✅ | Executes test suites in parallel without cluttering main logs. | Pass/Fail reports. |
| **Synthesize** | 🌪️ | Collates findings from other agents into a unified action plan. | The Final Blueprint. |

## 🚀 Why Use SubAgent-Teams?

* **No Auto-Compact:** By keeping the main context window focused on decision-making, you avoid the "forgetfulness" that happens in long sessions.
* **Parallel Speed:** Tasks that would take 10 minutes sequentially (Research -> Fix -> Test) are completed in parallel, cutting execution time by up to 50%.
* **Reduced Costs:** Efficiently uses smaller context windows for sub-tasks, optimizing token usage.



## 💻 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/alijilani-dev/Claude.git](https://github.com/alijilani-dev/Claude.git)