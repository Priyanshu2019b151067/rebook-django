from django.shortcuts import render,redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from usernames import is_safe_username
from django.contrib.auth import authenticate,login
from .models import BookDonater,Ngo,IndiDonar
from django.core.paginator import Paginator
import uuid
import re
# NGO DONATING BOOKS 
@login_required
def book_donater_view(request,ngo_name):
    nge =Ngo.objects.filter(ngo_name=ngo_name).first()
    ngo_name = nge.ngo_name
    print(ngo_name)
    if request.method =="POST":
        # donarname
        donarname = request.POST['donarname']
        # donarphone
        donarphone = request.POST['donarphone']
        if phone_number(donarphone):
            # donarwhatsapp
            donarwhatsapp = request.POST['donarwhatsapp']
            if phone_number(donarwhatsapp):
                # donaremail
                donaremail = request.POST['donaremail']
                if check(donaremail):
                    # donarcity
                    donarcity = request.POST['donarcity'].lower()
                    # donar_pincode
                    donar_pincode = request.POST['donar_pincode']
                    # donaraddress
                    donaraddress = request.POST['donaraddress']
                    if valid_pincode(donar_pincode):
                        # donarstate
                        donarstate = request.POST['donarstate'].lower()
                        # bookname
                        bookname = request.POST['bookname'].lower()
                        # authorname
                        authorname = request.POST['authorname'].lower()
                        # isbn 
                        isbn = request.POST['isbn']
                        if isbn_checker(isbn):
                            qs = (BookDonater.objects.filter(donarname__icontains=donarname).first() and BookDonater.objects.filter(authorname__icontains=authorname).first() and BookDonater.objects.filter(isbn__icontains=isbn).first())
                            if qs:
                                messages.warning(request,"Book already listed")
                                return redirect(f'/donate/{ngo_name}/')
                            # publisher_detail
                            publisher_detail = request.POST['publisher_detail'].lower()
                            # auth_token
                            auth_token = str(uuid.uuid4())
                            # bookphoooto
                            bookphoto = request.FILES['bookphoto']
                            send_donar_mail(donaremail,auth_token,ngo_name)
                            acc_holder = request.user
                            donar = BookDonater(donarname = donarname,
                            isbn = isbn,
                            donaraddress =donaraddress,
                            acc_holder =acc_holder ,auth_token = auth_token,
                            donarphone=donarphone,donarwhatsapp=donarwhatsapp,
                            donarcity =donarcity,donaremail=donaremail,
                            donar_pincode=donar_pincode,donarstate=donarstate,
                            bookname=bookname,authorname=authorname,
                            publisher_detail= publisher_detail,
                            bookphoto=bookphoto)
                            donar.save()
                            messages.warning(request,"Verify the link send at your email")
                            return redirect(f'/donate/{ngo_name}/')
                    else:
                        messages.warning(request,"Pincode not valid")
                        return redirect(f'/donate/{ngo_name}/')
                            
                else:
                    messages.warning(request,"Enter correct email details")
                    return redirect(f'/donate/{ngo_name}/')
                        
            else:
                messages.warning(request,"whatsapp number is incorrect")
                return redirect(f'/donate/{ngo_name}/')
                    
        else:
            messages.warning(request,"Contact number is incorrect")
            return redirect(f'/donate/{ngo_name}/')    
    return render(request,'donate/enlist_book.html')
