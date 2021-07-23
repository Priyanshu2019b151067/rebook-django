from django.shortcuts import render
from django.core.mail import send_mail
from .models import Complaint
from donate.models import *
from django.conf import settings
from resell.models import *
from accounts.models import Profiles
from django.contrib.auth.models import User
# Create your views here.
def home_view(request):
    ngo_count = Ngo.objects.all().count()
    ngo_donated =  IndiDonar.objects.all().count()
    ads = Seller.objects.all().count()
    users = User.objects.all().count()
    books = Seller.objects.all().order_by('-id')[:8]
    indi = IndiDonar.objects.all().filter(is_verified=True).order_by('-id')[:8]
    return render(request,'index.html',{"ngo_count":ngo_count,"ngo_donated":ngo_donated,"ads":ads,"users":users,"books":books,"indi":indi})
def about_view(request):
    return render(request,'home/about.html')
def privacy_view(request):
    return render(request,'home/privacy.html')
def terms_view(request):
    return render(request,'home/terms.html')
def contact_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        com = Complaint(name=name,email=email, subject=subject, message=message )
        com.save()
        send_mail("Complaint or Query",f"{name} \nsubject = {subject} \nquery = {message}",settings.EMAIL_HOST_USER,['rebookcompany2000@gmail.com'])
        res = "Thank you for contacting us we will answer to your query as soon as possible"
    else:
        res = False
    return render(request,'home/contact.html',{"res":res})
def profile(request):
    current = request.user
    userobj = User.objects.get(username = current)
    profile_obj = Profiles.objects.get(user = userobj)
    created_at = profile_obj.pub_date
    books = Seller.objects.all().filter(acc_holder = current).order_by('-id')
    sell_post = Seller.objects.all().filter(acc_holder = current).count()
    indi = IndiDonar.objects.all().filter(is_verified=True,acc_holder = current).order_by('-id')
    don_post = IndiDonar.objects.all().filter(is_verified=True,acc_holder = current).count()
    return render(request,'home/profile.html',{"books":books,"indi":indi,"sell_post" :sell_post,"don_post":don_post,"created_at":created_at})