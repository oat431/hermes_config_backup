# gRPC on Windows without a package manager — setup + codegen + tests

Verified 2026-08 on Windows 11 (git-bash), Go 1.25, protoc 35.1, grpc v1.83.

## 1. Install protoc (no choco/scoop needed)

Download the official win64 zip from GitHub releases into a **gitignored** `tools/` dir:

```bash
VER=$(curl -sL https://api.github.com/repos/protocolbuffers/protobuf/releases/latest \
      | grep -o '"tag_name": *"v[0-9.]*"' | head -1 | sed 's/.*"v\([0-9.]*\)".*/\1/')
mkdir -p tools/protoc
curl -sL -o tools/protoc.zip "https://github.com/protocolbuffers/protobuf/releases/download/v${VER}/protoc-${VER}-win64.zip"
unzip -oq tools/protoc.zip -d tools/protoc && rm tools/protoc.zip
tools/protoc/bin/protoc --version
```

Add `tools/` to `.gitignore`. `C:\Users\<user>\go\bin` must be on PATH (it is on this
machine) so the Go plugins below are reachable.

## 2. Go plugins

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

## 3. Codegen — use module= mode, not paths=source_relative

With proto `option go_package = "github.com/<owner>/<repo>/gen/userservice/v1;userservicev1";`:

```makefile
PROTOC ?= tools/protoc/bin/protoc
gen-proto:
	rm -rf gen
	$(PROTOC) --go_out=. --go_opt=module=github.com/<owner>/<repo> \
	          --go-grpc_out=. --go-grpc_opt=module=github.com/<owner>/<repo> \
	          proto/user_service/v1/user_service.proto
```

- `module=<modpath>` strips the module prefix from `go_package` → output lands exactly at
  `gen/userservice/v1/`.
- `paths=source_relative` instead dumps output under `gen/proto/user_service/v1/` which
  does NOT match `go_package` — the classic silent mismatch.
- protoc requires the output dir to exist; with `module=` and `--go_out=.` it does. If you
  keep `paths=source_relative`, `mkdir -p gen` first.
- Commit generated code — keeps the reviewer build free of protoc.
- On a module rename: update `go.mod` + all imports + proto `go_package` + the Makefile
  `module=` flag, then `rm -rf gen && make gen-proto`.

## 4. Server wiring essentials

```go
grpcSrv := grpc.NewServer(grpc.UnaryInterceptor(grpcapi.UnaryAuthInterceptor(authSvc)))
userservicev1.RegisterUserServiceServer(grpcSrv, grpcapi.NewServer(users))
reflection.Register(grpcSrv) // REQUIRED for grpcurl discovery
```

Auth interceptor: read `metadata.FromIncomingContext(ctx)`, get `md.Get("authorization")`,
strip the `Bearer ` prefix, call the same `AuthService.VerifyToken` the REST middleware
uses, reject with `status.Error(codes.Unauthenticated, ...)`.

Graceful shutdown with timeout fallback:

```go
grpcStopped := make(chan struct{})
go func() { grpcSrv.GracefulStop(); close(grpcStopped) }()
select {
case <-grpcStopped:
case <-time.After(5 * time.Second):
    grpcSrv.Stop()
}
```

## 5. bufconn tests (no real network)

```go
lis := bufconn.Listen(1 << 20)
srv := grpc.NewServer(grpc.UnaryInterceptor(...))
userservicev1.RegisterUserServiceServer(srv, grpcapi.NewServer(users))
go func() { _ = srv.Serve(lis) }()
t.Cleanup(srv.Stop)

conn, _ := grpc.NewClient("passthrough:///bufnet",
    grpc.WithContextDialer(func(ctx context.Context, _ string) (net.Conn, error) {
        return lis.DialContext(ctx)
    }),
    grpc.WithTransportCredentials(insecure.NewCredentials()),
)
```

Assert codes with `status.Code(err)` against `codes.NotFound`, `codes.Unauthenticated`,
`codes.InvalidArgument`, `codes.AlreadyExists`. Send tokens via
`metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+token)`.

## 6. grpcurl verification

```bash
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
grpcurl -plaintext localhost:50051 list                    # needs reflection
grpcurl -plaintext -H "authorization: Bearer $TOKEN" \
  -d '{"name":"X","email":"x@y.z","password":"abcdefgh"}' \
  localhost:50051 userservice.v1.UserService/CreateUser
```
