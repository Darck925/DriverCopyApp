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
    allowed_tags = {"i", "u", "br"}  # removed "b" from allowed tags
    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()
    return str(soup)

# updated display_rtf_with_counter function to apply sanitize_html
def display_rtf_with_counter(label, placeholder):
    rtf_content = st_quill(label, html=True, placeholder=placeholder)
    if rtf_content:
        char_count = len(BeautifulSoup(rtf_content, "html.parser").get_text())
        st.write(f"Character count: {char_count}")
    # sanitize html content to remove any residual bold tags
    sanitized_content = sanitize_html(rtf_content)
    return sanitized_content

# utility function to display character count
def display_rtf_with_counter(label, placeholder):
    rtf_content = st_quill(label, html=True, placeholder=placeholder)
    if rtf_content:
        char_count = len(BeautifulSoup(rtf_content, "html.parser").get_text())
        st.write(f"Character count: {char_count}")
    return sanitize_html(rtf_content)

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
    headline = display_rtf_with_counter(f"Headline #{i}", "Enter formatted headline here...")
    headline_texts.append(headline)
    body_copy = display_rtf_with_counter(f"Body Copy #{i}", "Enter formatted body copy here...")
    body_copy_texts.append(body_copy)
    references = display_rtf_with_counter(f"References/Footnotes #{i}", "Enter formatted references here...")
    references_texts.append(references)
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
    subject_line = display_rtf_with_counter(f"Email #{i} - Subject Line", "Enter formatted subject line here...")
    subject_texts.append(subject_line)
    email_body = display_rtf_with_counter(f"Email #{i} - Body Copy", "Enter formatted body copy here...")
    email_body_texts.append(email_body)
    email_references = display_rtf_with_counter(f"Email #{i} - References/Footnotes", "Enter formatted references here...")
    email_references_texts.append(email_references)
    email_cta = st.text_input(f"CTA #{i}", max_chars=20, key=f"email_cta_{i}")
    email_cta_texts.append(email_cta)
    email_cta_link = st.text_input(f"CTA Link #{i}", value="https://", key=f"email_cta_link_{i}")
    email_cta_links.append(email_cta_link)

# generate pdf with selective bold and black font color applied directly
if st.button("Generate PDF"):
    pdf = SimpleDocTemplate("Promo_Driver_Script.pdf", pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # custom style for regular body text (not bold)
    body_text_style = styles["BodyText"]
    body_text_style.fontName = "Helvetica"
    body_text_style.fontSize = 10
    body_text_style.textColor = colors.black

    # create a separate style for bold text only where explicitly required
    bold_text_style = styles["BodyText"]
    bold_text_style.fontName = "Helvetica-Bold"
    bold_text_style.fontSize = 10
    bold_text_style.textColor = colors.black

    # program details section
    program_details = f"SF#: {sf_number}<br/>Pharma: {pharma}<br/>Brand: {brand}<br/>Product: {product}<br/>Product Abbreviation: {product_abbr}<br/>Program URL: {program_url}"
    elements.append(Paragraph("Program Details", styles["Heading2"]))
    elements.append(Paragraph(f'<font color="black">{program_details}</font>', body_text_style))

    # text placements table
    elements.append(Paragraph("Text Placements Job Code", styles["Heading2"]))
    elements.append(Paragraph(f'<font color="black">{job_code_text}</font>', body_text_style))

    text_table_data = [
        [
            "Message #",
            Paragraph('<font color="whitesmoke">Headline<br/>(80 chars max)</font>', bold_text_style),
            Paragraph('<font color="whitesmoke">Body Copy<br/>(100 chars max)</font>', bold_text_style),
            Paragraph('<font color="whitesmoke">References/Footnotes<br/>(86 chars max)</font>', bold_text_style),
            Paragraph('<font color="whitesmoke">CTA<br/>(20 chars max)</font>', bold_text_style),
            Paragraph('<font color="whitesmoke">CTA Link</font>', bold_text_style)
        ]
    ]
    for i in range(4):
        text_table_data.append([
            f"Message #{i + 1}",
            Paragraph(f'<font color="black">{headline_texts[i]}</font>', body_text_style),
            Paragraph(f'<font color="black">{body_copy_texts[i]}</font>', body_text_style),
            Paragraph(f'<font color="black">{references_texts[i]}</font>', body_text_style),
            Paragraph(f'<font color="black">{cta_texts[i]}</font>', body_text_style),
            Paragraph(f'<font color="black">{cta_links[i]}</font>', body_text_style),
        ])

    text_table = Table(text_table_data, colWidths=[0.8 * inch, 2 * inch, 3 * inch, 2 * inch, 1.2 * inch, 2 * inch])
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

    # add page break
    elements.append(PageBreak())

    # email placements table
    elements.append(Paragraph("Email Job Code", styles["Heading2"]))
    elements.append(Paragraph(f'<font color="black">{job_code_email}</font>', body_text_style))

    email_table_data = [
        [
            "Email #",
            Paragraph('<font color="whitesmoke">Subject Line<br/>(65 chars max)</font>', bold_text_style),
            Paragraph('<font color="whitesmoke">Body Copy<br/>(350 chars max)</font>', bold_text_style),
            Paragraph('<font color="whitesmoke">References/Footnotes<br/>(86 chars max)</font>', bold_text_style),
            Paragraph('<font color="whitesmoke">CTA<br/>(20 chars max)</font>', bold_text_style),
            Paragraph('<font color="whitesmoke">CTA Link</font>', bold_text_style)
        ]
    ]
    for i in range(4):
        email_table_data.append([
            f"Email #{i + 1}",
            Paragraph(f'<font color="black">{subject_texts[i]}</font>', body_text_style),
            Paragraph(f'<font color="black">{email_body_texts[i]}</font>', body_text_style),
            Paragraph(f'<font color="black">{email_references_texts[i]}</font>', body_text_style),
            Paragraph(f'<font color="black">{email_cta_texts[i]}</font>', body_text_style),
            Paragraph(f'<font color="black">{email_cta_links[i]}</font>', body_text_style),
        ])

    email_table = Table(email_table_data, colWidths=[0.8 * inch, 2 * inch, 3 * inch, 2 * inch, 1.2 * inch, 2 * inch])
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


