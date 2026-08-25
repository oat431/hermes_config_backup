# LaTeX Formatting for Obsidian Math Notes

> **Last updated:** 2026-07-25
> **Critical rule:** Use SINGLE backslashes for all LaTeX commands in Obsidian `$$...$$` blocks.

## The Golden Rule

**`write_file` writes content literally.** Single backslashes in source → single backslashes in file → correct rendering. Double backslashes → broken rendering.

| Source (what you write) | File contains | Obsidian renders |
|---|---|---|
| `\frac{a}{b}` | `\frac{a}{b}` | $$\frac{a}{b}$$ ✅ |
| `\\frac{a}{b}` | `\\frac{a}{b}` | "f ac a b" ❌ |
| `\sqrt{x}` | `\sqrt{x}` | $$\sqrt{x}$$ ✅ |
| `\\sqrt{x}` | `\\sqrt{x}` | "s qrt{x}" ❌ |

## Correct Syntax Cheatsheet

### Inline vs Display

| Type | Syntax | When |
|---|---|---|
| Display math | `$$...$$` | Standalone equations, table cells with formulas |
| Inline math | `$...$` | Within sentences (use sparingly) |

### Common Commands

| Command | Renders As |
|---|---|
| `\frac{a}{b}` | $$\frac{a}{b}$$ |
| `\sqrt{x}` | $$\sqrt{x}$$ |
| `\text{word}` | $$\text{word}$$ |
| `\times` | $$\times$$ |
| `\div` | $$\div$$ |
| `\cdot` | $$\cdot$$ |
| `\pm` | $$\pm$$ |
| `\propto` | $$\propto$$ |
| `\Rightarrow` | $$\Rightarrow$$ |
| `\boxed{x}` | $$\boxed{x}$$ |
| `\mathbf{x}` | $$\mathbf{x}$$ |
| `\tfrac{1}{2}` | $$\tfrac{1}{2}$$ (small fraction) |
| `\overline{x}` | $$\overline{x}$$ |

### Subscripts and Superscripts

| Syntax | Renders |
|---|---|
| `x^2` | $$x^2$$ |
| `x^{10}` | $$x^{10}$$ (multi-char superscript) |
| `x_0` | $$x_0$$ |
| `x_{\text{max}}` | $$x_{\text{max}}$$ (text subscript) |
| `T_{1/2}` | $$T_{1/2}$$ (fraction subscript) |

### Greek Letters

| Command | Renders |
|---|---|
| `\alpha, \beta, \gamma` | $$\alpha, \beta, \gamma$$ |
| `\Delta, \Sigma, \Pi` | $$\Delta, \Sigma, \Pi$$ |
| `\lambda, \mu, \rho, \sigma` | $$\lambda, \mu, \rho, \sigma$$ |
| `\theta, \phi, \omega` | $$\theta, \phi, \omega$$ |
| `\varepsilon, \Phi, \Omega` | $$\varepsilon, \Phi, \Omega$$ |

### Chemical Formulas (mhchem)

Obsidian's MathJax includes the mhchem extension. Use `$$\ce{...}$$` for chemical notation:

| Syntax | Renders |
|---|---|
| `$$\ce{H2O}$$` | Water |
| `$$\ce{CO2}$$` | Carbon dioxide |
| `$$\ce{CH4}$$` | Methane |
| `$$\ce{NaCl}$$` | Sodium chloride |
| `$$\ce{-OH}$$` | Hydroxyl group |
| `$$\ce{C=C}$$` | Double bond |
| `$$\ce{CH3COOH}$$` | Acetic acid |
| `$$\ce{SO4^{2-}}$$` | Sulfate ion |

**Pitfall:** `\ce{}` only works inside `$$...$$` blocks, not in inline `$...$`.

### Environments

| Environment | When |
|---|---|
| `\begin{aligned}...\end{aligned}` | Multi-line equations with alignment |
| `\begin{cases}...\end{cases}` | Piecewise definitions |
| `\begin{array}{r}...\end{array}` | Aligned columns (fragile in Obsidian) |

**Critical:** `\\` (double backslash) is ONLY correct as a **line break** inside these environments:
```latex
$$\begin{aligned}
3 + 4 &= 7 \\
4 + 3 &= 7
\end{aligned}$$
```

## Batch Fix Command

When files have `\\frac`, `\\sqrt`, etc. (double backslash), fix with:

```bash
cd "F:/obsidian_note/general-knowledge/Mathematics"
for f in *.md; do
  sed -i 's/\\\\frac/\\frac/g; s/\\\\times/\\times/g; s/\\\\div/\\div/g; 
           s/\\\\text/\\text/g; s/\\\\sqrt/\\sqrt/g; s/\\\\boxed/\\boxed/g;
           s/\\\\mathbf/\\mathbf/g; s/\\\\begin/\\begin/g; s/\\\\end/\\end/g' "$f"
done
```

**Pitfall:** Run sed **ONCE**. Iterative sed passes corrupt already-correct content. After running, verify with `grep -c '\\\\\\\\' *.md | grep -v ':0$'` and fix remaining issues with `patch`.

## Fallback to Plain Text

When LaTeX is unreliable, prefer readability:

| LaTeX (fragile) | Plain text (safe) |
|---|---|
| `\frac{a}{b}` | `a/b` |
| `\frac{x_1+x_2}{2}` | `(x₁+x₂)/2` |
| `\sqrt{(x₂-x₁)²+(y₂-y₁)²}` | `√[(x₂−x₁)² + (y₂−y₁)²]` |
| `\frac{-b \pm \sqrt{b^2-4ac}}{2a}` | `x = (−b ± √(b²−4ac))/2a` |

## Testing Your LaTeX

To verify a formula renders correctly:
1. Open the .md file in Obsidian
2. Look for the rendered equation
3. If you see raw LaTeX code instead of a rendered equation, there's a backslash issue

## Common Pitfalls

- **`\\frac` → renders as "f ac a b"** — the double backslash escapes into nothing, leaving "frac" as literal text
- **`\\text` inside `$$...$$`** — same issue, renders as literal "text{word}"
- **`\left`, `\right`, `\middle`** — fragile in Obsidian's MathJax, prefer plain brackets
- **Array environments** — `\begin{array}{r}` often breaks; use code blocks for column alignment instead
- **`\\% ` showing as `\%`** — the sed fix might not catch all; if you see literal backslash-percent, run a targeted fix
