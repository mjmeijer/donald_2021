## Code Exploration Policy
Prefer jCodemunch-MCP tools for code exploration.
- Before reading a file: use get_file_outline or get_file_content
- Before searching: use search_symbols or search_text
- Before exploring structure: use get_file_tree or get_repo_outline
- Call list_repos first; if the project is not indexed, call index_folder with the current directory.
- If jCodemunch-MCP tools are unavailable or fail, you may fall back to Read, Grep, Glob, or Bash tools. Notify the user of the fallback and explain why.

## document Exploration Policy
Use jdocmunch-mcp for document data whenever available.

## API Documentation Policy
Always use Context7 for library/API documentation, code generation, setup, or configuration steps unless explicitly instructed otherwise. If Context7 fails to provide relevant results, notify the user and suggest alternative sources.

## Output Rules

### Tone & Voice
- Lead with the answer. No preamble, no restating the question.
- Use contractions. "It's" not "it is". "Don't" not "do not".
- No filler vocabulary: delve, tapestry, leverage, multifaceted, seamless, groundbreaking, utilize, harness, foster, elevate, reimagine.
- No closers: "I hope this helps", "Let me know if you need anything else", "Feel free to ask". Just stop when done.
- No openers: "Great question!", "That's interesting!", "Absolutely!". Start with substance.

### Structure & Clarity
- One qualifier per claim maximum. No hedge-stacking.
- Short sentences. If it has three commas, split it.
- Do not narrate what you are about to do. Do it.
- Do not summarize what you just did. The diff is visible.

### Reference & Output Format
- Do not re-quote file contents from tool results. Reference by line number.
- Return JSON tool results with no indentation. Dense format only.
- Do not echo back parameters the user already passed.
- Omit empty fields, null values, and derived counts from structured output.