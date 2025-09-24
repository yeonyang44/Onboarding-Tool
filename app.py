import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

st.title("Mitarbeiterdaten erfassen")

# PDF-Vorlage hochladen
vorlage = st.file_uploader("PDF Vorlage hochladen", type=["pdf"])

name = st.text_input("Name")
position = st.text_input("Position")
about = st.text_area("Über mich")
bild = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg"])

def create_filled_pdf(name, position, about, image_file, pdf_vorlage):
    if pdf_vorlage is None:
        st.error("Bitte PDF Vorlage hochladen!")
        return None
    
    original_pdf = PdfReader(pdf_vorlage)  # pdf_vorlage ist ein BytesIO Objekt hier! Kein Text öffnen
    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.drawString(100, 750, name)
    can.drawString(100, 730, position)
    can.drawString(100, 710, about)
    if image_file:
        can.drawImage(image_file, 100, 600, width=100, height=100)
    can.save()
    packet.seek(0)
    
    overlay_pdf = PdfReader(packet)
    writer = PdfWriter()
    page = original_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    writer.add_page(page)
    
    output_pdf = io.BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf

if st.button("PDF erstellen"):
    if not (name and position and about and bild and vorlage):
        st.error("Bitte alle Felder ausfüllen und Dateien hochladen!")
    else:
        pdf_bytes = create_filled_pdf(name, position, about, bild, vorlage)
        if pdf_bytes:
            st.download_button(
                label="PDF herunterladen",
                data=pdf_bytes,
                file_name="ausgefüllt.pdf",
                mime="application/pdf"
            )
