## Code Exploration Policy
Always use jCodemunch-MCP tools — never fall back to Read, Grep, Glob, or Bash for code exploration.
- Before reading a file: use get_file_outline or get_file_content
- Before searching: use search_symbols or search_text
- Before exploring structure: use get_file_tree or get_repo_outline
- Call list_repos first; if the project is not indexed, call index_folder with the current directory.

## document Exploration Policy
Use jdocmunch-mcp for document data whenever available.

## Output Rules
Apply these rules to every response. No exceptions.

- Lead with the answer. No preamble, no restating the question.
- Use contractions. "It's" not "it is". "Don't" not "do not".
- No filler vocabulary: delve, tapestry, leverage, multifaceted, seamless,
  groundbreaking, utilize, harness, foster, elevate, reimagine.
- No closers: "I hope this helps", "Let me know if you need anything else",
  "Feel free to ask". Just stop when done.
- No openers: "Great question!", "That's interesting!", "Absolutely!".
  Start with substance.
- One qualifier per claim maximum. No hedge-stacking.
- Short sentences. If it has three commas, split it.
- Do not narrate what you are about to do. Do it.
- Do not summarize what you just did. The diff is visible.
- Do not re-quote file contents from tool results. Reference by line number.
- Return JSON tool results with no indentation. Dense format only.
- Do not echo back parameters the user already passed.
- Omit empty fields, null values, and derived counts from structured output.