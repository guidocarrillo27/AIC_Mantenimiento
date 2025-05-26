from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Maquina

@receiver(pre_save, sender=Maquina)
def compress_image(sender, instance, **kwargs):
    if instance.foto:
        image = Image.open(instance.foto)
        # Reducir el tamaño de la imagen, aquí puedes cambiar el tamaño según tus necesidades
        image = image.convert("RGB")
        image.thumbnail((800, 800))  # Cambiar el tamaño máximo de la imagen
        # Guardar la imagen comprimida
        img_io = BytesIO()
        image.save(img_io, format='JPEG', quality=85)  # Controla la calidad (85 es un buen equilibrio)
        img_io.seek(0)
        instance.foto = InMemoryUploadedFile(img_io, 'ImageField', instance.foto.name, 'image/jpeg', img_io.tell(), None)
