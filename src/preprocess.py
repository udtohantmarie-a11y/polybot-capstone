import os
import re
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
        return text
    except FileNotFoundError:
        print("Error: The file " + pdf_path + " was not found.")
        return ""
    except Exception as e:
        print("An error occurred: " + str(e))
        return ""

def clean_text(raw_text):
    # Remove newlines and replace them with spaces to normalize formatting
    cleaned_text = re.sub(r'\n+', ' ', raw_text)
    # Remove multiple continuous spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # Keep only alphanumeric characters and basic punctuation to remove noise
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,?!-]', '', cleaned_text)
    return cleaned_text.strip()

def main():
    # Fix: Use absolute paths based on the script's location to prevent CWD errors
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_pdf = os.path.join(base_dir, 'data', 'TPC Student Handbook.pdf')
    output_txt = os.path.join(base_dir, 'data', 'cleaned_handbook.txt')

    print("Starting data extraction...")
    raw_text = extract_text_from_pdf(input_pdf)
    
    if not raw_text:
        print("Extraction failed. Please check if the PDF file is exactly named 'TPC Student Handbook.pdf' and is inside the data folder.")
        return

    print("Cleaning the extracted text...")
    cleaned_text = clean_text(raw_text)

    print("Saving cleaned text to " + output_txt + "...")
    try:
        # Ensure the data directory exists before saving
        os.makedirs(os.path.dirname(output_txt), exist_ok=True)
        with open(output_txt, "w", encoding="utf-8") as text_file:
            text_file.write(cleaned_text)
        print("Data preprocessing complete. File saved successfully.")
    except Exception as e:
        print("Failed to save the file: " + str(e))

if __name__ == "__main__":
    main()