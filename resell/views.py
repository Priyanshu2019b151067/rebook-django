from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
import uuid
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.
@login_required(login_url='account_login')
def enlist_book(request):

    if request.method == "POST":
        bookname =request.POST['bookname']
        bookname= bookname.lower()
        isbn = request.POST['isbn']
        bookpublisher = request.POST['bookpublisher']
        bookpublisher = bookpublisher.lower()
        bookauthor = request.POST['bookauthor']
        bookauthor = bookauthor.lower()
        offeredprice = request.POST['offeredprice']
        actualprice = request.POST['actualprice']
        offered = request.POST['offered']
        genre = request.POST['genre']
        genre = genre.lower()
        if not request.POST.get('board',False):
            board = "cbse"
        else:
            board = request.POST.get('board',False).lower()
        reseller_name = request.POST['reseller_name']
        reseller_name = reseller_name.lower()
        reseller_contact = request.POST['reseller_contact']
        reseller_whatsapp = request.POST['reseller_whatsapp']
        reseller_address = request.POST['reseller_address']
        reseller_city = request.POST['reseller_city']
        reseller_city = reseller_city.lower()
        reseller_pincode = request.POST['reseller_pincode']
        reseller_state = request.POST['reseller_state']
        reseller_state = reseller_state.lower()
        book_photo = request.FILES['book_photo']
        acc_holder = request.user
        seller = Seller.objects.filter(bookname = bookname,reseller_name = reseller_name,reseller_contact = reseller_contact).exists()
        if seller:
                messages.success(request,"Your Book has been already registered for resell")
                return redirect("enlist_book")
        seller_obj = Seller(bookname=bookname,board=board,actualprice = actualprice ,bookpublisher=bookpublisher,bookauthor=bookauthor,offeredprice=offeredprice,offered = offered,genre=genre,reseller_contact=reseller_contact,reseller_whatsapp=reseller_whatsapp,reseller_address=reseller_address,reseller_city=reseller_city,reseller_pincode=reseller_pincode,reseller_state=reseller_state,
            isbn = isbn,
            acc_holder = acc_holder,
            reseller_name=reseller_name,
            book_photo=book_photo)
        seller_obj.save()
        messages.success(request,"Your Book has been successfully registered for resell")
        return redirect("buy_book")
    return render(request,'resell/enlist_book.html')
def buy_book(request):
    books = Seller.objects.all().order_by('-id')[:12]
    return render(request,'resell/buy_book.html',{'books':books})

#####################################################IMPORTANT FUNCTIONS################################################


def location(request):
    query1 = request.GET.get('q').lower()
    genre = request.GET.get('g').lower()
    bs = request.GET.get('bs')
    if query1 == "cbse" or query1 == "delhi-board" or query1 =="icse" or query1 =="other-board" or query1 == "up-board":
        if request.method=="POST":
            reseller_city =request.POST['search'].lower()
            if not Seller.objects.filter(reseller_city = reseller_city,genre=genre,board = query1,bookname__iexact=bs).exists():
                messages.success(request,"This book is not available at this location")
            books = Seller.objects.all().filter(genre=genre,board = query1,reseller_city = reseller_city,bookname__iexact=bs).order_by('-id')
    else:
        if request.method=="POST":
            reseller_city =request.POST['search'].lower()
            if not Seller.objects.filter(reseller_city = reseller_city,genre=genre,bookname__iexact=bs).exists():
                messages.success(request,"This book is not available at this location")
            books = Seller.objects.all().filter(genre=genre,reseller_city = reseller_city,bookname__iexact=bs).order_by('-id')
    return render(request,'resell/Location.html',{"books":books,"q":query1,"g":genre,"bs":bs})

def search(request):
    query1 = request.GET.get('q').lower()
    genre = request.GET.get('g').lower()
    books = dict()
    # playschool - XII
    if query1 == "cbse" or query1 == "delhi-board" or query1 =="icse" or query1 =="other-board" or query1 == "up-board":
        if request.method=="GET":
            bs = request.GET.get('bs')
            if Seller.objects.filter(bookname__iexact = bs,board=query1,genre=genre).exists():
                books = Seller.objects.all().filter(bookname__iexact = bs,board=query1,genre=genre)
            elif Seller.objects.filter(bookauthor__iexact = bs,board=query1,genre=genre).exists():
                books = Seller.objects.all().filter(bookauthor__iexact=bs,board=query1,genre=genre)
            elif Seller.objects.filter(isbn = bs,board=query1,genre=genre).exists():
                books = Seller.objects.all().filter(isbn = bs,board=query1,genre=genre)
            else:
                messages.success(request,"Book with this specification doesnot exist")
        if request.method=="POST":
            bs=request.POST['bs'].lower()
            if Seller.objects.filter(bookname = bs,board=query1,genre=genre).exists():
                books = Seller.objects.all().filter(bookname__iexact = bs,board=query1,genre=genre)
            elif Seller.objects.filter(bookauthor__iexact = bs,board=query1,genre=genre).exists():
                books = Seller.objects.all().filter(bookauthor__iexact=bs,board=query1,genre=genre)
            elif Seller.objects.filter(isbn = bs,board=query1,genre=genre).exists():
                books = Seller.objects.all().filter(isbn = bs,board=query1,genre=genre)
            else:
                messages.success(request,"Book with this specification doesnot exist")
