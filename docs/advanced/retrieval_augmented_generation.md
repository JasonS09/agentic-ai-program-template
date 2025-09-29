# Retrieval Augmented Generation (RAG)

## Pipeline Stages
1. Ingest → chunk documents
2. Embed → vector store
3. Retrieve → top-k relevant chunks
4. Augment → construct prompt with context
5. Generate → model answer
6. Evaluate → grounding & correctness

## Chunking Tips
| Issue | Symptom | Adjustment |
|-------|---------|------------|
| Too large | Truncation | Reduce max tokens per chunk |
| Too small | Fragmented context | Merge with overlap (sliding window) |

## Prompt Skeleton
```
SYSTEM: You answer using ONLY the provided context.
CONTEXT (max 1200 tokens):
<<<
{retrieved_chunks}
>>>
USER QUESTION: {question}
If answer not in context, say "Insufficient context." Do not guess.
```

## Grounding Evaluation
- Exact citation presence
- Percentage of answer sentences backed by a chunk
- Adversarial test: excluded relevant chunk → should degrade gracefully

## Vector Store Selection
| Option | Strength | Tradeoff |
|--------|----------|----------|
| Chroma | Simple local | Scaling limits |
| Pinecone | Managed scaling | Cost |
| Weaviate | Hybrid search | Setup overhead |

## Failure Modes
| Mode | Cause | Mitigation |
|------|------|-----------|
| Hallucinated facts | Missing context | Increase k, better chunking |
| Irrelevant retrieval | Poor embeddings | Domain-specific model |
| Context overflow | Over-collection | Dynamic truncation w/ scoring |
| Latency spikes | External store | Batch + warm connections |

## Optimization
- Rerank top-k with cross-encoder for precision
- Cache retrieval results for repeated queries

## Security Note
Sanitize & classify ingested documents before indexing.
