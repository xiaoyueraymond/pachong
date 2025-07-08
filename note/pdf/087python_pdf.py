import fitz  # PyMuPDF library
import os    # For handling files and directories

# Get the directory where the script is located
current_folder = os.path.dirname(os.path.realpath(__file__))

# Loop through all files in the script's folder
for filename in os.listdir(current_folder):
    # Check if the file is a PDF
    if filename.lower().endswith('.pdf'):
        # Define input and output file paths
        input_pdf = os.path.join(current_folder, filename)
        output_pdf = os.path.join(current_folder, f"modified_{filename}")

        # Print the input and output paths
        print(f"Input PDF: {input_pdf}")
        print(f"Output PDF: {output_pdf}")

        # Open the PDF
        pdf_document = fitz.open(input_pdf)

        # Loop through all pages in the current PDF
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

        print(f"Processed {filename} and saved as {output_pdf}")

print("All PDFs in the folder have been processed.")