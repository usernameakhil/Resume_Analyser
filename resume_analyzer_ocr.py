import fitz  # PyMuPDF
import argparse
import re

# Define a list of key skills to look for
KEY_SKILLS = [
    "Python", "SQL", "Machine Learning", "Deep Learning", "NLP",
    "Data Analysis", "Pandas", "NumPy", "TensorFlow", "PyTorch",
    "Scikit-learn", "Excel", "Power BI", "AWS", "Docker"
]

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file using PyMuPDF"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

def count_keywords(text, keywords):
    """Count occurrences of each keyword in the text"""
    text_lower = text.lower()
    counts = {}
    for keyword in keywords:
        pattern = rf"\b{re.escape(keyword.lower())}\b"
        count = len(re.findall(pattern, text_lower))
        counts[keyword] = count
    return counts

def suggest_improvements(counts):
    """Suggest which important skills are missing"""
    missing_skills = [skill for skill, count in counts.items() if count == 0]
    if missing_skills:
        print("\n🔍 You may want to consider adding these skills:")
        for skill in missing_skills:
            print(f" - {skill}")
    else:
        print("\n✅ Great! Your resume includes all the key skills.")

def main():
    parser = argparse.ArgumentParser(description="📄 Resume Analyzer CLI Tool")
    parser.add_argument("pdf_path", help="Path to your resume in PDF format")
    args = parser.parse_args()

    print("📥 Extracting text from resume...")
    text = extract_text_from_pdf(args.pdf_path)

    if not text.strip():
        print("⚠️ No text extracted. Check if the PDF is scanned or empty.")
        return

    print("\n🔑 Analyzing for key skills...\n")
    counts = count_keywords(text, KEY_SKILLS)

    for skill, count in counts.items():
        print(f"{skill}: {count} mention(s)")

    suggest_improvements(counts)

if __name__ == "__main__":
    main()
