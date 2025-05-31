from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='book_images/', blank=True)
    file = models.FileField(upload_to='ebooks/', blank=True)

    def __str__(self):
        return self.title