#####################################################################################################
# INDIVIDUAL DONAR 
@login_required
def list_for_donation(request):
    if request.method =="POST":
        donarname = request.POST['donarname'].lower()
        donarphone = request.POST['donarphone']
        if phone_number(donarphone):
            donarwhatsapp = request.POST['donarwhatsapp']
            if phone_number(donarwhatsapp):
                donaremail = request.POST['donaremail']
                if check(donaremail):
                    donarcity = request.POST['donarcity'].lower()
                    donaraddress = request.POST['donaraddress']
                    donar_pincode = request.POST['donar_pincode']
                    if valid_pincode(donar_pincode):
                        donarstate = request.POST['donarstate'].lower()
                        bookname = request.POST['bookname'].lower()
                        authorname = request.POST['authorname'].lower()
                        publisher_detail = request.POST['publisher_detail'].lower()
                        genre = request.POST['genre'].lower()
                        if not request.POST.get('board',False):
                            board = "cbse"
                        else:
                            board = request.POST.get('board',False).lower()
                        isbn = request.POST['isbn']
                        if isbn_checker(isbn):
                            qs = (IndiDonar.objects.filter(donarname__icontains=donarname).first() and IndiDonar.objects.filter(authorname__icontains=authorname).first() and IndiDonar.objects.filter(isbn__icontains=isbn).first())
                            if qs:
                                messages.warning(request,"Book already listed")
                                return redirect('listdonation')
                            auth_token = str(uuid.uuid4())
                            bookphoto = request.FILES['bookphoto']
                            send_verification_mail(donaremail,auth_token)
                            acc_holder = request.user
                            donar = IndiDonar(donarname = donarname,
                            donarphone=donarphone,
                            donarwhatsapp=donarwhatsapp,
                            donaremail=donaremail,
                            donaraddress =donaraddress,
                            donarcity =donarcity,
                            donar_pincode=donar_pincode,
                            donarstate=donarstate,
                            bookname=bookname,
                            isbn =isbn,
                            authorname=authorname,
                            acc_holder=acc_holder,
                            publisher_detail= publisher_detail,
                            genre = genre,
                            board = board,
                            bookphoto=bookphoto,
                            auth_token = auth_token,
                            )
                            donar.save()
                            messages.warning(request,"Verify the link send at your email")
                            return redirect('listdonation')
                        else:
                            messages.warning(request,"Enter correct isbn number")
                            return redirect('listdonation')
                    else:
                        messages.warning(request,"Pincode not valid")
                        return redirect('listdonation')
                            
                else:
                    messages.warning(request,"Enter correct email details")
                    return redirect('listdonation')
                        
            else:
                messages.warning(request,"whatsapp number is incorrect")
                return redirect('listdonation')
                    
        else:
            messages.warning(request,"Contact number is incorrect")
            return redirect('listdonation')   
    return render(request,'donate/indi_donate.html')


##################################################################################################


# NGO LISTING DONATE PAGE
def donate_home(request):
    ngos = Ngo.objects.all().filter(is_verified = True)
    return render(request,'donate/donate.html',{'ngos':ngos})

# Creating NGO Function 
def create_ngo(request):
    if request.method == "POST":

        ngo_name = request.POST['ngo_name']
        ngo_email = request.POST['ngo_email']
        ngo_obj = Ngo.objects.filter(ngo_email=ngo_email).first()
        if ngo_obj:
            messages.warning(request, 'Ngo is already listed.')
            return redirect("create_ngo")
        ngo_aim = request.POST['ngo_aim']
        ngo_website = request.POST['ngo_website']
        ngolocation = request.POST['ngolocation']
        ngostate = request.POST['ngostate']
        ngopincode = request.POST['ngopincode']
        associated = request.POST['associated']
        ngo_head = request.POST['ngo_head']
        phone_num = request.POST['phone_num']
        ngo_whatsapp = request.POST['ngo_whatsapp']
        auth_token = str(uuid.uuid4())
        send_verification_mail(ngo_email,auth_token)
        ngo = Ngo(ngo_name=ngo_name,
        ngo_aim=ngo_aim,
        ngo_website=ngo_website,ngolocation=ngolocation,ngostate=ngostate,ngopincode=ngopincode,associated=associated,ngo_head=ngo_head,phone_num=phone_num,ngo_email=ngo_email,ngo_whatsapp=ngo_whatsapp,auth_token = auth_token )
        ngo.save()
        email_from = settings.EMAIL_HOST_USER
        send_mail(
           "Account Creation Request",
           'Ngo signup request from ' + ngo_name +
           "\nLocation :" + ngolocation + 
           "\nPincode :" + ngopincode +
           "\nState :" + ngostate+

           "\nEmail :"+ ngo_email + 
           "\nWebsite :" + ngo_website+
           "\nngo whatsapp number :" + ngo_whatsapp,
           email_from,
           ['rebookcompany2000@gmail.com']
        )

        res = True
    else:
        res = False
    return render(request,'donate/create_ngo.html',{"res":res})

