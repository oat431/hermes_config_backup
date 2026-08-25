---
name: web-research
description: "Fetch docs via curl when browser tools unavailable."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Documentation, Web, Technical, APIs, Frameworks]
    category: research
    related_skills: [grounded-citations, arxiv, blogwatcher]
---

# Web Research

Fetch and synthesize technical documentation from official sources when browser automation tools fail or are unavailable. Covers API documentation, framework guides, release notes, and technical references from sites like Microsoft Learn, GitHub, Stack Overflow, and vendor documentation.

## When to Use

- Researching APIs, frameworks, or libraries (e.g., ".NET 9 features", "React hooks", "gRPC in Go")
- Fetching release notes, migration guides, or breaking changes
- Gathering technical specifications or deployment patterns
- Synthesizing information from multiple official documentation sources
- When `browser_navigate` fails due to missing Chrome/Puppeteer/Playwright

Skip for: casual web searches (use `web_search`), academic papers (use `arxiv`), blog monitoring (use `blogwatcher`), or when you need interactive browser automation (use `computer_use`).

## Prerequisites

- `curl` (available on all platforms)
- Python 3 with `re` module (stdlib)
- `terminal` tool for shell commands

## Browser Fallback Pattern

When `browser_navigate` fails with "Chrome not found" or similar errors, fall back to curl + regex-based HTML text extraction:

```python
from hermes_tools import terminal
import re

def extract_text(html):
    """Strip HTML tags, remove script/style blocks, normalize whitespace."""
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'\s+', ' ', html)
    return html.strip()

# Fetch documentation
r = terminal("curl -sL '<url>' -H 'User-Agent: Mozilla/5.0' 2>/dev/null")
text = extract_text(r['output'])
print(text[:5000])  # Adjust slice based on content length
```

**Why this works:**
- Many documentation sites (Microsoft Learn, GitHub, etc.) are server-rendered, not SPA/JavaScript-heavy
- curl with a User-Agent header bypasses most bot detection
- Regex extraction is faster than full HTML parsing for simple text extraction
- Works in headless environments where Chrome isn't installed

**Limitations:**
- Won't work for JavaScript-rendered content (React/Vue/Angular apps)
- May miss content loaded via AJAX/fetch calls
- Complex table layouts or nested structures may lose formatting

## Procedure

① **Identify official sources first.** For framework/library research, start with:
- Official documentation (learn.microsoft.com, docs.python.org, etc.)
- GitHub repositories (README, docs/, release notes)
- RFC/specification documents
- Vendor blogs or engineering posts

② **Batch fetch in parallel.** Use `execute_code` to fetch multiple URLs concurrently:

```python
from hermes_tools import terminal
import re

def extract_text(html):
    # ... (function from above)

urls = [
    ('https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-9/overview', 'dotnet9'),
    ('https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-9.0', 'aspnet9'),
]

for url, key in urls:
    r = terminal(f"curl -sL '{url}' -H 'User-Agent: Mozilla/5.0' 2>/dev/null")
    text = extract_text(r['output'])
    print(f"=== {key.upper()} ===")
    print(text[:4000])
    print("\n---\n")
```

③ **Extract and synthesize.** Read the fetched text, identify key sections (features, breaking changes, code examples), and synthesize into a structured summary. Focus on:
- New features or capabilities
- Breaking changes or deprecations
- Performance improvements
- Code examples or patterns
- Migration paths

④ **Cite sources.** If using the `grounded-citations` skill, register URLs and cite inline. Otherwise, append a `Sources:` section with URLs.

⑤ **Structure the output.** For comprehensive research, organize by topic:

```markdown
## Topic 1: Feature Name
- Key points
- Code examples
- Breaking changes

## Topic 2: Deployment Patterns
- Docker multi-stage builds
- CI/CD workflows
```

## Pitfalls

- **JavaScript-rendered sites.** If curl returns empty or minimal content, the site likely requires JavaScript execution. Fall back to `browser_navigate` (if available) or find alternative documentation sources (GitHub READMEs, cached versions, etc.).
- **Rate limiting.** Some sites throttle curl requests. Add delays between fetches or use different User-Agent strings if you hit 429 errors.
- **HTML entity encoding.** Extracted text may contain `&amp;`, `&lt;`, `&gt;`. Use `html.unescape()` if you need clean text:
  ```python
  import html
  text = html.unescape(extract_text(r['output']))
  ```
- **Large pages.** Some documentation pages are 50k+ characters. Slice strategically (`text[:5000]`) or search for specific sections using regex.
- **Outdated documentation.** Official docs may lag behind actual releases. Cross-reference with GitHub release notes or changelog files for the most current information.
- **Missing context.** Extracted text loses visual structure (tables, code blocks, diagrams). Reconstruct formatting manually or note when structure is unclear.

## Verification

After synthesizing, verify by:
1. Cross-checking key claims against 2+ sources when possible
2. Checking GitHub repository for recent commits/releases
3. Looking for "last updated" dates in documentation metadata
4. Testing code examples if feasible (e.g., `dotnet new webapi --help` to verify CLI flags)

## Example: .NET Feature Research

```python
from hermes_tools import terminal
import re

def extract_text(html):
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'\s+', ' ', html)
    return html.strip()

# Fetch .NET 9 release notes
r = terminal("curl -sL 'https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-9/overview' -H 'User-Agent: Mozilla/5.0' 2>/dev/null")
text = extract_text(r['output'])

# Search for specific sections
import re
performance_section = re.search(r'Performance.*?(?=##|$)', text, re.IGNORECASE | re.DOTALL)
if performance_section:
    print(performance_section.group(0)[:2000])
```
