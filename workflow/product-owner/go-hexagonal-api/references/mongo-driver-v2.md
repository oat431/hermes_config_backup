# mongo-driver v2 breaking changes & patterns

Verified against `go.mongodb.org/mongo-driver/v2` v2.8.0 (2026-08).

## Breaking vs v1
| v1 pattern | v2 reality |
|---|---|
| `mongo.Connect(ctx, opts...)` | **`mongo.Connect(opts...) (*Client, error)` — no context param.** Connection is lazy; verify with `client.Ping(ctx, readpref.Primary())` |
| `go.mongodb.org/mongo-driver/bson/primitive` | **PACKAGE REMOVED** — `go mod tidy` fails with "does not contain package .../bson/primitive". Everything moved into `bson` directly: `bson.ObjectID`, `bson.ObjectIDFromHex(s)`, `bson.NilObjectID` |
| `mongo.IsDuplicateKeyError(err)` | unchanged, lives in `mongo` |
| `client.Disconnect(ctx)` | unchanged |
| `options.Client().ApplyURI(uri)` | unchanged |

## First-build go.sum noise
After `go get go.mongodb.org/mongo-driver/v2@latest`, the first `go build` reports many "missing go.sum entry" errors (pkcs8, klauspost/compress, xdg-go/scram, x/sync, ...). **Fix: `go mod tidy`** — don't chase the individual `go get` hints.

## Idempotent unique index at startup
```go
idx := mongo.IndexModel{
    Keys:    bson.D{{Key: "email", Value: 1}},
    Options: options.Index().SetUnique(true).SetName("ux_users_email"),
}
_, err := coll.Indexes().CreateOne(ctx, idx)  // same name+spec re-run = no-op
```

## Adapter error mapping pattern
- `mongo.ErrNoDocuments` → `domain.ErrNotFound`
- `mongo.IsDuplicateKeyError(err)` → `domain.ErrEmailExists`
- `time.Time` stored natively as BSON date; `bson.ObjectID` → hex string for the domain ID.
- Keep BSON tags (`bson:"password_hash"`) in the adapter doc struct only — domain entity carries JSON tags, not BSON.

## Layer rule (learned from a real bug)
Format validation (ObjectID hex shape) belongs in the **domain** layer, not the adapter. A fake repository bypasses adapter checks, turning invalid-ID requests into 404s instead of 400s. Domain check: `^[0-9a-fA-F]{24}$`.
