import streamlit as st
from streamlit_quill import st_quill
from fpdf import FPDF
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup

# function to get plain text and count characters from HTML
def get_text_and_count(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text()
    return text, len(text)

# add custom css for larger bold labels
st.markdown("""
    <style>
    .label {
        font-weight: bold;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# program details section
st.title("Promo Driver Copy Entry")

st.header("Program Details")
sf_number = st.text_input("SF#")
pharma = st.text_input("Pharma")
brand = st.text_input("Brand")
product = st.text_input("Product")
product_abbr = st.text_input("Product Abbreviation")
program_url = st.text_input("Program URL")

# text placements section
st.header("Text Placements")

st.markdown('<p class="label">Enter Job code and date</p>', unsafe_allow_html=True)
job_code_text = st.text_input("Enter Job code and date (Text Ads)", max_chars=27)

# message entries with rich-text formatting for Headline
for i in range(1, 5):
    st.subheader(f"Message #{i}")
    
    st.markdown('<p class="label">Headline</p>', unsafe_allow_html=True)
    headline = st_quill(f"Headline #{i}", html=True, placeholder="Enter formatted headline here...")
    headline_text, headline_count = get_text_and_count(headline)
    st.write(f"Character count: {headline_count} / 80")
    
    st.markdown('<p class="label">Body Copy (100 characters max)</p>', unsafe_allow_html=True)
    body_copy = st_quill(f"Body Copy #{i}", html=True, placeholder="Enter formatted body copy here...")
    body_copy_text, body_copy_count = get_text_and_count(body_copy)
    st.write(f"Character count: {body_copy_count} / 100")
    
    st.markdown('<p class="label">References/Footnotes (86 characters max)</p>', unsafe_allow_html=True)
    references = st_quill(f"References/Footnotes #{i}", html=True, placeholder="Enter formatted references here...")
    references_text, references_count = get_text_and_count(references)
    st.write(f"Character count: {references_count} / 86")
    
    st.markdown('<p class="label">CTA (20 characters max)</p>', unsafe_allow_html=True)
    cta = st.text_input(f"CTA #{i}", max_chars=20)
    
    st.markdown('<p class="label">CTA Link</p>', unsafe_allow_html=True)
    cta_link = st.text_input(f"CTA Link #{i}", value="https://")
    
    st.write("---")

# email placements section
st.header("Unbranded Emails")

# separate job code field for email section
st.markdown('<p class="label">Enter Job code and date for Emails</p>', unsafe_allow_html=True)
job_code_email = st.text_input("Enter Job code and date (Emails)", max_chars=27)

for i in range(1, 5):
    st.subheader(f"Email #{i}")
    
    st.markdown('<p class="label">Subject Line (65 characters max)</p>', unsafe_allow_html=True)
    subject_line = st_quill(f"Email #{i} - Subject Line", html=True, placeholder="Enter formatted subject line here...")
    subject_text, subject_count = get_text_and_count(subject_line)
    st.write(f"Character count: {subject_count} / 65")
    
    st.markdown('<p class="label">Body Copy (350 characters max)</p>', unsafe_allow_html=True)
    email_body = st_quill(f"Email #{i} - Body Copy", html=True, placeholder="Enter formatted body copy here...")
    email_body_text, email_body_count = get_text_and_count(email_body)
    st.write(f"Character count: {email_body_count} / 350")
    
    st.markdown('<p class="label">References/Footnotes (86 characters max)</p>', unsafe_allow_html=True)
    email_references = st_quill(f"Email #{i} - References/Footnotes", html=True, placeholder="Enter formatted references here...")
    email_references_text, email_references_count = get_text_and_count(email_references)
    st.write(f"Character count: {email_references_count} / 86")
    
    st.markdown('<p class="label">CTA (20 characters max)</p>', unsafe_allow_html=True)
    email_cta = st.text_input(f"Email #{i} - CTA", max_chars=20)
    
    st.markdown('<p class="label">CTA Link</p>', unsafe_allow_html=True)
    email_cta_link = st.text_input(f"Email #{i} - CTA Link", value="https://")
    
    st.write("---")

# generate pdf with landscape orientation, page break, and updated styling
if st.button("Generate PDF", key="generate_pdf"):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.platypus import Table, TableStyle, PageBreak

    pdf = SimpleDocTemplate("Promo_Driver_Script.pdf", pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # add program details section
    program_details = f"SF#: {sf_number}<br/>Pharma: {pharma}<br/>Brand: {brand}<br/>Product: {product}<br/>Product Abbreviation: {product_abbr}<br/>Program URL: {program_url}"
    elements.append(Paragraph("Program Details", styles["Heading2"]))
    elements.append(Paragraph(program_details, styles["BodyText"]))

    # text placements table
    elements.append(Paragraph("Text Placements Job Code", styles["Heading2"]))
    elements.append(Paragraph(job_code_text, styles["BodyText"]))

    # define table data with headers for text placements
    text_table_data = [
        ["Message #", "Headline (80 chars max)", "Body Copy (100 chars max)", "References/Footnotes (86 chars max)", "CTA (20 chars max)", "CTA Link"]
    ]

    # add each message row with data
    for i in range(1, 5):
        text_table_data.append([
            f"Message #{i}",
            headline_text,
            body_copy_text,
            references_text,
            cta,
            cta_link
        ])

    # create and style the text placements table
    text_table = Table(text_table_data, colWidths=[1 * inch, 2 * inch, 3 * inch, 2 * inch, 1 * inch, 2 * inch])
    text_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # grey header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # white cell background
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elements.append(text_table)

    # add a page break before the email placements section
    elements.append(PageBreak())

    # email placements table
    elements.append(Paragraph("Email Job Code", styles["Heading2"]))
    elements.append(Paragraph(job_code_email, styles["BodyText"]))

    # define table data with headers for email placements
    email_table_data = [
        ["Email #", "Subject Line (65 chars max)", "Body Copy (350 chars max)", "References/Footnotes (86 chars max)", "CTA (20 chars max)", "CTA Link"]
    ]

    # add each email row with data
    for i in range(1, 5):
        email_table_data.append([
            f"Email #{i}",
            subject_text,
            email_body_text,
            email_references_text,
            email_cta,
            email_cta_link
        ])

    # create and style the email placements table
    email_table = Table(email_table_data, colWidths=[1 * inch, 2 * inch, 3 * inch, 2 * inch, 1 * inch, 2 * inch])
    email_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # grey header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # white cell background
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elements.append(email_table)

    # save the pdf
    pdf.build(elements)

    # provide download link
    with open("Promo_Driver_Script.pdf", "rb") as f:
        pdf_data = f.read()
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Promo_Driver_Script.pdf">Download PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

