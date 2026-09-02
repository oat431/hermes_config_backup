# IPST Bilingual Conversion Pattern Examples

Concrete before/after examples captured during the Chemistry 14-20 conversion batch (July 2026). These are the patterns that kept recurring — when in doubt, match the converted output here.

## Pattern 1: Section headings with Thai topic-name

Convert Thai heading + English-title to English-title first, Thai in parens:

```
### 3.1 ความพิเศษของคาร์บอน
→ ### 3.1 The Special Properties of Carbon

### 3.2 ประเภทของไฮโดรคาร์บอน
→ ### 3.2 Classes of Hydrocarbons

### 3.5 ภาวะไอโซเมอร์ (Isomerism)
→ ### 3.5 Isomerism (ภาวะไอโซเมอร์)
```

When the source heading already has English in parens, swap the order: English-first, Thai-in-parens. This matches the bilingual aesthetic.

## Pattern 2: Sub-heading with alphanumber + Thai topic + English in parens

Convert mixed-numeric headings to clean English-first:

```
#### (a) ไขมันและน้ำมัน (Fats and Oils)
→ #### (a) Fats and Oils (ไขมันและน้ำมัน)

#### (2) คาร์โบไฮเดรต (Carbohydrates) — see 3.4
→ #### (2) Carbohydrates (คาร์โบไฮเดรต)
```

## Pattern 3: Bullet with bolded Thai-English mixed terminology

The bolded term stays bolded; the colon after stays; the prose after translates:

```
- **Tetravalent (เตตระวาเลนต์):** C มี 4 valence electrons จึงสร้างพันธะได้ 4 พันธะ
→ - **Tetravalent (เตตระวาเลนต์):** C has 4 valence electrons, so it forms 4 bonds.
```

Thai in parens after the bolded English term is preserved verbatim — it's the bilingual anchor.

## Pattern 4: Numbered list inside a section

```
1. **หาสายโซ่หลัก (Longest carbon chain)** ที่ยาวที่สุด
2. **ระบุหมู่แทนที่ (Substituents)** และตำแหน่ง
3. **นับตำแหน่ง** ให้ได้ตัวเลขน้อยที่สุด
→
1. **Find the longest carbon chain (สายโซ่หลัก)** that contains the most carbons.
2. **Identify the substituents (หมู่แทนที่)** and their positions.
3. **Number the chain** to give the lowest possible locants.
```

## Pattern 5: Table row with Thai prose cells

The header row stays identical (`| Thai | English | Symbol/Notes |`). Cell-by-cell Thai prose translates to English; chemical names stay. Cells with chemical formulas or Sanskrit-derived English-only names (methane, ethane) stay.

## Pattern 6: Equation/chemical block inside prose

```
**สูตรทั่วไป:** $\ce{C_nH_{2n+1}OH}$ หรือ $\ce{R-OH}$
→ **General formula:** $\ce{C_nH_{2n+1}OH}$ or $\ce{R-OH}$.
```

LaTeX is verbatim; only the Thai prose around it translates.

## Pattern 7: Trailing parenthetical "(ต่อในบทถัดไป)" boilerplate

```
|| **Semester 2** | (ต่อในบทถัดไป) | — |
→ || **Semester 2** | (continued in the next note) | — |
```

## Pattern 8: Reaction table column with Thai sample labels

```
|| ชื่อ | องค์ประกอบ | แหล่ง |
→ || Name | Components | Source |
```

Table headers ALWAYS translate. Body cells translate when prose, keep when chemical/formula.

## Pattern 9: "Solution:" with Thai

The label `**สมการ:**` / `**สูตร:**` / `**Solution:**` translates when the source label is Thai:

```
**สมการ:**
$\ce{C3H8 + 5O2 -> 3CO2 + 4H2O}$
→ **Equation:**
$\ce{C3H8 + 5O2 -> 3CO2 + 4H2O}$
```

## Pattern 10: Comparison table (SN1/SN2/E1/E2)

```
|| กลไก | Substrate | Nucleophile/Base | Solvent | ขั้น |
|| SN1 | 3° | weak | polar protic | 2 |
→
|| Mechanism | Substrate | Nucleophile/Base | Solvent | Steps |
|| SN1 | 3° | weak | polar protic | 2 |
```

Header row translates. The SN1/SN2/E1/E2 labels are universal nomenclature — leave alone. Numeric step count left alone.

## Pattern 11: Cross-link descriptions

```
- [[14_Organic_Fundamentals]] — โครงสร้างพื้นฐาน
- [[15_Organic_Reactions]] — ปฏิกิริยาเคมีอินทรีย์ (ถัดไป)
→
- [[14_Organic_Fundamentals]] — Basic structures
- [[15_Organic_Reactions]] — Organic reactions (next)
```

Wikilink path is preserved verbatim. Description translates; drop the "(ถัดไป)" boilerplate by integrating "— next" into the description (Pattern 7 above).

## Pattern 12: Body prose with multi-clause Thai

Long Thai sentences with multiple clauses translate clause-by-clause, NOT word-by-word. Example:

```
**ปฏิกิริยาเคมีอินทรีย์แบ่งออกเป็นหลายประเภทตามกลไกและการเปลี่ยนแปลงโครงสร้าง ได้แก่ ปฏิกิริยาการแทนที่ การเติม การกำจัด การควบแน่น การไฮโดรลิซิส การเผาไหม้ และปฏิกิริยารีดอกซ์**
→ Organic reactions are classified into several types according to their mechanism and the structural change that occurs: substitution, addition, elimination, condensation, hydrolysis, combustion, and redox.
```

The "ได้แก่" (namely) becomes a colon. The list items translate. Don't break into bullet form — match source structure.

## Pattern 13: Thai-anchored identifier (keep verbatim)

These identifiers are curriculum codes, NOT Thai prose. Always leave intact:

- `ม.6 (ว313)`, `ม.5 (ว312)`, `ม.4 (ว311)`
- `B.E. 2551 (2008, revised 2560/2017)`
- `IPST (สสวท.)`
- Course codes `ว302`, `ว311`, `ว312`, `ว313`

Within prose, course code references also stay:

```
ในวิชา ว313 Semester 1 ...
→ In ว313 Semester 1 ...
```

## Pattern 14: Thai commentary inside parentheses that explains a Thai concept

```
**หลักการ:** ความร้อน → e⁻ กระโดดขึ้นระดับพลังงานสูง → ตกกลับ → ปล่อยพลังงานเป็นแสงสีจำเพาะ
→ **Principle:** heat excites electrons to higher energy levels → they fall back → release the energy as light of a characteristic color.
```

Arrows `→` stay. Process prose translates. No conversion to sentence form needed.

## Pattern 15: "≈" / "$\approx$" approximation symbols

Always preserve. Same for `\Delta`, `\ce{}`, `\leftrightarrow`, `\rightarrow`, subscripts, superscripts.

## Line-count verification rule of thumb

| Source line count | Converted line count should be |
|---|---|
| < 100 | within ±10 |
| 100-300 | within ±20 (the conversion can add a line or two for clarity) |
| > 300 | within ±30 |

Converted files for the Chemistry 14-20 batch (target: 7 files, average source ~200 lines) all came out within ±5 lines. If yours is 30% shorter or longer, you've introduced a regression.
