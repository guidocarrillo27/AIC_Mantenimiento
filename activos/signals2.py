import PyPDF2
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Activo

@receiver(pre_save, sender=Activo)
def compress_pdf(sender, instance, **kwargs):
    if instance.archivo and instance.archivo.name.endswith('.pdf'):
        pdf_file = instance.archivo
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        output_pdf = BytesIO()
        pdf_writer = PyPDF2.PdfWriter()

        # Comprimir cada página
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        pdf_writer.write(output_pdf)
        output_pdf.seek(0)

        instance.archivo = InMemoryUploadedFile(output_pdf, 'FileField', instance.archivo.name, 'application/pdf', output_pdf.tell(), None)
