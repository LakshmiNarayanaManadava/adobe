import fitz  # PyMuPDF
import os
import json

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    title = ""
    font_sizes = {}

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if 'lines' in block:
                for line in block['lines']:
                    for span in line['spans']:
                        size = round(span['size'], 1)
                        font_sizes[size] = font_sizes.get(size, 0) + 1

    sorted_sizes = sorted(font_sizes.keys(), reverse=True)
    title_font_size = sorted_sizes[0] if sorted_sizes else None

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if 'lines' in block:
                for line in block['lines']:
                    for span in line['spans']:
                        text = span['text'].strip()
                        if not text:
                            continue
                        size = round(span['size'], 1)

                        if not title and title_font_size and size == title_font_size and page_num < 2:
                            title = text

                        if size in sorted_sizes[:3]:
                            level_index = sorted_sizes.index(size)
                            level = f"H{level_index+1}"
                            headings.append({
                                "level": level,
                                "text": text,
                                "page": page_num+1
                            })

    return {"title": title, "outline": headings}

def process_all_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            output_data = extract_outline(pdf_path)
            output_filename = os.path.splitext(filename)[0] + ".json"
            with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)
    process_all_pdfs(input_dir, output_dir)
