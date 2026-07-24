# Memory Integration with Context Engine

The Context Engine integrates seamlessly with conversation memory, key-value stores, and vector memory.

## Integration Architecture

- `MemoryContextProvider`: Recalls user preferences and fact lists.
- `KnowledgeContextProvider`: Integrates RAG vector index chunks.
- Priority Management: Memory fragments are assigned `Priority 7`, allowing automatic summarization or pruning when input token budgets are constrained.
