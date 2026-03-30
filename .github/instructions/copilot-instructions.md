## Code Exploration Policy
Always use jCodemunch-MCP tools — never fall back to Read, Grep, Glob, or Bash for code exploration.
- Before reading a file: use get_file_outline or get_file_content
- Before searching: use search_symbols or search_text
- Before exploring structure: use get_file_tree or get_repo_outline
- Call list_repos first; if the project is not indexed, call index_folder with the current directory.

## txt file Exploration Policy
Use jdatamunch-mcp for tabular data whenever available.
Always call describe_dataset first to understand the schema.
Use get_rows with filters rather than loading raw files.
Use aggregate for any group-by or summary questions.
