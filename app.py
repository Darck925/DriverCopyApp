# app.py
import streamlit as st
from fpdf import FPDF

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

# text placements section
st.title("Promo Driver Copy Entry")
st.header("Text Placements")

st.text("Job Code (include in builds):")
job_code = st.text_input("Enter job code", max_chars=20)  # change max chars as needed

# message entries
for i in range(1, 5):
    st.subheader(f"Message #{i}")
    headline = st.text_input(f"Headline #{i}", max_chars=80)
    body_copy = st.text_area(f"Body Copy #{i} (100 characters max)", max_chars=100)
    cta = st.text_input(f"CTA #{i}", max_chars=20)
    cta_link = st.text_input(f"CTA Link #{i}", value="https://")
    st.write("---")

# email placements section
st.header("Unbranded Emails")

for i in range(1, 5):
    st.subheader(f"Email #{i}")
    subject_line = st.text_input(f"Email #{i} - Subject Line", max_chars=65)
    email_headline = st.text_input(f"Email #{i} - Headline", max_chars=80)
    email_body = st.text_area(f"Email #{i} - Body Copy (350 characters max)", max_chars=350)
    email_cta = st.text_input(f"Email #{i} - CTA", max_chars=20)
    email_cta_link = st.text_input(f"Email #{i} - CTA Link", value="https://")
    st.write("---")

# generate pdf
if st.button("Generate PDF"):
    pdf = PDF()
    pdf.add_page()

    pdf.add_section("Job Code", job_code)
    for i in range(1, 5):
        pdf.add_section(f"Message #{i}", f"Headline: {headline}\nBody: {body_copy}\nCTA: {cta}\nLink: {cta_link}")

    for i in range(1, 5):
        pdf.add_section(f"Email #{i}", f"Subject Line: {subject_line}\nHeadline: {email_headline}\nBody: {email_body}\nCTA: {email_cta}\nLink: {email_cta_link}")

    pdf.output("Promo_Driver_Script.pdf")
    st.success("PDF generated successfully! Check your download folder.")

