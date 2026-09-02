# mongo-driver v2 Gotchas (verified against v2.8.0)

Breaking changes from the v1 driver that produce confusing compile errors.

## API differences

| v1 | v2 | Notes |
|----|----|-------|
| `go.mongodb.org/mongo-driver/bson/primitive.ObjectID` | `go.mongodb.org/mongo-driver/v2/bson.ObjectID` | **`bson/primitive` package removed entirely** — compiler says "module does not contain package bson/primitive". Everything (`ObjectID`, `ObjectIDFromHex`, `NilObjectID`) lives in `bson` directly |
| `mongo.Connect(ctx, opts...)` | `mongo.Connect(opts ...*options.ClientOptions) (*Client, error)` | **No ctx parameter** — pass context to `Ping`/operations instead |
| `client.Ping(ctx, rp)` | unchanged signature | `readpref.Primary()` still in `v2/mongo/readpref` |
| `mongo.IsDuplicateKeyError(err)` | unchanged | use for unique-index → domain error mapping |

## Correct setup sequence (v2)

```go
client, err := mongo.Connect(options.Client().
    ApplyURI(uri).
    SetMaxPoolSize(50).SetMinPoolSize(5).
    SetServerSelectionTimeout(5*time.Second))
// then verify:
pingCtx, cancel := context.WithTimeout(ctx, 10*time.Second)
defer cancel()
if err := client.Ping(pingCtx, readpref.Primary()); err != nil { ... }
```

## First `go get` friction

After adding the dependency, `go build` reports "missing go.sum entry for module providing package github.com/klauspost/compress/..." etc. — run `go mod tidy` once to resolve the transitive go.sum graph; not a code problem.

## Idempotent unique index at startup

```go
idx := mongo.IndexModel{
    Keys:    bson.D{{Key: "email", Value: 1}},
    Options: options.Index().SetUnique(true).SetName("ux_users_email"),
}
_, _ = coll.Indexes().CreateOne(ctx, idx) // same name+spec = no-op on re-run
```

Duplicate-key → `mongo.IsDuplicateKeyError(err)` → map to domain sentinel (e.g. `ErrEmailExists`) in the adapter.
