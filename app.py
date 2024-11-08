import streamlit as st
from streamlit_quill import st_quill
from bs4 import BeautifulSoup
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT

# sanitize html function to retain formatting tags and remove unsupported tags
def sanitize_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    allowed_tags = {"b", "i", "u", "br"}
    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()
    return str(soup)

# collect input fields
st.title("Promo Driver Copy Entry")

# program details section
st.header("Program Details")
sf_number = st.text_input("SF#")
pharma = st.text_input("Pharma")
brand = st.text_input("Brand")
product = st.text_input("Product")
product_abbr = st.text_input("Product Abbreviation")
program_url = st.text_input("Program URL")

# text placements
st.header("Text Placements")
job_code_text = st.text_input("Enter Job code and date (Text Ads)", max_chars=27)

headline_texts, body_copy_texts, references_texts, cta_texts, cta_links = [], [], [], [], []
for i in range(1, 5):
    st.subheader(f"Message #{i}")
    headline = st_quill(f"Headline #{i}", html=True)
    headline_texts.append(sanitize_html(headline))
    body_copy = st_quill(f"Body Copy #{i}", html=True)
    body_copy_texts.append(sanitize_html(body_copy))
    references = st_quill(f"References/Footnotes #{i}", html=True)
    references_texts.append(sanitize_html(references))
    cta = st.text_input(f"CTA #{i}", max_chars=20)
    cta_texts.append(cta)
    cta_link = st.text_input(f"CTA Link #{i}", value="https://", key=f"text_cta_link_{i}")
    cta_links.append(cta_link)

# email placements
st.header("Unbranded Emails")
job_code_email = st.text_input("Enter Job code and date (Emails)", max_chars=27)

subject_texts, email_body_texts, email_references_texts, email_cta_texts, email_cta_links = [], [], [], [], []
for i in range(1, 5):
    st.subheader(f"Email #{i}")
    subject_line = st_quill(f"Email #{i} - Subject Line", html=True)
    subject_texts.append(sanitize_html(subject_line))
    email_body = st_quill(f"Email #{i} - Body Copy", html=True)
    email_body_texts.append(sanitize_html(email_body))
    email_references = st_quill(f"Email #{i} - References/Footnotes", html=True)
    email_references_texts.append(sanitize_html(email_references))
    email_cta = st.text_input(f"CTA #{i}", max_chars=20, key=f"email_cta_{i}")
    email_cta_texts.append(email_cta)
    email_cta_link = st.text_input(f"CTA Link #{i}", value="https://", key=f"email_cta_link_{i}")
    email_cta_links.append(email_cta_link)

# generate pdf button
if st.button("Generate PDF"):
    pdf = SimpleDocTemplate("Promo_Driver_Script.pdf", pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # custom styles for readability
    body_text_style = styles["BodyText"]
    body_text_style.textColor = colors.black
    body_text_style.fontName = "Helvetica"

    header_style = styles["BodyText"]
    header_style.fontName = "Helvetica-Bold"
    header_style.textColor = colors.whitesmoke

    # program details section
    program_details = f"SF#: {sf_number}<br/>Pharma: {pharma}<br/>Brand: {brand}<br/>Product: {product}<br/>Product Abbreviation: {product_abbr}<br/>Program URL: {program_url}"
    elements.append(Paragraph("Program Details", styles["Heading2"]))
    elements.append(Paragraph(program_details, body_text_style))

    # text placements table
    elements.append(Paragraph("Text Placements Job Code", styles["Heading2"]))
    elements.append(Paragraph(job_code_text, body_text_style))

    text_table_data = [
        [
            "Message #",
            Paragraph('<font color="whitesmoke"><b>Headline<br/>(80 chars max)</b></font>', header_style),
            Paragraph('<font color="whitesmoke"><b>Body Copy<br/>(100 chars max)</b></font>', header_style),
            Paragraph('<font color="whitesmoke"><b>References/Footnotes<br/>(86 chars max)</b></font>', header_style),
            Paragraph('<font color="whitesmoke"><b>CTA<br/>(20 chars max)</b></font>', header_style),
            Paragraph('<font color="whitesmoke"><b>CTA Link</b></font>', header_style)
        ]
    ]
    for i in range(4):
        text_table_data.append([
            f"Message #{i + 1}",
            Paragraph(headline_texts[i], body_text_style),
            Paragraph(body_copy_texts[i], body_text_style),
            Paragraph(references_texts[i], body_text_style),
            Paragraph(cta_texts[i], body_text_style),
            Paragraph(cta_links[i], body_text_style),
        ])

    text_table = Table(text_table_data, colWidths=[0.7 * inch, 1.5 * inch, 2.5 * inch, 2 * inch, 1 * inch, 1.5 * inch])
    text_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(text_table)

    # page break for email placements
    elements.append(PageBreak())

    # email placements table
    elements.append(Paragraph("Email Job Code", styles["Heading2"]))
    elements.append(Paragraph(job_code_email, body_text_style))

    email_table_data = [
        [
            "Email #",
            Paragraph('<font color="whitesmoke"><b>Subject Line<br/>(65 chars max)</b></font>', header_style),
            Paragraph('<font color="whitesmoke"><b>Body Copy<br/>(350 chars max)</b></font>', header_style),
            Paragraph('<font color="whitesmoke"><b>References/Footnotes<br/>(86 chars max)</b></font>', header_style),
            Paragraph('<font color="whitesmoke"><b>CTA<br/>(20 chars max)</b></font>', header_style),
            Paragraph('<font color="whitesmoke"><b>CTA Link</b></font>', header_style)
        ]
    ]
    for i in range(4):
        email_table_data.append([
            f"Email #{i + 1}",
            Paragraph(subject_texts[i], body_text_style),
            Paragraph(email_body_texts[i], body_text_style),
            Paragraph(email_references_texts[i], body_text_style),
            Paragraph(email_cta_texts[i], body_text_style),
            Paragraph(email_cta_links[i], body_text_style),
        ])

    email_table = Table(email_table_data, colWidths=[0.7 * inch, 1.5 * inch, 2.5 * inch, 2 * inch, 1 * inch, 1.5 * inch])
    email_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
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