##########################################################################################################
# VERIFICATION ROUTES OF NGO AND INDIVIDUAL DONATER
def verify(request,auth_token):
    ngo_obj=Ngo.objects.filter(auth_token=auth_token).first()
    indi = IndiDonar.objects.filter(auth_token=auth_token).first()
    if ngo_obj:
        if ngo_obj.is_verified:
            messages.success(request,"Account Already Verified")
            return redirect("success")
        ngo_obj.is_verified = True
        ngo_obj.save()
        messages.success(request,"Account is been verified. \nThank you for registering❤.\n\nTEAM REBOOK")
        return redirect("success")
    if indi:
        if indi.is_verified:
            messages.success(request,"Listing Already Verified")
            return redirect("available_books")
        indi.is_verified = True
        indi.save()
        messages.success(request,"Listing is been verified.\nThank you for Donating❤.\n\nTEAM REBOOK")
        return redirect("available_books")
    else:
        messages.success(request,"Listing doesnot verified yet\n\nTEAM REBOOK")
        return redirect("success")




# VERIFY DONATER TO NGO
def verify_donar(request,ngo_name,auth_token):
    ngo = Ngo.objects.filter(ngo_name = ngo_name).first()
    do = BookDonater.objects.filter(auth_token =auth_token).first()
    if do:
        if do.is_verified:
            messages.success(request,"Listing Already Verified")
            return redirect("success")
        do.is_verified = True
        do.save()
        messages.success(request,"Listing has been verified \n\nThank you for Donating❤\n\nNgo will contact u soon.\n\n\nTEAM REBOOK")
        send_ngo_email(auth_token,ngo.ngo_email)
        return redirect("success")
    else:
        messages.success(request,"Listing doesnot verified yet..\n\nTEAM REBOOK")
        return redirect("success")


# SUCCESS ROUTE FOR AUXILAARY USE CASE
def success(request):
    return render(request,'donate/success.html')

# VERIFICATION MAIL ROUTE 
def send_verification_mail(email,auth_token):
    email = str(email)
    subject = "Account Verification "
    message = f'Click the link to verify your account https://rebook-tech.herokuapp.com/donate/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    receiver_list = [email,]
    send_mail(subject,message,email_from,receiver_list)


def send_donar_mail(email,auth_token,ngo_name):
    subject = "Listing Verification "
    message = f'Click the link to verify your account https://rebook-tech.herokuapp.com/verify_donar/{ngo_name}/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    receiver_list = [email]
    send_mail(subject,message,email_from,receiver_list)


def send_ngo_email(auth_token,email):
    don = BookDonater.objects.filter(auth_token = auth_token).first()
    subject = "Book Donation Request "
    message = f"Hi There \nThis is to inform you that you have received a book donation request.\nDonarname - {don.donarname}.\nBook  - {don.bookname}\nPublisher - {don.publisher_detail}\nContact no. - {don.donarphone}\nwhatsapp no. - {don.donarwhatsapp}\nCity - {don.donarcity}\n\nThank you\n\nTEAM REBOOK"
    email = EmailMessage(subject, message,settings.EMAIL_HOST_USER, [str(email),settings.EMAIL_HOST_USER])
    email.content_subtype ='html'
    email.attach(don.bookphoto.name,don.bookphoto.read(),'text/plain')
    email.send()

##################################################################################################
# VALIDATION 
def phone_number(phone):
    output = False
    if re.fullmatch('^[6789]\d{9}$', phone):
        output = True
    return output
def check(email):
    output = False
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        output = True
    return output
def valid_pincode(pincode):
    output = True
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$" 
    p = re.compile(regex)
    m = re.match(p, pincode)
    if m is None:
        output = False
    return output
def isbn_checker(isbn):
    output = False
    if isbn[0] != "0" and len(isbn)==13 and isbn.isdecimal():
        output = True
    return output

# Validation ends
####################################################################################################################
# ROUTES FOR  DIFFERENT SECTION 


def available_books(request):
    books = IndiDonar.objects.all().filter(is_verified=True).order_by('-id')[:12]
    return render(request,'donate/resell/buy_book.html',{'books' :books})

