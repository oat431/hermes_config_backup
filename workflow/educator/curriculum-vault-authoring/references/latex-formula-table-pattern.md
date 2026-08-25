# LaTeX Formula-in-Table Pattern for Obsidian

## The Pattern

Use `$$...$$` (display math) inside markdown table cells for formulas. This is the user's established and preferred format for Key Formulas sections across all BOK sub-overviews.

## Correct Syntax

```markdown
| Concept | Formula |
|---|---|
| **Mass-energy** | $$E = mc^2$$ |
| **Photon energy** | $$E = hf = \frac{hc}{\lambda}$$ |
| **Time dilation** | $$\Delta t = \frac{\Delta t_0}{\sqrt{1 - v^2/c^2}}$$ |
| **Quadratic formula** | $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$ |
```

## Key Rules

1. **Single backslashes ONLY** — `\frac`, `\sqrt`, `\pm`, `\propto`, `\Rightarrow`, `\text`, `\rho`, `\lambda`, `\Delta`
2. **`$$...$$` wrapping** — One formula per cell, display math mode
3. **Simple table structure** — Two columns (Concept | Formula), no fancy alignment
4. **When LaTeX breaks, go plain** — `a/b` beats broken `\frac{a}{b}`
5. **Chemical formulas** — Use `$$\ce{CH4}$$` (requires mhchem extension, standard in Obsidian)

## Common Formula Types Encountered

### Physics
- Kinematics: `$$v = u + at$$`, `$$s = ut + \tfrac{1}{2}at^2$$`
- Newton: `$$F = ma$$`
- Energy: `$$KE = \tfrac{1}{2}mv^2$$`
- Waves: `$$v = f\lambda$$`
- Thermo: `$$PV = nRT$$`
- E&M: `$$V = IR$$`, `$$F = qvB \sin\theta$$`
- Modern: `$$E = mc^2$$`, `$$\lambda = \frac{h}{mv}$$`

### Chemistry
- Mole: `$$n = \frac{m}{M}$$`
- Ideal gas: `$$PV = nRT$$`
- pH: `$$\text{pH} = -\log[\text{H}^+]$$`
- Organic: `$$\ce{CH3COOH}$$`, `$$\ce{-OH}$$`

### Math
- Pythagoras: `$$a^2 + b^2 = c^2$$`
- Slope: `$$m = \frac{y_2 - y_1}{x_2 - x_1}$$`
- Area: `$$A = \pi r^2$$`
- Quadratic: `$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$`

## Pitfalls

- **Double backslashes break rendering** — `\\frac` renders as literal text "f ac a b"
- **Greek letter line-wrapping** — When using `patch` tool, Greek letters (`\rho`, `\lambda`) can get split across lines. Keep formula lines short (< 60 chars) in patch strings
- **`\left`, `\right`, `\middle`** — Fragile in Obsidian MathJax. Use plain brackets: `(1 + x)` instead of `\left(1 + x\right)`
- **`\ce{}` for chemicals** — Requires MathJax mhchem extension. Test that it renders. If not, fall back to plain text: `CH₃COOH` instead of `$$\ce{CH3COOH}$$`
