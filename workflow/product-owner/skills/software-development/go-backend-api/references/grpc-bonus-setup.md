# gRPC bonus setup for a Go service (verified 2026-08)

## Toolchain on Windows (no choco/scoop)

```bash
# protoc binary — official win64 zip into a gitignored tools/ dir
VER=$(curl -sL https://api.github.com/repos/protocolbuffers/protobuf/releases/latest | grep -o '"tag_name": *"v[0-9.]*"' | head -1 | sed 's/.*"v\([0-9.]*\)".*/\1/')
mkdir -p tools/protoc && curl -sL -o tools/protoc.zip "https://github.com/protocolbuffers/protobuf/releases/download/v${VER}/protoc-${VER}-win64.zip"
unzip -oq tools/protoc.zip -d tools/protoc && rm tools/protoc.zip

# Go plugins + grpcurl (GOPATH/bin must be on PATH — verify with `go env GOPATH`)
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
```

## Proto generation — use module= mode

`paths=source_relative` lands output at `gen/proto/user_service/v1/` (mirrors source tree — ugly). Instead:

```makefile
gen-proto:
	rm -rf gen
	$(PROTOC) --go_out=. --go_opt=module=github.com/<owner>/<repo> \
	       --go-grpc_out=. --go-grpc_opt=module=github.com/<owner>/<repo> \
	       proto/user_service/v1/user_service.proto
```

produces clean `gen/userservice/v1/`. `go_package` in the .proto must be `github.com/<owner>/<repo>/gen/userservice/v1;userservicev1`. Module rename = update go.mod + proto go_package + Makefile module= flag + regenerate (sed everything, then `make gen-proto`).

## Server wiring — reflection is REQUIRED for grpcurl

```go
grpcSrv := grpc.NewServer(grpc.UnaryInterceptor(grpcapi.UnaryAuthInterceptor(authSvc)))
userservicev1.RegisterUserServiceServer(grpcSrv, grpcapi.NewServer(users))
reflection.Register(grpcSrv) // WITHOUT THIS: "server does not support the reflection API"
```

Auth interceptor reads metadata: `metadata.FromIncomingContext(ctx)`, key `"authorization"`, value `"Bearer <token>"`; reject with `status.Error(codes.Unauthenticated, ...)`. Reuse the SAME token verifier as the REST middleware (one policy, two adapters).

## Tests — bufconn, no real network

```go
lis := bufconn.Listen(1 << 20)
srv := grpc.NewServer(grpc.UnaryInterceptor(grpcapi.UnaryAuthInterceptor(authSvc)))
go srv.Serve(lis)
conn, _ := grpc.NewClient("passthrough:///bufnet",
	grpc.WithContextDialer(func(ctx context.Context, _ string) (net.Conn, error) { return lis.DialContext(ctx) }),
	grpc.WithTransportCredentials(insecure.NewCredentials()))
```

Send tokens via `metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+token)`. Assert codes via `status.Code(err)`.

## Graceful stop

`GracefulStop()` blocks until in-flight RPCs drain — run in a goroutine with a timeout fallback to hard `Stop()` (5s worked well). Sequence: HTTP Shutdown → grpc GracefulStop → cancel worker ctx → mongo Disconnect.

## Live verification

```bash
grpcurl -plaintext localhost:50051 list                                # reflection discovery
grpcurl -plaintext -H "authorization: Bearer $TOKEN" -d '{"name":"X","email":"x@y.z","password":"long-enough"}' \
  localhost:50051 userservice.v1.UserService/CreateUser
grpcurl -plaintext -d '{"id":"..."}' localhost:50051 userservice.v1.UserService/GetUser  # → Unauthenticated
```
