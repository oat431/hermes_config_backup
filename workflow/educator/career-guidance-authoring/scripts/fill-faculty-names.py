"""
Fill missing faculty names in university tables.

When university tables have "-" for faculty, this script fills them with
the correct Thai faculty names based on the profession.

Usage:
  python3 fill-faculty-names.py <career_folder>
  python3 fill-faculty-names.py F:/obsidian_note/general-knowledge/career/nurse
  
  # Or process all careers:
  python3 fill-faculty-names.py --all F:/obsidian_note/general-knowledge/career
"""

import os
import sys
import re

# Faculty mappings by profession and university
FACULTY_MAP = {
    'nurse': {
        'Walailak University': 'คณะพยาบาลศาสตร์',
        'Mahasarakham University': 'คณะพยาบาลศาสตร์',
        'Ubon Ratchathani University': 'คณะพยาบาลศาสตร์',
        'Suranaree University of Technology': 'สำนักวิชาพยาบาลศาสตร์',
        'Mae Fah Luang University': 'คณะพยาบาลศาสตร์',
        'Silpakorn University': 'คณะพยาบาลศาสตร์',
    },
    'psychologist': {
        'Sukhothai Thammathirat Open University': 'สาขาวิชาจิตวิทยา',
    },
    'teacher': {
        'มหาวิทยาลัยราชภัฏสวนสุนันทา': 'คณะครุศาสตร์',
        'มหาวิทยาลัยราชภัฏจันทรเกษม': 'คณะครุศาสตร์',
        'มหาวิทยาลัยราชภัฏเชียงใหม่': 'คณะครุศาสตร์',
        'มหาวิทยาลัยราชภัฏนครราชสีมา': 'คณะครุศาสตร์',
        'มหาวิทยาลัยราชภัฏสงขลา': 'คณะครุศาสตร์',
        'มหาวิทยาลัยราชภัฏพระนคร': 'คณะครุศาสตร์',
    },
    'engineer': {
        'Naresuan University': 'คณะวิศวกรรมศาสตร์',
        'Mahasarakham University': 'คณะวิศวกรรมศาสตร์',
        'Ubon Ratchathani University': 'คณะวิศวกรรมศาสตร์',
        'Walailak University': 'สำนักวิชาวิศวกรรมศาสตร์',
        'Silpakorn University': 'คณะวิศวกรรมศาสตร์และเทคโนโลยีอุตสาหกรรม',
        'Rajamangala Universities of Technology (RMUT)': 'คณะวิศวกรรมศาสตร์',
        'Sripatum University': 'คณะวิศวกรรมศาสตร์',
        'Assumption University (ABAC)': 'Faculty of Engineering',
    },
    'lawyer': {
        'Khon Kaen University': 'คณะนิติศาสตร์',
        'Burapha University': 'คณะนิติศาสตร์',
        'Naresuan University': 'คณะนิติศาสตร์',
        'Ubon Ratchathani University': 'คณะนิติศาสตร์',
        'Mahasarakham University': 'คณะนิติศาสตร์',
        'Walailak University': 'คณะนิติศาสตร์',
        'Sripatum University': 'คณะนิติศาสตร์',
        'Bangkok University': 'คณะนิติศาสตร์',
    },
    'agriculture': {
        'Naresuan University': 'คณะเกษตรศาสตร์',
        'Ubon Ratchathani University': 'คณะเกษตรศาสตร์',
        'Walailak University': 'สำนักวิชาเทคโนโลยีการเกษตร',
        'Rajamangala Universities of Technology (RMUT)': 'คณะเกษตรศาสตร์',
    },
    'accountant': {
        'Burapha University': 'คณะบริหารธุรกิจ (สาขาบัญชี)',
        'Ubon Ratchathani University': 'คณะบริหารธุรกิจ (สาขาบัญชี)',
        'Naresuan University': 'คณะบริหารธุรกิจ (สาขาบัญชี)',
        'Prince of Songkla University': 'คณะพาณิชยศาสตร์และการจัดการ',
        'Sripatum University': 'คณะบัญชี',
        'Bangkok University': 'คณะบัญชี',
        'Rangsit University': 'คณะบริหารธุรกิจ (สาขาบัญชี)',
        'Mahasarakham University': 'คณะบัญชีและการจัดการ',
    },
}

# Common faculty patterns for universities not in the explicit map
GENERIC_FACULTY_PATTERNS = {
    'nurse': 'คณะพยาบาลศาสตร์',
    'psychologist': 'สาขาวิชาจิตวิทยา',
    'teacher': 'คณะครุศาสตร์',
    'engineer': 'คณะวิศวกรรมศาสตร์',
    'lawyer': 'คณะนิติศาสตร์',
    'agriculture': 'คณะเกษตรศาสตร์',
    'accountant': 'คณะบริหารธุรกิจ (สาขาบัญชี)',
}


def fill_faculty_in_file(file_path, career_name):
    """Fill missing faculty names in a university guide file."""
    if not os.path.exists(file_path):
        return 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    mappings = FACULTY_MAP.get(career_name, {})
    generic = GENERIC_FACULTY_PATTERNS.get(career_name, '')
    
    count = 0
    new_lines = []
    
    for line in lines:
        # Check if this is a university row with missing faculty
        if line.strip().startswith('|') and '**' in line:
            cells = [c.strip() for c in line.split('|')[1:-1]]
            
            if len(cells) >= 2 and cells[1] == '-':
                # Extract university name
                uni_name = cells[0].replace('**', '').strip()
                
                # Try explicit mapping first
                faculty = mappings.get(uni_name, '')
                
                # If not found, try generic pattern
                if not faculty and generic:
                    faculty = generic
                
                if faculty:
                    # Replace the "-" with faculty name
                    # Use regex to handle variable whitespace
                    pattern = r'(\| \*\*' + re.escape(uni_name) + r'\*\*\s+)\| -\s+\|'
                    replacement = f'| **{uni_name}** | {faculty} |'
                    new_line = re.sub(pattern, replacement, line)
                    if new_line != line:
                        line = new_line
                        count += 1
        
        new_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return count


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fill-faculty-names.py <career_folder>")
        print("       python3 fill-faculty-names.py --all <careers_base>")
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        # Process all careers
        base = sys.argv[2]
        total = 0
        for career in FACULTY_MAP.keys():
            file_path = os.path.join(base, career, '00_University_Guide_and_Career_Paths.md')
            filled = fill_faculty_in_file(file_path, career)
            if filled > 0:
                print(f"DONE: {career} - filled {filled} faculties")
                total += filled
        print(f"\nTotal: {total} faculties filled across all careers")
    else:
        # Process single career
        career_path = sys.argv[1]
        career_name = os.path.basename(career_path)
        file_path = os.path.join(career_path, '00_University_Guide_and_Career_Paths.md')
        filled = fill_faculty_in_file(file_path, career_name)
        print(f"DONE: {career_name} - filled {filled} faculties")


if __name__ == '__main__':
    main()
