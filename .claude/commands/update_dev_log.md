---
description: Update today's dev log with current progress, issues, and attempts
---

You are updating the development log for this project. Follow these steps:

## 1. Determine Today's Dev Log File

- Today's date is provided in the <env> section of your system prompt
- Dev log filename format: `DEV_LOG_YYYY-MM-DD.md` (e.g., `DEV_LOG_2025-11-24.md`)
- Check if a dev log file exists for today

## 2. Analyze Recent Context

Review the recent conversation to identify:
- **Current task/goal**: What are we trying to accomplish?
- **Issues faced**: What problems or blockers have come up?
- **Attempts made**: What have we tried so far?
- **Current approach**: What are we currently working on?
- **Results**: What were the outcomes (success, failure, partial success)?
- **Decisions made**: Any technical decisions or direction changes?
- **Next steps**: What should we try next?

## 3. Update the Dev Log

**If dev log exists for today:**
- Read the existing file
- Add a new timestamped section at the end, MAKE SURE YOU USE CORRECT LOCAL TIME
- Use format: `## HH:MM AM/PM - Brief Title`
- Append new content without modifying existing entries
- Add NAME OF BRANCH that we are working on regarding this dev log entry. 
- Add all relevant files, e.g. PRD.md, and files we've been editing/troubleshooting. 

**If no dev log exists for today:**
- Create a new dev log file with today's date, in the proper /dev-logs folder (this folder should be git-ignored)
- Use this header structure:
  ```markdown
  # Development Log - Month Day, Year

  ## Session Start: YYYY-MM-DD

  ---
  ```
- Add the first timestamped entry

## 4. Entry Content Format

Each entry should include relevant sections (omit sections if not applicable):

```markdown
## HH:MM AM/PM - Brief Descriptive Title

### Context
Brief summary of what we're working on.

### Issue/Problem
What problem or challenge came up?

### What We Tried
- Approach 1: Result
- Approach 2: Result
- etc.

### Current Status
Where things stand now.

### Results/Findings
What did we learn or discover?

### Decisions Made
Any technical decisions or direction changes.

### Next Steps
- [ ] Task 1
- [ ] Task 2

---
```

## 5. Writing Style

- Be concise but informative
- Use bullet points for lists of attempts or findings
- Include code snippets or file paths when relevant
- Use checkboxes for next steps/tasks
- Add horizontal rules (`---`) between major sections
- Use appropriate time (estimate based on conversation flow)

## 6. Execute the Update

After analyzing the context:
1. Determine the appropriate timestamp for this entry
2. Write a descriptive title that captures what this entry is about
3. Fill in relevant sections based on recent conversation
4. Either append to existing dev log or create new one
5. Confirm to the user what was added

## Important Notes

- Focus on technical details and decisions, not just "what we did"
- Capture the "why" behind decisions
- Document failed attempts (they're valuable!)
- Be honest about current status (working, blocked, uncertain, etc.)
- One dev log file per day - always append to today's file if it exists
