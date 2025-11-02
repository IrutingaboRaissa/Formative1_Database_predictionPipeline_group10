import os
import glob

# Define emoji replacements
replacements = {
    '✓': '',
    '✅': '',
    '❌': '',
    '📊': '',
    '🎯': '',
    '😊': '',
    '💡': '',
    '🚀': '',
    '⭐': '',
    '✗': 'X',
    'print("=" * 100)': 'print("")',
    'print("=" * 80)': 'print("")',
    'print("-" * 100)': 'print("")',
    'print("-" * 80)': 'print("")',
}

def clean_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

# Find all Python files
python_files = glob.glob('**/*.py', recursive=True)

cleaned_count = 0
for filepath in python_files:
    if clean_file(filepath):
        cleaned_count += 1

print(f"\nTotal files cleaned: {cleaned_count}/{len(python_files)}")
