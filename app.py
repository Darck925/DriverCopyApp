import streamlit as st
from streamlit_quill import st_quill
from fpdf import FPDF
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

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

st.text("Enter Job code and date")
job_code_text = st.text_input("Enter Job code and date (Text Ads)", max_chars=27)

# message entries with rich-text formatting
for i in range(1, 5):
    st.subheader(f"Message #{i}")
    headline = st.text_input(f"Headline #{i}", max_chars=80)
    body_copy = st_quill(f"Body Copy #{i}", html=True, placeholder="Enter formatted body copy here...")
    references = st_quill(f"References/Footnotes #{i}", html=True, placeholder="Enter formatted references here...")
    cta = st.text_input(f"CTA #{i}", max_chars=20)
    cta_link = st.text_input(f"CTA Link #{i}", value="https://")
    st.write("---")

# email placements section
st.header("Unbranded Emails")

# separate job code field for email section
st.text("Enter Job code and date for Emails")
job_code_email = st.text_input("Enter Job code and date (Emails)", max_chars=27)

for i in range(1, 5):
    st.subheader(f"Email #{i}")
    subject_line = st.text_input(f"Email #{i} - Subject Line", max_chars=65)
    email_headline = st.text_input(f"Email #{i} - Headline", max_chars=80)
    email_body = st_quill(f"Email #{i} - Body Copy", html=True, placeholder="Enter formatted body copy here...")
    email_references = st_quill(f"Email #{i} - References/Footnotes", html=True, placeholder="Enter formatted references here...")
    email_cta = st.text_input(f"Email #{i} - CTA", max_chars=20)
    email_cta_link = st.text_input(f"Email #{i} - CTA Link", value="https://")
    st.write("---")

# generate pdf with rich-text support
if st.button("Generate PDF", key="generate_pdf"):
    pdf = SimpleDocTemplate("Promo_Driver_Script.pdf", pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # add program details
    program_details = f"SF#: {sf_number}<br/>Pharma: {pharma}<br/>Brand: {brand}<br/>Product: {product}<br/>Product Abbreviation: {product_abbr}<br/>Program URL: {program_url}"
    elements.append(Paragraph("Program Details", styles["Heading2"]))
    elements.append(Paragraph(program_details, styles["BodyText"]))

    # add text placements with rich-text formatting
    elements.append(Paragraph("Text Placements Job Code", styles["Heading2"]))
    elements.append(Paragraph(job_code_text, styles["BodyText"]))
    for i in range(1, 5):
        elements.append(Paragraph(f"Message #{i}", styles["Heading2"]))
        elements.append(Paragraph(f"Headline: {headline}", styles["BodyText"]))
        elements.append(Paragraph(f"Body Copy: {body_copy}", styles["BodyText"]))
        elements.append(Paragraph(f"References/Footnotes: {references}", styles["BodyText"]))
        elements.append(Paragraph(f"CTA: {cta}", styles["BodyText"]))
        elements.append(Paragraph(f"CTA Link: {cta_link}", styles["BodyText"]))

    # add email placements with rich-text formatting
    elements.append(Paragraph("Email Job Code", styles["Heading2"]))
    elements.append(Paragraph(job_code_email, styles["BodyText"]))
    for i in range(1, 5):
        elements.append(Paragraph(f"Email #{i}", styles["Heading2"]))
        elements.append(Paragraph(f"Subject Line: {subject_line}", styles["BodyText"]))
        elements.append(Paragraph(f"Headline: {email_headline}", styles["BodyText"]))
        elements.append(Paragraph(f"Body Copy: {email_body}", styles["BodyText"]))
        elements.append(Paragraph(f"References/Footnotes: {email_references}", styles["BodyText"]))
        elements.append(Paragraph(f"CTA: {email_cta}", styles["BodyText"]))
        elements.append(Paragraph(f"CTA Link: {email_cta_link}", styles["BodyText"]))

    # save the pdf
    pdf.build(elements)

    # provide download link
    with open("Promo_Driver_Script.pdf", "rb") as f:
        pdf_data = f.read()
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Promo_Driver_Script.pdf">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
