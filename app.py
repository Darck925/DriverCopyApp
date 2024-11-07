import streamlit as st
from fpdf import FPDF
import base64

# define pdf creation
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Promo Drivers Template", 0, 1, "C")
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def add_section(self, title, content):
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, title, 0, 1)
        self.set_font("Arial", "", 9)
        self.multi_cell(0, 8, content)
        self.ln(5)

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
job_code_text = st.text_input("Enter Job code and date", max_chars=27)  # 27-character limit for job code in text ad section

# message entries
for i in range(1, 5):
    st.subheader(f"Message #{i}")
    headline = st.text_input(f"Headline #{i}", max_chars=80)
    body_copy = st.text_area(f"Body Copy #{i} (100 characters max)", max_chars=100)
    references = st.text_input(f"References/Footnotes #{i}", max_chars=86)  # new References/Footnotes field with 86 char limit
    cta = st.text_input(f"CTA #{i}", max_chars=20)
    cta_link = st.text_input(f"CTA Link #{i}", value="https://")
    st.write("---")

# email placements section
st.header("Unbranded Emails")

# separate job code field for email section
st.text("Enter Job code and date for Emails")
job_code_email = st.text_input("Enter Job code and date (Emails)", max_chars=27)  # 27-character limit for job code in email section

for i in range(1, 5):
    st.subheader(f"Email #{i}")
    subject_line = st.text_input(f"Email #{i} - Subject Line", max_chars=65)
    email_headline = st.text_input(f"Email #{i} - Headline", max_chars=80)
    email_body = st.text_area(f"Email #{i} - Body Copy (350 characters max)", max_chars=350)
    email_references = st.text_input(f"Email #{i} - References/Footnotes", max_chars=86)  # new References/Footnotes field with 86 char limit
    email_cta = st.text_input(f"Email #{i} - CTA", max_chars=20)
    email_cta_link = st.text_input(f"Email #{i} - CTA Link", value="https://")
    st.write("---")

# generate pdf
if st.button("Generate PDF", key="generate_pdf"):
    pdf = PDF()
    pdf.add_page()

    # add program details
    pdf.add_section("Program Details", f"SF#: {sf_number}\nPharma: {pharma}\nBrand: {brand}\nProduct: {product}\nProduct Abbreviation: {product_abbr}\nProgram URL: {program_url}")

    # add text placements
    pdf.add_section("Job Code (Text Ads)", job_code_text)
    for i in range(1, 5):
        pdf.add_section(f"Message #{i}", f"Headline: {headline}\nBody: {body_copy}\nReferences: {references}\nCTA: {cta}\nLink: {cta_link}")

    # add email placements
    pdf.add_section("Job Code (Emails)", job_code_email)
    for i in range(1, 5):
        pdf.add_section(f"Email #{i}", f"Subject Line: {subject_line}\nHeadline: {email_headline}\nBody: {email_body}\nReferences: {email_references}\nCTA: {email_cta}\nLink: {email_cta_link}")

    pdf.output("Promo_Driver_Script.pdf")

    # provide download link
    with open("Promo_Driver_Script.pdf", "rb") as f:
        pdf_data = f.read()
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Promo_Driver_Script.pdf">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