def delete_page(request,donarname,bookname):
    if request.method=="POST":
        if request.POST.get('delete1',False)=="Yes":
            obj = IndiDonar.objects.filter(bookname__iexact=bookname).filter(donarname__iexact=donarname)
            obj.delete()
        return redirect("profile")
    return render(request,'donate/delete.html')

# def delete_view(request,reseller_name,bookname):
#     if request.method=="POST":
#         if request.POST.get('delete1',False)=="Yes":
#             obj = Seller.objects.filter(bookname__iexact=bookname).filter(reseller_name__iexact=reseller_name)
#             obj.delete()
#         return redirect("buy_book")
#     return render(request,'resell/delete.html')
def details(request,donarname,bookname):
    obj = IndiDonar.objects.filter(bookname__iexact=bookname,donarname__iexact=donarname).first()
    q = request.GET.get('q')
    m = request.GET.get('m')
    p = request.GET.get('p')
    x = False
    if m  and  p  is not None:
        x = True
        s = "category1"
        return render(request,'donate/book_Detail_Page.html',{"book":obj,"q":m,"g":p,"s":s,"x":x})
    if q is None:
        q='available_books'
    return render(request,'donate/book_Detail_Page.html',{"book":obj,"q":q,"x":x})

def all_rounder(request):
    # if request.GET.get('q') ==None and request.GET.get('g') == None:
    #     pager()
    query1 = request.GET.get('q').lower()
    genre = request.GET.get('g').lower() 
    location = None
    if query1 == "cbse" or query1 == "delhi-board" or query1 =="icse" or query1 =="other-board" or query1 == "up-board":
        location = "school"
        if not IndiDonar.objects.filter(genre=genre,board = query1).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre,board = query1).order_by('-id')
        # paginator = Paginator(books,3)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        
    if query1 =="entrance" or query1 =="government" or query1 == "junior":
        location = "competitive"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="first" or query1 == "second" or query1 =="third" or query1 =="fourth":
        location ="engineering"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "medical":
        location ="medical" 
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "bsc_first" or query1 == "bsc_second" or query1 =="bsc_third":
        location ="bsc"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "be_first" or query1 == "be_second" or query1 =="be_third" or query1 =="be_fourth":
        location ="be"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "bca_first" or query1 =="bca_second" or query1 =="bca_third":
        location ="bca"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "msc_first" or query1 =="msc_second":
        location ="msc"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 == "mtech_first" or query1 =="mtech_second":
        location ="mtech"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bams_first" or query1 == "bams_second" or query1 == "bams_third" or query1 =="bams_fourth" or query1 =="bams_fifth":
        location ="bams"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bhms_first" or query1 =="bhms_second" or query1 =="bhms_third" or query1 =="bhms_fourth" or query1 =="bhms_fifth":
        location = "bhms"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bums_first" or query1 =="bums_second" or query1 =="bums_third" or query1 =="bums_fourth" or query1 =="bums_fifth":
        location = "bums"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="ba_first" or query1 =="ba_second" or query1 =="ba_third":
        location = "ba"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bfa_first" or query1 =="bfa_second" or query1 =="bfa_third":
        location = "bfa"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bba_first" or query1 =="bba_second" or query1 =="bba_third":
        location = "bba"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bllb_first" or query1 =="bllb_second" or query1 =="bllb_third" or query1 =="bllb_fourth" or query1 =="bllb_fifth":
        location = "bllb"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bjm_first" or query1 =="bjm_second" or query1 =="bjm_third":
        location = "bjm"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bhm_first" or query1 =="bhm_second" or query1 =="bhm_third" or query1 =="bhm_fourth":
        location = "bhm"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bcom_first" or query1 =="bcom_second" or query1 =="bcom_third":
        location = "bcom"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bld_first" or query1 =="bld_second" or query1 =="bld_third" or query1 =="bld_fourth" or query1 =="bld_fifth":
        location ="bld"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="llb_first" or query1 =="llb_second" or query1 =="llb_third":
        location ="llb" 
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')       
    if query1 =="ca_first" or query1 =="ca_second" or query1 =="ca_third" or query1 =="ca_fourth" or query1 =="ca_fifth":
        location ="ca"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="cs_first":
        location ="cs"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="cma_first" or query1 =="cma_second" or query1 =="cma_third" or query1 =="cma_fourth":
        location ="cma"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="cfp_first":
        location = "cfp"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="mcom_first" or query1 =="mcom_second":
        location = "mcom"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="mba_first" or query1 =="mba_second":
        location ="mba"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="sanskrit" or query1 =="hindi" or query1 =="english" or query1 =="french" or query1=="language_others":
        location ="Language"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1=="astrology" or query1 =="business" or query1=="health" or query1 =="history" or query1 =="sports" or query1 =="fiction_other":
        location ="fiction"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="magazine" or query1 =="comicbooks" or query1 =="storybook" or query1 =="poembook" or query1 =="entertainment_others":
        location = "entertainment"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="self_help" or query1 =="spirituality" or query1 =="sh_others":
        location = "selfh"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="finance" or query1 =="economy" or query1 =="feo":
        location = "finance"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="bed_first" or query1 =="bed_second":
        location = "bed"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="btc_first" or query1 =="btc_second":
        location ="btc" 
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
    if query1 =="other_other":
        location ="other"
        if not IndiDonar.objects.filter(genre= genre).exists():
            messages.success(request,"Book is not available in this section")
        books = IndiDonar.objects.all().filter(genre=genre).order_by('-id')
          # paginator = Paginator(books,3)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    paginator = Paginator(books,15,orphans=3)
    # paginator = Paginator(books,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,f'donate/resell/{location}/{query1}/{genre}.html',{"books":page_obj})

