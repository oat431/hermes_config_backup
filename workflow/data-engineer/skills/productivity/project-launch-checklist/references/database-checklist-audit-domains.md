# Database & AI Checklist Audit Domains

Per-engine gap analysis reference for auditing production checklists. Each engine has unique operational concerns that a general checklist cannot cover. Use this when auditing or expanding engine-specific checklist files.

## Mandatory Cross-Cutting Sections (ALL engines)

Every production database checklist must have these three sections. They are the most commonly missing — application engineers think "does it work," data engineers think "is the data correct/safe/maintainable over time."

| Section | Core items |
|---|---|
| **Privacy & Data Protection** | PII inventory & classification, right to erasure (GDPR/CCPA/PDPA), data retention policy, anonymization/pseudonymization, consent tracking |
| **Data Quality** | DB-level constraints as quality gates, referential integrity verification, profiling on load, quality monitoring over time, natural key uniqueness edge cases |
| **Maintenance & Operations** | Autovacuum/compaction tuning, statistics freshness, maintenance window, deadlock detection, long-running transaction monitoring |

## Per-Engine Signature Features (must be present in engine-specific checklist)

### PostgreSQL
- Major version upgrade path (`pg_upgrade --link` vs logical replication)
- `pg_partman` for automated partition management
- pgvector HNSW vs IVFFlat tuning + `hnsw_ef_search`
- Logical replication for CDC / cross-version migration (`CREATE PUBLICATION`/`SUBSCRIPTION`)
- `pgcrypto` for column-level encryption
- `postgresql_anonymizer` for dynamic data masking
- Exclusion constraints (`EXCLUDE USING gist`) for range overlap prevention
- Domain types for reusable validation (`CREATE DOMAIN`)
- `lock_timeout` (not just `statement_timeout`)
- `pg_squeeze`/`pg_repack` for online index rebuilds

### MongoDB
- `$jsonSchema` validators with `validationLevel` and `validationAction` — **the #1 MongoDB data quality tool**
- Multi-document ACID transactions (4.0+), causal consistency sessions, retry on transient errors
- Queryable Encryption (7.0+) and CSFLE lifecycle management
- Change streams for CDC / cache invalidation / audit (`db.collection.watch()`)
- Resharding (5.0+) — shard keys are no longer permanent
- Time-series collections (5.0+)
- Connection pool settings (`maxPoolSize`, `connectTimeoutMS`, `socketTimeoutMS`)
- Read preference deliberate per use case
- `collMod` for updating validators on existing collections
- `cleanupOrphaned` for sharded cluster integrity
- Schema drift monitoring via `schemaVersion` distribution

### Valkey / Redis
- Cluster mode (16384 hash slots) vs Sentinel — decision documented with trade-offs
- Client-side caching (6.0+ tracking mode) — `CLIENT TRACKING ON`
- `LATENCY` command monitoring (`LATENCY DOCTOR`, `LATENCY HISTORY`)
- `activedefrag` for online memory defragmentation
- `MEMORY USAGE` and `OBJECT ENCODING` for capacity and encoding awareness
- I/O threading (`io-threads`, `io-threads-do-reads`)
- Async `DEL`/`UNLINK` for non-blocking big-key deletion
- PII in cache values identified and encrypted/excluded
- Cache purge procedure for data subject requests (GDPR/PDPA)
- Cache-DB consistency model documented per key group
- `WAIT` command for critical multi-replica writes

### Elasticsearch / OpenSearch
- Dedicated master nodes (3, odd quorum) — prevents split-brain
- Heap ≤ 31 GB (compressed oops threshold), 50% RAM for OS page cache
- `dynamic: strict` mapping to prevent mapping explosion
- Shard count deliberate (~20–50 GB per shard)
- `refresh_interval` tuned (not default `1s` during bulk load)
- ILM/ISM policies (hot → warm → cold → delete)
- Force merge read-only indices to 1 segment
- `search_after` for pagination (not `from` + `size` for deep pages)
- Filter context over query context (cacheable, no scoring)
- Thread pool rejections monitored
- Circuit breakers monitored (`parent`, `fielddata`, `request`)
- Snapshots to object storage (S3), incremental
- Document-level security (DLS) / field-level security (FLS) for multi-tenant

