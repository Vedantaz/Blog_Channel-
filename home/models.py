from django.db import models

# Create your models here.

# database == excel workbook
# models in django == database table == excel sheet

class Contact(models.Model):
    # // primary_ket = True : automatically increment krega ., uniquly identify it ,.jango automatically configure it ,
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    content = models.TextField()

    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "Message from " + self.name + '-' + self.email
