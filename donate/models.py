from django.db import models
from django.contrib.auth.models import User
class Ngo(models.Model):
    ngo_name = models.CharField(max_length=200)
    ngo_website = models.URLField(max_length=200,default=None)
    ngo_aim = models.CharField(max_length=250)
    ngolocation = models.TextField()
    ngostate = models.CharField(max_length=80,default =None)
    ngopincode = models.CharField(max_length=50,default =None)
    associated = models.TextField()
    ngo_head  = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=50)
    ngo_email = models.EmailField(max_length=254)
    ngo_whatsapp = models.CharField(max_length=50)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default = False)
class BookDonater(models.Model):
    bookname = models.CharField(max_length=150,default=None)
    publisher_detail = models.TextField(default=None)
    authorname = models.CharField(max_length=100,default=None)
    isbn = models.CharField(max_length=50,default=0)
    bookphoto = models.ImageField(upload_to="images/",default=None)
    donarname = models.CharField(max_length=70,default=None)
    donarphone = models.CharField(max_length=13,default=None)
    donarwhatsapp = models.CharField(max_length=50,default=None)
    donaremail= models.EmailField(max_length=254,default=None)
    donaraddress = models.CharField(max_length=100,default=None)
    donarcity = models.CharField(max_length=100,default=None)
    donar_pincode = models.CharField(max_length = 20,default=None)
    donarstate = models.CharField(max_length=50,default=None)
    acc_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default = False)

    def __str__(self):
        return self.donarname
class IndiDonar(models.Model):
    donarname = models.CharField(max_length=70,default=None)
    donarphone = models.CharField(max_length=13,default=None)
    donarwhatsapp = models.CharField(max_length=50,default=None)
    donaremail= models.EmailField(max_length=254,default=None)
    donaraddress = models.CharField(max_length=100,default=None)
    donarcity = models.CharField(max_length=100,default=None)
    donar_pincode = models.CharField(max_length = 20,default=None)
    donarstate = models.CharField(max_length=50,default=None)
    bookname = models.CharField(max_length=150,default=None)
    isbn = models.CharField(max_length=50,default=0)
    authorname = models.CharField(max_length=100,default=None)
    acc_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    publisher_detail = models.TextField(default=None)
    genre = models.CharField(max_length=50,default=None)
    board = models.CharField(max_length=50,blank=True,default="cbse")
    bookphoto = models.ImageField(upload_to="images/",default=None)
    pub_date = models.DateTimeField(auto_now_add=True)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default = False)
    def book_name(self):
        return self.bookname[:]
    def __str__(self):
        return self.donarname
    def pub_date_preety(self):
        return self.pub_date.strftime('%b %e %Y')
    def publisher(self):
        return self.publisher_detail[:]
    def author(self):
        return self.authorname[:]
    def donar_city(self):
        return self.donarcity[:]
    