# Competitive
    else:
        if request.method=="GET":
            bs = request.GET.get('bs')
            if Seller.objects.filter(bookname__iexact = bs,genre=genre).exists():
                books = Seller.objects.all().filter(bookname__iexact = bs,genre=genre)
            elif Seller.objects.filter(bookauthor__iexact = bs,genre=genre).exists():
                books = Seller.objects.all().filter(bookauthor__iexact=bs,genre=genre)
            elif Seller.objects.filter(isbn = bs,genre=genre).exists():
                books = Seller.objects.all().filter(isbn = bs,genre=genre)
            else:
                messages.success(request,"Book with this specification doesnot exist")
        if request.method=="POST":
            bs=request.POST['bs'].lower()
            if Seller.objects.filter(bookname = bs,genre = genre).exists():
                books = Seller.objects.all().filter(bookname__iexact = bs,genre=genre)
            elif Seller.objects.filter(bookauthor__iexact = bs,genre = genre).exists():
                books = Seller.objects.all().filter(bookauthor__iexact=bs,genre=genre)
            elif Seller.objects.filter(isbn = bs,genre = genre).exists():
                books = Seller.objects.all().filter(isbn = bs,genre=genre)
            else:
                messages.success(request,"Book with this specification doesnot exist")
    return render(request,f'resell/Search.html',{"books":books,"q":query1,"g":genre,"bs":bs})


def all_rounder(request):
    query1 = request.GET.get('q').lower()
    genre = request.GET.get('g').lower() 
    location = None
    if query1 == "cbse" or query1 == "delhi-board" or query1 =="icse" or query1 =="other-board" or query1 == "up-board":
        if not Seller.objects.filter(genre=genre,board = query1).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre,board = query1).order_by('-id')
        location = "school"
    if query1 =="entrance" or query1 =="government" or query1 == "junior":
        location = "competitive"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="first" or query1 == "second" or query1 =="third" or query1 =="fourth":
        location ="engineering"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="medical" :
        location ="medical"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id') 
    if query1 == "bsc_first" or query1 == "bsc_second" or query1 =="bsc_third":
        location ="bsc"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "be_first" or query1 == "be_second" or query1 =="be_third" or query1 =="be_fourth":
        location ="be"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "bca_first" or query1 =="bca_second" or query1 =="bca_third":
        location ="bca"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "msc_first" or query1 =="msc_second":
        location ="msc"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "mtech_first" or query1 =="mtech_second":
        location ="mtech"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bams_first" or query1 == "bams_second" or query1 == "bams_third" or query1 =="bams_fourth" or query1 =="bams_fifth":
        location ="bams"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bhms_first" or query1 =="bhms_second" or query1 =="bhms_third" or query1 =="bhms_fourth" or query1 =="bhms_fifth":
        location = "bhms"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bums_first" or query1 =="bums_second" or query1 =="bums_third" or query1 =="bums_fourth" or query1 =="bums_fifth":
        location = "bums"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="ba_first" or query1 =="ba_second" or query1 =="ba_third":
        location = "ba"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bfa_first" or query1 =="bfa_second" or query1 =="bfa_third":
        location = "bfa"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bba_first" or query1 =="bba_second" or query1 =="bba_third":
        location = "bba"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bllb_first" or query1 =="bllb_second" or query1 =="bllb_third" or query1 =="bllb_fourth" or query1 =="bllb_fifth":
        location = "bllb"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bjm_first" or query1 =="bjm_second" or query1 =="bjm_third":
        location = "bjm"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bhm_first" or query1 =="bhm_second" or query1 =="bhm_third" or query1 =="bhm_fourth":
        location = "bhm"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bcom_first" or query1 =="bcom_second" or query1 =="bcom_third":
        location = "bcom"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bld_first" or query1 =="bld_second" or query1 =="bld_third" or query1 =="bld_fourth" or query1 =="bld_fifth":
        location ="bld"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="llb_first" or query1 =="llb_second" or query1 =="llb_third":
        location ="llb"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')       
    if query1 =="ca_first" or query1 =="ca_second" or query1 =="ca_third" or query1 =="ca_fourth" or query1 =="ca_fifth":
        location ="ca"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="cs_first":
        location ="cs"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="cma_first" or query1 =="cma_second" or query1 =="cma_third" or query1 =="cma_fourth":
        location ="cma"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="cfp_first":
        location = "cfp"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="mcom_first" or query1 =="mcom_second":
        location = "mcom"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="mba_first" or query1 =="mba_second":
        location ="mba"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="sanskrit" or query1 =="hindi" or query1 =="english" or query1 =="french" or query1=="language_others":
        location ="Language"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1=="astrology" or query1 =="business" or query1=="health" or query1 =="history" or query1 =="sports" or query1 =="fiction_other":
        location ="fiction"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="magazine" or query1 =="comicbooks" or query1 =="storybook" or query1 =="poembook" or query1 =="entertainment_others":
        location = "entertainment"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="self_help" or query1 =="spirituality" or query1 =="sh_others":
        location = "selfh"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="finance" or query1 =="economy" or query1 =="feo":
        location = "finance"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bed_first" or query1 =="bed_second":
        location = "bed"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="btc_first" or query1 =="btc_second":
        location ="btc" 
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="other_other":
        location ="other"
        if not Seller.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = Seller.objects.all().filter(genre=genre).order_by('-id')
    paginator = Paginator(books,15,orphans=3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,f'resell/{location}/{query1}/{genre}.html',{"books":page_obj})
