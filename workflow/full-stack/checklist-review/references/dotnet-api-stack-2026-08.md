# .NET/C# API Stack Research — 2026-08-05

Research conducted for future `dotnet-api.md` checklist creation. Not yet applied to a checklist file.

## Framework
- **ASP.NET Core 10** (.NET 10 LTS, released Nov 2025, support until Nov 2028)
- **C# 14** — new features: `field` keyword, extension blocks, null-conditional assignment (`?.=`), `nameof` for unbound generics
- **Minimal APIs** (preferred for new projects) — lower overhead than controllers, built-in validation, full AOT support
- **Controllers** (still supported) — better for complex enterprise apps with filters, model binding, attribute routing

## Architecture & Structure
- **Clean Architecture** (Jason Taylor template — industry standard):
  - `Application/` — business logic, CQRS handlers (MediatR)
  - `Domain/` — entities, value objects
  - `Infrastructure/` — EF Core, external services
  - `WebApi/` — endpoints, configuration
- **Feature Folders** (simpler alternative) — group by feature with `Endpoints.cs`, `Commands/`, `Queries/`, `Validators/`
- **MediatR** — CQRS pattern, pipeline behaviors for validation/logging/caching
- **AutoMapper** — object mapping (DTOs ↔ entities)

## ORM & Data Access
- **Entity Framework Core 10** (recommended default):
  - New: vector search (`SqlVector<float>` for AI/RAG), native JSON support (SQL Server 2025+)
  - Providers: SQL Server, PostgreSQL, SQLite, MySQL, Cosmos DB
- **Dapper** (micro-ORM) — raw SQL, performance-critical queries, often used alongside EF Core
- **Marten** — PostgreSQL document DB + event sourcing (for event-driven architectures)

## Validation
- **FluentValidation** (industry standard):
  ```csharp
  RuleFor(x => x.Email).EmailAddress().WithMessage("Invalid email");
  ```
  - Auto-registered via `AddValidatorsFromAssembly()`
  - Integrates with Minimal APIs (`AddValidation()`) and controllers
- **DataAnnotations** — simpler, attribute-based (`[Required]`, `[EmailAddress]`)

## Dependency Injection
- **Built-in container** (recommended):
  - `AddTransient<T>()` — new instance per request
  - `AddScoped<T>()` — one per HTTP request
  - `AddSingleton<T>()` — app lifetime
- **Scrutor** — decorators, advanced registration patterns
- **Keyed services** (.NET 8+) — named registrations

## Configuration
- **appsettings.json** + environment-specific files (`appsettings.Production.json`)
- **User secrets** — `dotnet user-secrets` for local dev (never committed)
- **Azure Key Vault** — production secrets via `AddAzureKeyVault()`
- **Strongly-typed config** — `IOptions<T>` pattern with `Configure<T>()`

## Authentication & Authorization
- **JWT Bearer** — `AddJwtBearer()` with RS256 (asymmetric keys)
- **Duende IdentityServer 7.x** — full OAuth2/OIDC (commercial license for production)
- **Microsoft.Identity.Web** — Azure AD / Entra ID integration, managed identities
- **Authorization policies** — `[Authorize(Policy = "Admin")]`, role-based or claim-based

## Testing
- **xUnit** (v3.2.2) — industry standard, parallel execution by default
- **Testcontainers** (v4.13.0) — real PostgreSQL/SQL Server/Redis in integration tests
- **WireMock.Net** — mock external HTTP dependencies
- **Moq** or **NSubstitute** — mocking (Moq more popular, NSubstitute cleaner syntax)
- **FluentAssertions** or **Shouldly** — readable assertions

## Observability
- **OpenTelemetry .NET** (v1.17.0) — traces, metrics, logs to Jaeger/Zipkin/Prometheus
  - Auto-instrumentation: ASP.NET Core, HttpClient, EF Core, SQL Client
