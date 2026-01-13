#!/usr/bin/env bash
# .claude/hooks/study-workflow-orchestrator.sh

input=$(cat)
hook_event=$(echo "$input" | jq -r '.hook_event_name')
subagent_type=$(echo "$input" | jq -r '.subagent_type // ""')

# State tracking (persisted in temporary file)
STATE_FILE="$CLAUDE_PROJECT_DIR/.claude/workflow-state.json"

case "$hook_event" in
"UserPromptSubmit")
    # Detect workflow trigger and inject orchestration context
    user_message=$(echo "$input" | jq -r '.user_message')

    if [[ "$user_message" =~ "start study workflow" ]]; then
    # Initialize workflow state
    echo '{"stage": "study-notes", "topic": "..."}' > "$STATE_FILE"

    # Inject context to guide Claude toward invoking study-notes agent
    cat <<EOF | jq -c
{
"continue": true,
"hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "User has requested study workflow orchestration. Invoke agents in sequence: study-notes → tutor-agent → 
flashcard-agent → quiz-master."
}
}
EOF
    fi
    ;;

"SubagentStop")
    # Check current workflow stage and determine next action
    current_stage=$(jq -r '.stage' "$STATE_FILE" 2>/dev/null || echo "none")

    case "$current_stage" in
    "study-notes")
        # Update state to next stage
        jq '.stage = "tutor-agent"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

        # Block the stop to add context for next agent invocation
        cat <<EOF | jq -c
{
"decision": "block",
"reason": "Proceeding to tutor-agent phase. Please invoke the tutor-agent with the study-notes output as context."
}
EOF
        ;;
    # Similar logic for other stages...
    esac
    ;;
esac

exit 0