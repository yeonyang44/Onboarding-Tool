import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

st.title("Mitarbeiterdaten erfassen")

# Eingabeformulare
name = st.text_input("Name")
position = st.text_input("Position")
about = st.text_area("Über mich")
bild = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg"])

def create_filled_pdf(name, position, about, image_file):
    vorlage_pfad = "Albaad_NeueMitarbeiter_Onboarding_3_Template.pdf"  # muss im gleichen Ordner liegen
    original_pdf = PdfReader("Albaad_NeueMitarbeiter_Onboarding_3_Template.pdf")
    
    # Erstelle Overlay
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
    
    out_pdf = io.BytesIO()
    writer.write(out_pdf)
    out_pdf.seek(0)
    return out_pdf

if st.button("PDF erstellen"):
    if not (name and position and about and bild):
        st.error("Bitte alle Felder ausfüllen und Bild hochladen!")
    else:
        pdf_bytes = create_filled_pdf(name, position, about, bild)
        st.download_button(
            label="PDF herunterladen",
            data=pdf_bytes,
            file_name="gespeicherte_mitarbeiter.pdf",
            mime="application/pdf"
        )
