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

# function to sanitize and apply custom formatting for HTML content
def sanitize_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # allowed tags for reportlab compatibility
    allowed_tags = {"b", "i", "u", "br"}
    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()
        elif tag.name in {"sub", "sup"}:
            # Apply baseline shift to simulate subscript and superscript
            if tag.name == "sub":
                tag.wrap(soup.new_tag("font", size="8"))
                tag.insert_before(" ")
            elif tag.name == "sup":
                tag.wrap(soup.new_tag("font", size="8"))
                tag.insert_before(" ")

    return str(soup)

# collect program details inputs
st.title("Promo Driver Copy Entry")

st.header("Program Details")
sf_number = st.text_input("SF#")
pharma = st.text_input("Pharma")
brand = st.text_input("Brand")
product = st.text_input("Product")
product_abbr = st.text_input("Product Abbreviation")
program_url = st.text_input("Program URL")

# collect text placements data
st.header("Text Placements")

st.markdown('<p style="font-weight:bold; font-size:18px;">Enter Job code and date</p>', unsafe_allow_html=True)
job_code_text = st.text_input("Enter Job code and date (Text Ads)", max_chars=27)

headline_texts, body_copy_texts, references_texts, cta_texts, cta_links = [], [], [], [], []
for i in range(1, 5):
    st.subheader(f"Message #{i}")

    # Collect and sanitize each field's input data
    headline = st_quill(f"Headline #{i}", html=True, placeholder="Enter formatted headline here...")
    headline_texts.append(sanitize_html(headline))

    body_copy = st_quill(f"Body Copy #{i}", html=True, placeholder="Enter formatted body copy here...")
    body_copy_texts.append(sanitize_html(body_copy))

    references = st_quill(f"References/Footnotes #{i}", html=True, placeholder="Enter formatted references here...")
    references_texts.append(sanitize_html(references))

    cta = st.text_input(f"CTA #{i}", max_chars=20)
    cta_texts.append(cta)

    cta_link = st.text_input(f"CTA Link #{i}", value="https://")
    cta_links.append(cta_link)

# collect email placements data
st.header("Unbranded Emails")

st.markdown('<p style="font-weight:bold; font-size:18px;">Enter Job code and date for Emails</p>', unsafe_allow_html=True)
job_code_email = st.text_input("Enter Job code and date (Emails)", max_chars=27)

subject_texts, email_body_texts, email_references_texts, email_cta_texts, email_cta_links = [], [], [], [], []
for i in range(1, 5):
    st.subheader(f"Email #{i}")

    # Collect and sanitize each field's input data
    subject_line = st_quill(f"Email #{i} - Subject Line", html=True, placeholder="Enter formatted subject line here...")
    subject_texts.append(sanitize_html(subject_line))

    email_body = st_quill(f"Email #{i} - Body Copy", html=True, placeholder="Enter formatted body copy here...")
    email_body_texts.append(sanitize_html(email_body))

    email_references = st_quill(f"Email #{i} - References/Footnotes", html=True, placeholder="Enter formatted references here...")
    email_references_texts.append(sanitize_html(email_references))

    email_cta = st.text_input(f"Email #{i}", max_chars=20)
    email_cta_texts.append(email_cta)

    email_cta_link = st.text_input(f"CTA Link", value="https://")
    email_cta_links.append(email_cta_link)

# generate pdf with landscape orientation, page break, and updated styling
if st.button("Generate PDF"):
    pdf = SimpleDocTemplate("Promo_Driver_Script.pdf", pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # adjust styles to allow alignment and formatting
    header_style = styles["BodyText"]
    header_style.fontName = "Helvetica-Bold"
    header_style.textColor = colors.whitesmoke
    header_style.alignment = TA_LEFT

    # program details section
    program_details = f"SF#: {sf_number}<br/>Pharma: {pharma}<br/>Brand: {brand}<br/>Product: {product}<br/>Product Abbreviation: {product_abbr}<br/>Program URL: {program_url}"
    elements.append(Paragraph("Program Details", styles["Heading2"]))
    elements.append(Paragraph(program_details, styles["BodyText"]))

    # text placements table
    elements.append(Paragraph("Text Placements Job Code", styles["Heading2"]))
    elements.append(Paragraph(job_code_text, styles["BodyText"]))

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
            Paragraph(headline_texts[i], styles["BodyText"]),
            Paragraph(body_copy_texts[i], styles["BodyText"]),
            Paragraph(references_texts[i], styles["BodyText"]),
            Paragraph(cta_texts[i], styles["BodyText"]),
            Paragraph(cta_links[i], styles["BodyText"]),
        ])

    text_table = Table(text_table_data, colWidths=[1 * inch, 2 * inch, 3 * inch, 2 * inch, 1 * inch, 2 * inch])
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

    # add page break before email placements
    elements.append(PageBreak())

    # email placements table with line breaks for character counts in headers
    elements.append(Paragraph("Email Job Code", styles["Heading2"]))
    elements.append(Paragraph(job_code_email, styles["BodyText"]))

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
            Paragraph(subject_texts[i], styles["BodyText"]),
            Paragraph(email_body_texts[i], styles["BodyText"]),
            Paragraph(email_references_texts[i], styles["BodyText"]),
            Paragraph(email_cta_texts[i], styles["BodyText"]),
            Paragraph(email_cta_links[i], styles["BodyText"]),
        ])

    email_table = Table(email_table_data, colWidths=[1 * inch, 2 * inch, 3 * inch, 2 * inch, 1 * inch, 2 * inch])
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
