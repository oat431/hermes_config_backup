# mongo-driver v2 — breaking changes from v1

Verified against `go.mongodb.org/mongo-driver/v2 v2.8.0` (2026-08). When code or docs from
tutorials written against v1 fails to compile, this is the map.

## Breaking changes (v1 → v2)

| Concern | v1 | v2 |
|---|---|---|
| ObjectID type | `go.mongodb.org/mongo-driver/bson/primitive.ObjectID` | `go.mongodb.org/mongo-driver/v2/bson.ObjectID` — **the whole `bson/primitive` package is gone** |
| Parse ID | `primitive.ObjectIDFromHex(s)` | `bson.ObjectIDFromHex(s)` |
| Nil ID | `primitive.NilObjectID` | `bson.NilObjectID` |
| Connect | `mongo.Connect(ctx, opts...)` | `mongo.Connect(opts ...*options.ClientOptions)` — **no ctx**; lazy connect, verify with `Ping` |
| Ping / Disconnect | `Ping(ctx, rp)` / `Disconnect(ctx)` | unchanged |
| Duplicate-key check | `mongo.IsDuplicateKeyError(err)` | unchanged |
| Index model | `mongo.IndexModel{Keys, Options: options.Index().SetUnique(true).SetName(...)}` | unchanged |
| ErrNoDocuments | `mongo.ErrNoDocuments` | unchanged |

## Gotchas

1. **After `go get` on the v2 driver, `go build` fails with `missing go.sum entry`** for
   transitive deps (`github.com/klauspost/compress/snappy`, `github.com/xdg-go/scram`,
   `golang.org/x/sync/...`, `github.com/youmark/pkcs8`). Fix: `go mod tidy` once.
2. Verify signatures fast with `go doc` instead of guessing:
   `go doc go.mongodb.org/mongo-driver/v2/mongo.Connect`
3. `CreateOne` index creation is idempotent for the same name+spec — safe to call at startup.

## Minimal working snippets (v2)

```go
client, err := mongo.Connect(options.Client().ApplyURI(cfg.MongoURI))
if err != nil { /* ... */ }

ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
if err := client.Ping(ctx, readpref.Primary()); err != nil { /* ... */ }

idx := mongo.IndexModel{
    Keys:    bson.D{{Key: "email", Value: 1}},
    Options: options.Index().SetUnique(true).SetName("ux_users_email"),
}
_, err = db.Collection("users").Indexes().CreateOne(ctx, idx)

// insert + translate race-proof duplicate
res, err := coll.InsertOne(ctx, doc)
if err != nil {
    if mongo.IsDuplicateKeyError(err) {
        return domain.ErrEmailExists
    }
    return err
}
```

## BSON vs JSON separation (domain purity)

Keep `bson` tags out of the domain package. Domain struct carries `json` tags only; the
persistence adapter owns a private `userDoc` with `bson` tags and maps to/from the domain
entity (`_id` ObjectID ↔ hex string ID). This keeps domain stdlib-only and lets the
in-memory test fake implement the repository port without any Mongo types.