def mainsearch(request):
    if request.method=="POST":
        bs=request.POST['bs'].lower()
        if IndiDonar.objects.filter(bookname = bs).exists():
            books = IndiDonar.objects.all().filter(bookname__iexact = bs).order_by('id')
        elif IndiDonar.objects.filter(authorname = bs).exists():
            books = IndiDonar.objects.all().filter(authorname__iexact=bs).order_by('id')
        elif IndiDonar.objects.filter(isbn = bs).exists():
            books = IndiDonar.objects.all().filter(isbn = bs).order_by('id')
        else:
            messages.success(request,"Book with this specification doesnot exist")
            return redirect('available_books')
        # paginator = Paginator(books,2)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        return render(request,'donate/resell/Search_Main.html',{"books":books,"bs":bs})
    if request.method == "GET":
        bs = request.GET.get('bs')
        if IndiDonar.objects.filter(bookname = bs).exists():
            books = IndiDonar.objects.all().filter(bookname__iexact = bs).order_by('id')
        elif IndiDonar.objects.filter(authorname = bs).exists():
            books = IndiDonar.objects.all().filter(authorname__iexact=bs).order_by('id')
        elif IndiDonar.objects.filter(isbn = bs).exists():
            books = IndiDonar.objects.all().filter(isbn = bs).order_by('id')
        else:
            messages.success(request,"Book with this specification doesnot exist")
            return redirect('available_books')
        # paginator = Paginator(books,2)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        return render(request,'donate/resell/Search_Main.html',{"books":books,"bs":bs})   
   

def searchlocation(request,bs):    
    books = dict()
    if request.method == "POST":
        city = request.POST['search'].lower()
        if IndiDonar.objects.filter(bookname = bs,donarcity =city).exists():
            books = IndiDonar.objects.all().filter(bookname__iexact = bs,donarcity =city)
        elif IndiDonar.objects.filter(authorname = bs,donarcity =city).exists():
            books = IndiDonar.objects.all().filter(authorname__iexact=bs,donarcity =city)
        elif IndiDonar.objects.filter(isbn = bs,donarcity =city).exists():
            books = IndiDonar.objects.all().filter(isbn = bs,donarcity =city)
        else:
            messages.success(request,"Book with this specification doesnot exist")
    return render(request,'donate/resell/Searchlocation.html',{"books":books,"bs":bs})

# def details(request,donar_name,bookname):
#     obj = Seller.objects.filter(bookname__iexact=bookname,donar_name__iexact=reseller_name).first()
#     return render(request,'resell/book_Detail_Page.html',{"book":obj})



