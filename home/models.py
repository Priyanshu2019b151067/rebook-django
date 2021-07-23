from django.db import models


class Complaint(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    subject = models.CharField(max_length=50)
    message = models.TextField()

    


