from django.db import models
import os
from.Maquina import Maquina
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import pikepdf

# Función para reducir el tamaño de la imagen
def resize_image(image, max_width=800, max_height=800):
    img = Image.open(image)

    if img.format not in ['JPEG','PNG','WEBP']:
        raise ValueError(f"Formato de imagen no soportado:{img.format}.")
    
    img.thumbnail((max_width, max_height), Image.LANCZOS)  # Usamos Image.LANCZOS para la reducción  
    img=img.convert('RGB')

    # Guardar la imagen redimensionada en un archivo temporal en memoria
    temp_file = BytesIO()
    img.save(temp_file, format='JPEG')
    temp_file.seek(0)
    return temp_file

# Función para comprimir el archivo PDF utilizando pikepdf
def compress_pdf(input_pdf):
    # Crear una instancia de pikepdf
    pdf = pikepdf.open(input_pdf)
    # Reducir el tamaño eliminando los objetos no utilizados
    pdf.save('/tmp/compressed.pdf')  # Guardamos el PDF comprimido en un archivo temporal
    # Volver a abrir el PDF comprimido
    with open('/tmp/compressed.pdf', 'rb') as f:
        output_pdf = BytesIO(f.read())
    return output_pdf

class Parte(models.Model):

    maquina=models.ForeignKey(Maquina,on_delete=models.CASCADE)
    num_parte=models.IntegerField()
    codigo_parte=models.CharField(max_length=100)
    nombre=models.CharField(max_length=130) 
    descripcion=models.TextField() 
    mantenimiento=models.TextField(null=True,blank=True)  
    foto=models.FileField(upload_to="images_partes/",null=True,blank=True)    
    anexo=models.FileField(upload_to="archivos_partes/",null=True,blank=True)
    
    def save_foto(self, *args, **kwargs):
        if self.foto:
            extension = self.foto.name.split('.')[-1]
            new_filename = f"{self.codigo_parte}_{self.nombre}.{extension}"
            new_file_path = f"{new_filename}"

            # Redimensionar la imagen antes de guardarla
            resized_image = resize_image(self.foto)

            # Asignar la imagen redimensionada al campo foto sin llamar a self.foto.save()
            self.foto.delete(save=False)
            self.foto = ContentFile(resized_image.read(), new_file_path)

    def save_link(self):
        """Método para procesar el campo 'link' (comprimir el archivo PDF y cambiar su nombre)"""
        if self.anexo:
            # Verificar que el archivo sea un PDF y esté presente
            if self.anexo.name.endswith('.pdf'):
                with self.anexo.open('rb') as f:
                    compressed_pdf = compress_pdf(f)
                
                # Crear un nuevo nombre para el archivo PDF basado en 'codigo' y 'nombre'
                new_file_name = f"{self.codigo_parte}_{self.nombre}.pdf"
                new_file_path = f"{new_file_name}"

                # Eliminar el archivo anterior
                self.anexo.delete(save=False)  # Eliminar el archivo anterior

                # Guardar el archivo comprimido con el nuevo nombre
                self.anexo = ContentFile(compressed_pdf.read(), name=new_file_path)

    def save(self, *args, **kwargs):
        self.save_foto()  # Procesar el campo 'foto' (si es una imagen)
        self.save_link()  # Procesar el campo 'link' (si es un PDF)
        
        super(Parte, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    




