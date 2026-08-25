# MongoDB Go driver v2 — gotchas (v2.8.0, verified 2026-08)

The v2 line (2025+) breaks several v1 idioms. Always confirm with `go doc go.mongodb.org/mongo-driver/v2/<pkg>.<Symbol>` before writing main.go.

## Package moves

| v1 | v2 |
|----|-----|
| `bson/primitive.ObjectID` | `bson.ObjectID` (the whole `bson/primitive` package is GONE) |
| `bson/primitive.ObjectIDFromHex` | `bson.ObjectIDFromHex` |
| `bson/primitive.NilObjectID` | `bson.NilObjectID` |
| `bson.D`, `bson.M` | unchanged (`bson` pkg) |

## Signature changes

- `mongo.Connect(opts ...*options.ClientOptions) (*Client, error)` — **no context parameter** (v1 had `Connect(ctx, opts)`). Connection is lazy; verify with `client.Ping(ctx, readpref.Primary())` and fail fast.
- `client.Ping(ctx, readpref)` and `client.Disconnect(ctx)` still take ctx.
- `mongo.IsDuplicateKeyError(err)` unchanged — map it to a domain `ErrEmailExists`-style sentinel.
- `mongo.ErrNoDocuments` unchanged — map to domain `ErrNotFound`.

## Error signatures you'll hit

- `no required module provides package go.mongodb.org/mongo-driver/v2/bson/primitive` → you imported the removed package; move to `bson`.
- `missing go.sum entry for module providing package github.com/klauspost/compress/snappy ...` (and xdg-go, youmark/pkcs8, x/sync) → just `go mod tidy`; these are transitive deps of the driver.

## Patterns

- Unique index creation is idempotent via `coll.Indexes().CreateOne(ctx, mongo.IndexModel{Keys: bson.D{{Key:"email", Value:1}}, Options: options.Index().SetUnique(true).SetName("ux_users_email")})` — safe to run on every startup.
- Adapter boundary: BSON struct lives in the adapter (`userDoc` with `bson:` tags); domain entity keeps only `json:` tags. Convert in both directions in the adapter.
- Duplicate-email race: friendly pre-check in the application layer + unique index as the race-proof backstop (`IsDuplicateKeyError` → 409).
- Read-back after write (`FindOne` by oid) extracted as one `getByObjectID` helper, reused by `FindByID` and `Update` — avoids DRY smell.
