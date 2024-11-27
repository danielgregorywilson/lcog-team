# from pypdf import PdfWriter

# merger = PdfWriter()

# for pdf in ["test-doc-1.pdf", "test-doc-2.pdf"]:
#     merger.append(pdf)

# merger.write("merged-pdf.pdf")
# merger.close()






from pypdf import PdfWriter

merger = PdfWriter()

input1 = open("test-doc-1.pdf", "rb")
input2 = open("test-doc-2.pdf", "rb")

# Add the first 3 pages of input1 document to output
merger.append(fileobj=input1)

# Append entire input3 document to the end of the output document
merger.append(input2)

# Write to an output PDF document
output = open("document-output.pdf", "wb")
merger.write(output)

# Close file descriptors
merger.close()
output.close()