- **Serilog** — structured logging with sinks (Seq, Elasticsearch, Application Insights)
- **Health checks** — `Microsoft.Extensions.Diagnostics.HealthChecks`
  - Endpoints: `/health`, `/health/ready`, `/health/live`
  - Check DB, Redis, external APIs, disk space

## Resilience
- **Polly** (v8.7.0) — circuit breaker, retry with exponential backoff, timeout, bulkhead isolation
- **HttpClientFactory** — prevents socket exhaustion, automatic DNS refresh, connection pooling
- **Combined pattern**:
  ```csharp
  services.AddHttpClient<PaymentClient>()
      .AddPolicyHandler(Policy.WrapAsync(retry, circuitBreaker));
  ```

## Caching
- **IMemoryCache** — in-process, single-instance deployments
- **IDistributedCache** — Redis (StackExchange.Redis) for multi-instance
- **HybridCache** (.NET 9) — built-in stampede protection for Minimal APIs
- **Response caching** — `[ResponseCache]` attribute, CDN for static assets

## API Versioning
- **Asp.Versioning** (v10.0.1) — URL segment (`/api/v1/users`), query string, header, or media type
- Automatic OpenAPI docs per version, deprecation policies

## Background Jobs
- **Hangfire** (v1.8.24) — persistent storage (SQL Server/PostgreSQL/Redis), dashboard, distributed processing
  - Fire-and-forget, delayed, recurring (cron), continuation jobs
- **Quartz.NET** — advanced scheduling, complex cron expressions
- **MediatR** — in-process mediator for CQRS (not a job scheduler — use with Hangfire)

## API Documentation
- **Built-in OpenAPI** (.NET 9+, recommended):
  - `AddOpenApi()` + `MapOpenApi()`
  - Build-time generation (no runtime dependency), AOT-compatible
- **Swashbuckle** — legacy, still valid for .NET 8 and earlier
- **Scalar** — modern Swagger UI alternative

## Real-time & gRPC
- **SignalR** — WebSockets with automatic transport fallback (SSE → long polling)
  - Hubs, group messaging, Redis backplane for multi-server
- **gRPC** — `Grpc.AspNetCore` (server), `Grpc.Net.Client` (client)
  - Code generation from `.proto` files, HTTP/2 multiplexing, AOT-compatible

## Deployment & Containerization
- **Docker multi-stage builds**:
  ```dockerfile
  FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
  RUN dotnet publish -c Release -o /app
  
  FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine
  COPY --from=build /app .
  ENTRYPOINT ["dotnet", "MyApi.dll"]
  ```
- **Alpine images** — ~50MB runtime, minimal attack surface
- **Native AOT** — sub-second startup, dramatically smaller memory, ideal for serverless/containers
  - Supported: x64/Arm64 Windows/Linux, macOS, iOS/tvOS (no longer experimental in .NET 9+)
- **CI/CD** — GitHub Actions (`setup-dotnet`) or Azure DevOps (`DotNetCoreCLI@2`)

## Summary Table

| Concern | Tool | Version |
|---|---|---|
| Framework | ASP.NET Core | 10 (LTS) |
| Language | C# | 14 |
| ORM | Entity Framework Core | 10 |
| Validation | FluentValidation | Latest |
| Auth | JWT Bearer / Duende IdentityServer | 7.x |
| Testing | xUnit | 3.2.2 |
| Logging | Serilog | Latest |
| Observability | OpenTelemetry .NET | 1.17.0 |
| Resilience | Polly | 8.7.0 |
| Caching | StackExchange.Redis | Latest |
| API Versioning | Asp.Versioning | 10.0.1 |
| Background Jobs | Hangfire | 1.8.24 |
| API Docs | Built-in OpenAPI | .NET 9+ |
| Real-time | SignalR | Built-in |
| gRPC | Grpc.AspNetCore | Latest |
| Containerization | Docker + Alpine | — |
| CI/CD | GitHub Actions / Azure DevOps | — |

---

**Status**: Research complete. Ready for checklist creation when user requests.
