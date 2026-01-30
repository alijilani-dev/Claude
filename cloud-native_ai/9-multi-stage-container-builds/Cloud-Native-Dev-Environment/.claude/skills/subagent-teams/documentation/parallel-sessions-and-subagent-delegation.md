  ---

# How Parallel Sessions & Subagent Delegation Works

  The Core Problem

  When Claude does all work in a single session (reading files, searching, reasoning, implementing), the context window fills up quickly, triggering auto-compact — which loses nuance and earlier
  context, degrading performance.

  The Solution: Subagent Delegation

  Each subagent runs in its own isolated context window. The main orchestrator only receives compact synthesized results, keeping its context lean and focused. 

  Key Benefits

| Without Subagents              | With Subagents                  |
| ------------------------------ | ------------------------------- |
| All work fills ONE context     | Each task gets SEPARATE context |
| Sequential execution (10 min)  | Parallel execution (5 min)      |
| Auto-compact triggers often    | Main context stays small        |
| Performance degrades over time | Consistent quality throughout   |

  The Four Pillars of Delegation

1. Specialization — Each subagent has a focused domain

2. Domain-specific prompts — Targeted reasoning per task

3. Tool isolation — Restrict capabilities to reduce bloat

4. Model selection — Opus/Sonnet for complex work, Haiku for simple tasks
   Best Strategy in Practice
   Main Orchestrator (lean context, decision-making only)
   ├── Explore Agent: Research codebase → returns summary
   ├── Explore Agent: Find patterns → returns summary
   ├── General Agent: Run tests → returns pass/fail
   └── Orchestrator: Synthesize → Execute with full context available
   Key rules:
- Delegate all heavy exploration/search to subagents

- Launch independent tasks in parallel (multiple Task tool calls in one message)

- Keep the main session for synthesis and final implementation

- Never read many files or do long search chains directly in main context
  The plan file has been written with full details. Would you like me to clarify anything, or shall I exit plan mode?

● User approved Claude's plan
  ⎿  Plan saved to: C:\Users\Acer\.claude\plans\unified-launching-crab.md · /plan to edit
     Parallel Sessions & Subagent Delegation Strategy
     Summary from agentfactory.panaversity.org

     The page describes how delegating work to subagents enables parallel execution and preserves the main orchestrator's context window, preventing auto-compaction and maintaining Claude's
     performance.

     ---
     Key Concepts

     1. Why Subagents Preserve Context Window

     - Each subagent runs in its own isolated context — work done by subagents does NOT consume the main Claude session's context
     - The orchestrator only receives synthesized results (compact summaries), not the full exploration/reasoning
     - This prevents the main session from hitting context limits and triggering auto-compact (which loses nuance and earlier context)

     2. Parallel Execution Model

     | Approach                  | Time                                    | Context Impact                    |
     |---------------------------|-----------------------------------------|-----------------------------------|
     | Sequential (no subagents) | Sum of all tasks (e.g., 5+3+2 = 10 min) | All work fills ONE context window |
     | Parallel (with subagents) | Longest single task (e.g., 5 min)       | Each task in SEPARATE context     |

     3. Four Pillars of Subagent Delegation

     1. Specialization via description — Each subagent has a focused expertise domain
     2. Reasoning frameworks through prompts — Domain-specific system prompts for targeted thinking
     3. Tool isolation — Restrict capabilities to prevent unintended actions and reduce context bloat
     4. Model selection — Use Opus/Sonnet for complex reasoning, Haiku for straightforward tasks

     ---
     Best Strategy to Implement This Approach

     When to Delegate to Subagents

     - Tasks are independent (no sequential dependencies between them)
     - Specialization matters (different domains like testing, code review, exploration)
     - Parallelism saves meaningful time
     - Tool isolation is needed (e.g., read-only exploration vs. write operations)
     - Context window is tight — the main session is already large

     Implementation Pattern

     Main Orchestrator (minimal context usage)
     ├── Subagent 1: Explore codebase (read-only, returns summary)
     ├── Subagent 2: Run tests (bash, returns pass/fail)
     ├── Subagent 3: Review code (read-only, returns findings)
     └── Orchestrator: Synthesize results → Execute plan

     Practical Steps in Claude Code

     1. Use the Task tool to spawn subagents for heavy lifting:
       - subagent_type=Explore for codebase research
       - subagent_type=Plan for architecture design
       - subagent_type=general-purpose for multi-step autonomous tasks
     2. Launch multiple agents in parallel (single message, multiple Task tool calls):
       - Independent searches/explorations run simultaneously
       - Each gets its own context window
       - Results come back as compact summaries
     3. Keep the main session lean:
       - Don't read large files directly — delegate to subagents
       - Don't do extensive grep/search chains — use Explore agents
       - Reserve the main context for decision-making and synthesis
     4. Result synthesis:
       - Subagents return focused, structured outputs
       - Orchestrator combines findings into unified action plan
       - Only essential information enters the main context

     Anti-Patterns to Avoid

     - ❌ Reading many files directly in the main session
     - ❌ Running long sequential search chains in main context
     - ❌ Doing exploration AND implementation in the same context
     - ❌ Using one agent for everything when tasks are independent

     Benefits

     - No auto-compact — main context stays small and focused
     - Better reasoning — Claude has full context available for decisions
     - Faster execution — parallel tasks complete in time of longest single task
     - Specialization — each subagent optimized for its specific task
     - Cost optimization — use cheaper models (Haiku) for simple tasks

● The plan has been approved. Since this was primarily a research and information-sharing task (understanding the subagent delegation strategy from the documentation), the work is complete. The
  plan file at C:\Users\Acer\.claude\plans\unified-launching-crab.md contains the full strategy document you can reference anytime.

  Key takeaway: To implement this approach in your own Claude Code sessions, always delegate heavy exploration, searching, and independent tasks to subagents using the Task tool — this keeps your
  main context window lean, avoids auto-compact, and maintains Claude's reasoning quality throughout long sessions.
