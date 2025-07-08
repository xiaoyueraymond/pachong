import fitz  # PyMuPDF library

# Input and output file paths
input_pdf = r"C:\Users\musk8\Desktop\取土\唛头_SZSH25031258_YYZ3.PDF"
output_pdf = r"C:\Users\musk8\Desktop\取土\1.pdf"

# Open the PDF
pdf_document = fitz.open(input_pdf)

# Loop through all pages
for page_num in range(len(pdf_document)):
    # Select the current page
    page = pdf_document[page_num]

    # Remove the text "MADE IN CHINA"
    text_instances = page.search_for("MADE IN CHINA")
    for inst in text_instances:
        page.add_redact_annot(inst)  # Mark the text for redaction
    page.apply_redactions()  # Apply the redactions to remove the text

    # Remove all shapes (graphical objects)
    for item in page.get_drawings():  # Get all drawing objects (shapes)
        page.add_redact_annot(item["rect"])  # Mark each shape for redaction
    page.apply_redactions()  # Apply redactions to remove shapes

# Save the modified PDF to the output file
pdf_document.save(output_pdf)
pdf_document.close()

print(f"Modified PDF saved as {output_pdf}")