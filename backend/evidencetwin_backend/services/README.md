# Application services

- runtime.py: existing Blueprint-to-application binding, typed transport validation,
  application CRUD/filtering/comparison and truthful capability metadata.
- store.py: private local SQLite JSON records and uploads.
- workflow.py: bounded review jobs, actual transitions, cancellation, restart
  recovery, audit and clearly unverified exploratory reports.
- provider.py: strict owner reviewer/cross-review/judge schemas, reference integrity,
  packaged instructions and Ollama transport adapted from snippets/VA.py.
- transports.py: OpenAI, Gemini, Anthropic, OpenRouter and DeepSeek transport
  adapters adapted from snippets/all.py.

No source authentication, statistical inference, neutral-chart generation,
benchmark scoring, MCP server or multi-user authentication is implemented. See the
root implementation guide before enabling or deploying scientific capabilities.
