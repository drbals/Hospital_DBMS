from fpdf import FPDF

# Create a PDF instance
pdf = FPDF()

# Add a page to the PDF
pdf.add_page()

# Set font for the PDF
pdf.set_font("Arial", size=12)

# Add a cell with some text
pdf.cell(200, 10, txt="Hello, this is a simple PDF file!", ln=True, align="C")

# Save the PDF to a file
pdf.output("Invoice.pdf")

print("PDF created successfully!")