### ClickHouse
- MergeTree family selection (Replacing/Aggregating/Collapsing/Summing) — never plain MergeTree when dedup needed
- `ORDER BY` is the primary index (sparse, query-pattern-driven)
- Batch inserts ONLY (10K+ rows per insert, never single-row)
- No UPDATE/DELETE in hot paths — use CollapsingMergeTree or ReplacingMergeTree
- Materialized views for pre-aggregation (`AggregatingMergeTree` target)
- Dictionaries for dimension lookups (no big JOINs)
- `PREWHERE`, `LIMIT BY`, `argMax()` — ClickHouse-specific optimizations
- `system.query_log` as primary observability table
- Part count monitored (not approaching `parts_to_throw_insert`)
- `max_memory_usage` + `max_bytes_before_external_group_by` set
- TTL for data lifecycle + tiered storage movement
- ClickHouse Keeper (C++ built-in) or ZooKeeper for replication
- `BACKUP`/`RESTORE` (24.3+) or `clickhouse-backup` (Altinity) for older versions

### SQLite
- WAL mode enabled (`PRAGMA journal_mode = WAL`) — single most important config
- Single-writer model understood — `BEGIN IMMEDIATE` for write transactions
- `busy_timeout` set (5000+ ms)
- `synchronous = NORMAL` (not FULL unless data-loss-intolerant)
- `foreign_keys = ON` (off by default — most commonly missed config)
- `cache_size` increased from default 2MB
- `PRAGMA` persistence understood (most are per-connection)
- `.backup` command or online backup API (NOT direct file copy with active writes)
- `PRAGMA integrity_check` scheduled periodically
- SQLCipher / SEE for encryption at rest
- Honest tier warning: SQLite is Tier 1–4; at Tier 5+, recommend migrating to PostgreSQL

### Cassandra / ScyllaDB
- Query-first data modeling (not normalization-first) — one table per query pattern
- Partition key design (high cardinality, bounded size < 100MB, time-bucketed)
- Tunable consistency per operation (`LOCAL_QUORUM` production default)
- Compaction strategy (STCS/LCS/TWCS) matched to data pattern
- Tombstone ratio monitored (< 0.2)
- `gc_grace_seconds` and node repair within that window
- NetworkTopologyStrategy (never SimpleStrategy in production)
- Correct snitch for deployment topology
- LWT (Paxos) used sparingly — 4x latency, doesn't scale under contention
- Read-before-write anti-pattern avoided
- ScyllaDB shard-per-core architecture (no JVM GC tuning)
- Multi-DC as disaster recovery (driver config failover)
- Honest tier warning: overkill below Tier 4

## AI / LLM Checklist Audit

### Mandatory sections beyond the application layer
- **Model Lifecycle & MLOps** — model registry, artifact versioning (hash-pinned), serving infrastructure (vLLM/TGI/Triton), deployment strategy (canary/blue-green), rollback procedure, GPU resource management
- **Fine-Tuning & Custom Models** — justify over alternatives (prompting → few-shot → RAG → structured output first), LoRA/QLoRA vs full fine-tune, overfitting/catastrophic forgetting, eval comparison vs base, quantization for inference

### Behavioral monitoring (not just ops monitoring)
- Input drift detection (topics/languages/formats shifting from tested envelope)
- Output quality tracked over time (hallucination rate, feedback trends)
- Toxicity/safety trend monitored (guardrail trigger rate over time)
- Prompt regression detection (run golden set against production daily)

### RAG data pipeline (not just query-time retrieval)
- Ingestion pipeline: extract → clean → chunk → embed → index (idempotent, observable)
- Freshness SLA defined and monitored
- Re-indexing strategy for embedding model changes (dual-index transition)
- Incremental updates (document hash tracking)
- Ingestion data quality (OCR errors, encoding issues — critical for Thai text)

### Evaluation rigor
- Eval dataset versioned alongside model + prompt versions (provenance)
- Statistical significance (bootstrap CIs, paired tests — AI outputs are noisy)
- Human evaluation workflow (inter-rater agreement Cohen's κ ≥ 0.6)
