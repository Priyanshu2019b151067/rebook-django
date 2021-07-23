from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Seller(models.Model):
    bookname = models.CharField(max_length=150)
    pub_date = models.DateTimeField(auto_now_add=True)
    bookpublisher = models.CharField(max_length=150)
    bookauthor = models.CharField(max_length=150)
    isbn = models.CharField(max_length=100,blank=True,default="xxxxxxxxxxxxx")
    offeredprice = models.IntegerField(default = 0)
    actualprice=models.IntegerField(default=0)
    offered = models.CharField(max_length=50)
    genre = models.CharField(max_length=200)
    board = models.CharField(max_length=50,blank=True)
    acc_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    reseller_name = models.CharField(max_length=50,default ="seller")
    reseller_contact = models.CharField(max_length=50)
    reseller_whatsapp = models.CharField(max_length=50)
    reseller_address = models.TextField()
    reseller_city = models.CharField(max_length=100)
    reseller_pincode = models.IntegerField()
    reseller_state = models.CharField(max_length=100)
    book_photo = models.ImageField(upload_to='images/')
    def book_name(self):
        return self.bookname[:]
    def publisher(self):
        return self.bookpublisher[:]
    def author(self):
        return self.bookauthor[:]
    def resellercity(self):
        return self.reseller_city[:]