def mainsearch(request):
    if request.method == "GET":
        bs = request.GET.get('bs')
        if Seller.objects.filter(bookname = bs).exists():
            books = Seller.objects.all().filter(bookname__iexact = bs)
        elif Seller.objects.filter(bookauthor = bs).exists():
            books = Seller.objects.all().filter(bookauthor__iexact=bs)
        elif Seller.objects.filter(isbn = bs).exists():
            books = Seller.objects.all().filter(isbn = bs)
        else:
            messages.success(request,"Book with this specification doesnot exist")
            return redirect('buy_book')
        return render(request,'resell/Search_Main.html',{"books":books,"bs":bs})

    if request.method=="POST":
        bs=request.POST['bs'].lower()
        if Seller.objects.filter(bookname = bs).exists():
            books = Seller.objects.all().filter(bookname__iexact = bs)
        elif Seller.objects.filter(bookauthor = bs).exists():
            books = Seller.objects.all().filter(bookauthor__iexact=bs)
        elif Seller.objects.filter(isbn = bs).exists():
            books = Seller.objects.all().filter(isbn = bs)
        else:
            messages.success(request,"Book with this specification doesnot exist")
            return redirect('buy_book')
    return render(request,'resell/Search_Main.html',{"books":books,"bs":bs})


def searchlocation(request,bs):    
    books = dict()
    if request.method == "POST":
        city = request.POST['search'].lower()
        if Seller.objects.filter(bookname = bs,reseller_city =city).exists():
            books = Seller.objects.all().filter(bookname__iexact = bs,reseller_city =city)
        elif Seller.objects.filter(bookauthor = bs,reseller_city =city).exists():
            books = Seller.objects.all().filter(bookauthor__iexact=bs,reseller_city =city)
        elif Seller.objects.filter(isbn = bs,reseller_city =city).exists():
            books = Seller.objects.all().filter(isbn = bs,reseller_city =city)
        else:
            messages.success(request,"Book with this specification doesnot exist")
    return render(request,'resell/Searchlocation.html',{"books":books,"bs":bs})
def delete_view(request,reseller_name,bookname):
    if request.method=="POST":
        if request.POST.get('delete1',False)=="Yes":
            obj = Seller.objects.filter(bookname__iexact=bookname).filter(reseller_name__iexact=reseller_name)
            obj.delete()
        return redirect("profile")
    return render(request,'resell/delete.html')

def details(request,reseller_name,bookname):
    obj = Seller.objects.filter(bookname__iexact=bookname,reseller_name__iexact=reseller_name).first()
    q = request.GET.get('q')
    m = request.GET.get('m')
    p = request.GET.get('p')
    x = False
    if m  and  p  is not None:
        x = True
        s = "category"
        return render(request,'resell/book_Detail_Page.html',{"book":obj,"q":m,"g":p,"s":s,"x":x})
    if q is None:
        q = 'buy_book'
    return render(request,'resell/book_Detail_Page.html',{"book":obj,"q":q,"x":x})

def error(request):
    return render(request,'resell/error.html')