def location(request):
    query1 = request.GET.get('q').lower()
    genre = request.GET.get('g').lower()
    bs = request.GET.get('bs')
    if query1 == "cbse" or query1 == "delhi-board" or query1 =="icse" or query1 =="other-board" or query1 == "up-board":
        if request.method=="POST":
            donarcity =request.POST['search'].lower()
            if not IndiDonar.objects.filter(donarcity = donarcity,genre=genre,board = query1,bookname__iexact=bs).exists():
                messages.success(request,"This book is not available at this location")
            books = IndiDonar.objects.all().filter(genre=genre,board = query1,donarcity = donarcity,bookname__iexact=bs).order_by('-id')
    else:
        if request.method=="POST":
            donarcity =request.POST['search'].lower()
            if not IndiDonar.objects.filter(donarcity = donarcity,genre=genre,bookname__iexact=bs).exists():
                messages.success(request,"This book is not available at this location")
            books = IndiDonar.objects.all().filter(genre=genre,donarcity = donarcity,bookname__iexact=bs).order_by('-id')
    return render(request,'donate/resell/Location.html',{"books":books,"q":query1,"g":genre,"bs":bs})

def search(request):
    query1 = request.GET.get('q').lower()
    genre = request.GET.get('g').lower()
    books = dict()
    # playschool - XII
    if query1 == "cbse" or query1 == "delhi-board" or query1 =="icse" or query1 =="other-board" or query1 == "up-board":
        if request.method=="GET":
            bs = request.GET.get('bs')
            if IndiDonar.objects.filter(bookname__iexact = bs,board=query1,genre=genre).exists():
                books = IndiDonar.objects.all().filter(bookname__iexact = bs,board=query1,genre=genre)
            elif IndiDonar.objects.filter(bookauthor__iexact = bs,board=query1,genre=genre).exists():
                books = IndiDonar.objects.all().filter(authorname__iexact=bs,board=query1,genre=genre)
            elif IndiDonar.objects.filter(isbn = bs,board=query1,genre=genre).exists():
                books = IndiDonar.objects.all().filter(isbn = bs,board=query1,genre=genre)
            else:
                messages.success(request,"Book with this specification doesnot exist")
        if request.method=="POST":
            bs=request.POST['bs'].lower()
            if IndiDonar.objects.filter(bookname = bs,board=query1,genre=genre).exists():
                books = IndiDonar.objects.all().filter(bookname__iexact = bs,board=query1,genre=genre)
            elif IndiDonar.objects.filter(authorname__iexact = bs,board=query1,genre=genre).exists():
                books = IndiDonar.objects.all().filter(authorname__iexact=bs,board=query1,genre=genre)
            elif IndiDonar.objects.filter(isbn = bs,board=query1,genre=genre).exists():
                books = IndiDonar.objects.all().filter(isbn = bs,board=query1,genre=genre)
            else:
                messages.success(request,"Book with this specification doesnot exist")
    else:
        if request.method=="GET":
            bs = request.GET.get('bs')
            if IndiDonar.objects.filter(bookname__iexact = bs,genre=genre).exists():
                books = IndiDonar.objects.all().filter(bookname__iexact = bs,genre=genre)
            elif IndiDonar.objects.filter(authorname__iexact = bs,genre=genre).exists():
                books = IndiDonar.objects.all().filter(authorname__iexact=bs,genre=genre)
            elif IndiDonar.objects.filter(isbn = bs,genre=genre).exists():
                books = IndiDonar.objects.all().filter(isbn = bs,genre=genre)
            else:
                messages.success(request,"Book with this specification doesnot exist")
        if request.method=="POST":
            bs=request.POST['bs'].lower()
            if IndiDonar.objects.filter(bookname = bs,genre = genre).exists():
                books = IndiDonar.objects.all().filter(bookname__iexact = bs,genre=genre)
            elif IndiDonar.objects.filter(authorname__iexact = bs,genre = genre).exists():
                books = IndiDOnar.objects.all().filter(authorname__iexact=bs,genre=genre)
            elif IndiDonar.objects.filter(isbn = bs,genre = genre).exists():
                books = IndiDonar.objects.all().filter(isbn = bs,genre=genre)
            else:
                messages.success(request,"Book with this specification doesnot exist")
    return render(request,f'donate/resell/Search.html',{"books":books,"q":query1,"g":genre,"bs":bs})
