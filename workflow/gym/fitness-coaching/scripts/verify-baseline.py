"""Verify a baseline-assessment.md note for integrity.

Usage: python verify-baseline.py <vault_path>
Example: python verify-baseline.py "F:\\projects\\orlita_md"

Checks:
- File exists and is non-empty
- Valid YAML frontmatter
- All expected data points present
- BMI and BMR calculations match the stored values
"""
import sys
import re
from pathlib import Path


def extract_number(text: str, label: str) -> float | None:
    """Extract a numeric value following a label in the note."""
    m = re.search(rf"{re.escape(label)}.*?([\d.]+)", text)
    return float(m.group(1)) if m else None


def main(vault: str) -> int:
    path = Path(vault) / "fitness" / "baseline-assessment.md"
    if not path.exists():
        print(f"FAIL: {path} not found")
        return 1

    content = path.read_text()
    if len(content) < 100:
        print(f"FAIL: file too small ({len(content)} bytes)")
        return 1

    # Frontmatter check
    if not content.startswith("---"):
        print("FAIL: missing YAML frontmatter")
        return 1
    parts = content.split("---", 2)
    if len(parts) < 3:
        print("FAIL: malformed frontmatter")
        return 1

    # Extract values
    weight = extract_number(content, "Weight")
    height = extract_number(content, "Height")
    age = extract_number(content, "Age")
    stored_bmi = extract_number(content, "BMI")
    stored_bmr = extract_number(content, "BMR")

    failures = 0

    # BMI check
    if weight and height:
        expected_bmi = weight / ((height / 100) ** 2)
        if stored_bmi and abs(expected_bmi - stored_bmi) > 0.1:
            print(f"FAIL: BMI mismatch — stored {stored_bmi}, expected {expected_bmi:.1f}")
            failures += 1
        elif stored_bmi:
            print(f"  BMI: {expected_bmi:.1f} ✓")

    # BMR check (Mifflin-St Jeor, male)
    if weight and height and age:
        expected_bmr = 10 * weight + 6.25 * height - 5 * age + 5
        if stored_bmr:
            if abs(expected_bmr - stored_bmr) > 1:
                print(f"FAIL: BMR mismatch — stored {stored_bmr}, expected {expected_bmr:.0f}")
                failures += 1
            else:
                print(f"  BMR: {expected_bmr:.0f} kcal ✓")

    # Required data points
    required = [
        "Weight", "Height", "Age", "BMI", "BMR", "TDEE",
        "Calories", "Protein", "Training age", "Equipment",
        "Schedule", "Sleep", "Goals"
    ]
    for label in required:
        if label.lower() not in content.lower():
            print(f"FAIL: missing section '{label}'")
            failures += 1

    if failures == 0:
        print(f"✅ All checks passed — BMI {expected_bmi:.1f}, BMR {expected_bmr:.0f} kcal")
        return 0
    else:
        print(f"❌ {failures} failure(s)")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify-baseline.py <vault_path>")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
