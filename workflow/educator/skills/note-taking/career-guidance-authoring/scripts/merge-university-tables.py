"""
Merge multiple university tables with different column structures into one unified table.

Handles these column patterns:
- 5 columns: University | Faculty | Est. | Location | Notable Features
- 4 columns: University | Faculty | Location | Notable Features
- 3 columns: University | Faculty/Location | Notable Features
- 2 columns: University | Location

Output: 4 columns: University | Faculty | Location | Notable Features

Usage:
  python3 merge-university-tables.py <career_folder>
  python3 merge-university-tables.py F:/obsidian_note/general-knowledge/career/nurse
"""

import os
import sys
import re

def parse_university_row(line):
    """Parse a single table row into a university dict."""
    cells = [c.strip() for c in line.split('|')[1:-1]]
    
    uni = {'name': '', 'faculty': '', 'location': '', 'features': ''}
    
    # Smart column detection: check if any cell is a year (4 digits)
    year_idx = None
    for idx, cell in enumerate(cells):
        if cell.isdigit() and len(cell) == 4:
            year_idx = idx
            break
    
    if year_idx is not None:
        # 5-column format with Est.
        uni['name'] = cells[0]
        uni['faculty'] = cells[1]
        uni['location'] = cells[year_idx + 1] if year_idx + 1 < len(cells) else ''
        uni['features'] = cells[year_idx + 2] if year_idx + 2 < len(cells) else ''
    elif len(cells) >= 4:
        # 4 columns: University, Faculty, Location, Notable Features
        uni['name'] = cells[0]
        uni['faculty'] = cells[1]
        uni['location'] = cells[2]
        uni['features'] = cells[3]
    elif len(cells) == 3:
        # 3 columns: detect if second is location or faculty
        uni['name'] = cells[0]
        location_keywords = ['Bangkok', 'Chiang', 'Khon', 'Hat', 'Pathum', 'Nakhon',
                           'Phitsanulok', 'Ubon', 'Surin', 'Maha', 'Songkhla',
                           'Chonburi', 'Lampang', 'Rayong', 'Distance', 'Nonthaburi']
        if any(loc in cells[1] for loc in location_keywords):
            uni['location'] = cells[1]
            uni['features'] = cells[2]
        else:
            uni['faculty'] = cells[1]
            uni['location'] = cells[2]
    elif len(cells) == 2:
        uni['name'] = cells[0]
        uni['location'] = cells[1]
    
    return uni if uni['name'] else None


def merge_tables(section_lines):
    """Parse all university tables in a section and return merged list."""
    universities = []
    
    for line in section_lines:
        line = line.strip()
        
        # Skip non-data rows
        if not line.startswith('|') or '---' in line:
            continue
        if 'University' in line and ('Faculty' in line or 'Location' in line):
            continue
        if line == '#':
            continue
        
        # Parse university rows
        if line.startswith('|') and '**' in line:
            uni = parse_university_row(line)
            if uni:
                universities.append(uni)
    
    # Remove duplicates (keep first occurrence)
    seen = set()
    unique = []
    for uni in universities:
        name = uni['name'].replace('**', '').strip()
        if name not in seen:
            seen.add(name)
            unique.append(uni)
    
    return unique


def build_table(display_name, universities):
    """Build a markdown table from university list."""
    result = f"### {display_name} Programs in Thailand\n\n"
    result += "| University | Faculty | Location | Notable Features |\n"
    result += "|---|---|---|---|\n"
    
    for uni in universities:
        name = uni['name']
        faculty = uni['faculty'] if uni['faculty'] else '-'
        location = uni['location'] if uni['location'] else '-'
        features = uni['features'] if uni['features'] else '-'
        result += f"| {name} | {faculty} | {location} | {features} |\n"
    
    return result


def process_career(career_path, display_name):
    """Process a single career's 00_University_Guide file."""
    file_path = os.path.join(career_path, '00_University_Guide_and_Career_Paths.md')
    
    if not os.path.exists(file_path):
        print(f"SKIP: {file_path} not found")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Find the "Programs in Thailand" section
    section_start = None
    section_end = None
    
    for i, line in enumerate(lines):
        if 'Programs in Thailand' in line:
            section_start = i
        elif section_start is not None and line.strip().startswith('###') and 'Programs' not in line:
            section_end = i
            break
    
    if section_start is None:
        print(f"SKIP: {career_path} - section not found")
        return
    
    # Extract and merge
    section_lines = lines[section_start:section_end]
    universities = merge_tables(section_lines)
    
    # Build new table
    new_section = build_table(display_name, universities)
    
    # Reconstruct file
    new_content = '\n'.join(lines[:section_start]) + '\n' + new_section + '\n' + '\n'.join(lines[section_end:])
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"DONE: {display_name} - merged {len(universities)} universities")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 merge-university-tables.py <career_folder>")
        print("Example: python3 merge-university-tables.py F:/obsidian_note/general-knowledge/career/nurse")
        sys.exit(1)
    
    career_path = sys.argv[1]
    career_name = os.path.basename(career_path)
    
    display_names = {
        'nurse': 'Nursing',
        'psychologist': 'Psychology',
        'teacher': 'Education',
        'engineer': 'Engineering',
        'lawyer': 'Law',
        'agriculture': 'Agriculture',
        'accountant': 'Accounting'
    }
    
    display_name = display_names.get(career_name, career_name.title())
    process_career(career_path, display_name)
