import os
import shutil
import pandas as pd
import re
import unicodedata
import json
import time

def is_emoji(char):
    cat = unicodedata.category(char)
    if cat in ('So', 'Sk'):
        return True
    code = ord(char)
    if (0x1F600 <= code <= 0x1F64F or
        0x1F300 <= code <= 0x1F5FF or
        0x1F680 <= code <= 0x1F6FF or
        0x1F700 <= code <= 0x1F77F or
        0x1F780 <= code <= 0x1F7FF or
        0x1F800 <= code <= 0x1F8FF or
        0x1F900 <= code <= 0x1F9FF or
        0x1FA00 <= code <= 0x1FA6F or
        0x1FA70 <= code <= 0x1FAFF or
        0x2600 <= code <= 0x26FF or
        0x2700 <= code <= 0x27BF or
        0xFE00 <= code <= 0xFE0F or
        0x1F1E6 <= code <= 0x1F1FF):
        return True
    return False

def is_only_emojis_or_empty(text):
    if pd.isna(text) or text is None:
        return True
    s = str(text).strip()
    if not s or s.lower() == 'nan':
        return True
    non_ws = [c for c in s if not c.isspace() and c not in '.,!?-:;()[]{}*~_#/@']
    if not non_ws:
        return True
    return all(is_emoji(c) for c in non_ws)

def get_word_count(text):
    if pd.isna(text) or text is None:
        return 0
    s = str(text).strip()
    if not s or s.lower() == 'nan':
        return 0
    text_without_emojis = "".join(c if not is_emoji(c) else " " for c in s)
    words = re.findall(r'\b\w+\b', text_without_emojis)
    return len(words)

def main():
    start_time = time.time()
    csv_file = "Google_Photos_Master_Reviews.csv"
    xlsx_file = "Google_Photos_Master_Reviews.xlsx"
    csv_backup = "Google_Photos_Master_Reviews_backup_raw.csv"
    xlsx_backup = "Google_Photos_Master_Reviews_backup_raw.xlsx"

    print("--- Step 1: Creating Safety Backups ---")
    if not os.path.exists(csv_backup):
        print(f"Copying {csv_file} -> {csv_backup}...")
        shutil.copyfile(csv_file, csv_backup)
        print("CSV backup created successfully.")
    else:
        print("CSV backup already exists.")

    if os.path.exists(xlsx_file) and not os.path.exists(xlsx_backup):
        print(f"Copying {xlsx_file} -> {xlsx_backup}...")
        shutil.copyfile(xlsx_file, xlsx_backup)
        print("Excel backup created successfully.")
    else:
        print("Excel backup already exists or skipped.")

    print("\n--- Step 2: Processing and Filtering Dataset ---")
    print("Reading master CSV...")
    df = pd.read_csv(csv_file, low_memory=False)
    raw_count = len(df)
    print(f"Loaded {raw_count:,} raw reviews.")

    def full_text(row):
        t = str(row['title']).strip() if pd.notna(row['title']) and str(row['title']).lower() != 'nan' else ''
        c = str(row['content']).strip() if pd.notna(row['content']) and str(row['content']).lower() != 'nan' else ''
        if t and c:
            return f"{t} {c}"
        return c or t

    texts = df.apply(full_text, axis=1)
    word_counts = texts.apply(get_word_count)
    only_emojis = texts.apply(is_only_emojis_or_empty)

    keep_mask = (word_counts >= 8) & (~only_emojis)
    df_clean = df[keep_mask].copy()
    clean_count = len(df_clean)
    removed_count = raw_count - clean_count

    print(f"Filtering Results:")
    print(f"  Raw: {raw_count:,}")
    print(f"  Removed (< 8 words / emoji-only): {removed_count:,} ({removed_count/raw_count*100:.2f}%)")
    print(f"  Cleaned (>= 8 words): {clean_count:,} ({clean_count/raw_count*100:.2f}%)")

    print("\n--- Step 3: Writing Cleaned CSV File ---")
    df_clean.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"Saved {csv_file} ({os.path.getsize(csv_file)/1024/1024:.2f} MB).")

    print("\n--- Step 4: Writing Cleaned Excel File ---")
    if os.path.exists(xlsx_file):
        with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer:
            df_clean.to_excel(writer, sheet_name='Google Photos Reviews', index=False)
        print(f"Saved {xlsx_file} ({os.path.getsize(xlsx_file)/1024/1024:.2f} MB).")

    print(f"\nCompleted in {time.time() - start_time:.2f} seconds!")

if __name__ == '__main__':
    main()
