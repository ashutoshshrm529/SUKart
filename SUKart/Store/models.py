from django.db import models

from PIL import Image


class Company(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(default='product-images/default.jpeg', upload_to='product-images')
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > img.width:
            img = img.crop((0, ((img.height-img.width)/2), img.width, ((img.height+img.width)/2)))
        else:
            img = img.crop((((img.width-img.height)/2), 0,
                            ((img.width+img.height)/2), img.height))

        img.save(self.image.path)
