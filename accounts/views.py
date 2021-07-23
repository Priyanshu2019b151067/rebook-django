# from django.shortcuts import render,redirect
# from django.contrib import messages
# from django.views.decorators.cache import never_cache
# from django.http import Http404
# from usernames import is_safe_username
# from django.contrib.auth.models import User
# from .models import *
# import re
# from django.conf import settings
# from django.core.mail import send_mail
# from django.http import  HttpResponseRedirect
# from django.urls import reverse
# from django.contrib.auth import authenticate,login,logout
# import uuid
# # Create your views here.
# @never_cache
# def login_view(request):
#     try:
#         if request.method=="POST":
#             username = request.POST['username']
#             password = request.POST['password']
#             user_obj = User.objects.filter(username=username).first()
#             if user_obj is None:
#                 user_obj = User.objects.filter(email=username).first()
#                 if user_obj is None:
#                     messages.warning(request,"User doesnot exits")
#                     return redirect("manual_login")
#             profile_obj = Profiles.objects.filter(user=user_obj).first()
#             if not profile_obj.is_verified:
#                     messages.warning(request, 'Account not verified check your mail.')
#                     return redirect("manual_login")
#             username = user_obj.username
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#             else:
#                 messages.warning(request,"Password doesnot match the username")
#                 return redirect("manual_login") 
#     except:
#         raise Http404("Temporary error occured")
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('home'))
#     return render(request,'accounts/login.html',{})
# # def register_view(request):
# #     try:
# #         if request.method == "POST":
# #             if request.POST['password1']==request.POST['password2']:
# #                 username=request.POST['username']
# #                 if is_safe_username(username):
# #                     email = request.POST['email']
# #                     if check(email):
# #                         password = request.POST['password1']
# #                         if check_password(password):
# #                             if User.objects.filter(username=username).first():
# #                                 messages.warning(request, 'Username already exists')
# #                                 return redirect('register')
# #                             if User.objects.filter(email=email).first():
# #                                 messages.warning(request, 'Email already exists')
# #                                 return redirect('register')
# #                             user_obj = User(username = username,email= email)
# #                             user_obj.set_password(password)
# #                             user_obj.save()
# #                             auth_token = str(uuid.uuid4())
# #                             profile_obj = Profiles(user=user_obj,auth_token = auth_token)
# #                             profile_obj.save()
# #                             send_verfication_mail(email,auth_token)
# #                             messages.success(request, 'Account activation link has been send to your registered email.')  
# #                             return redirect('login')
# #                         else:
# #                             messages.warning(request, 'Password is short or invalid')
# #                             return redirect('register')

# #                     else:
# #                         messages.warning(request, 'Email is not appropriate')
# #                         return redirect('register')

# #                 else:
# #                     messages.warning(request, 'Username is not appropriate')
# #                     return redirect('register')

# #             else:
# #                 messages.warning(request, 'Password doesnot match')
# #                 return redirect('register')
# #     except:
# #         raise Http404("Signup error")
# #     return render(request,'accounts/register.html',{})
# # def logout_view(request):
# #     try:
# #         if request.method =="POST":
# #             logout(request)
# #             return redirect('home')
# #     except:
# #         raise Http404("Logout error")

# #     return render(request,'accounts/logout.html',{})
# # def verify(request,auth_token):
# #     try:
# #         profile_obj = Profiles.objects.filter(auth_token = auth_token).first()
# #         if profile_obj:
# #             if profile_obj.is_verified:
# #                 messages.warning(request, 'Account already verified')
# #                 return redirect('manual_login')
# #             profile_obj.is_verified = True
# #             profile_obj.save()
# #             messages.warning(request, 'Account has been verified')
# #             return redirect('manual_login')
# #     except:
# #         return Http404("Verification link is invalid")
    
# # def send_verfication_mail(email,auth_token):
# #     subject = "Account Verification "
# #     message = f'Click the link to verify your account https://rebook-tech.herokuapp.com/accounts/verify/{auth_token}'
# #     email_from = settings.EMAIL_HOST_USER
# #     receiver_list = [email]
# #     send_mail(subject,message,email_from,receiver_list)
# # def check(email):
# #     output = False
# #     regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
# #     if(re.search(regex, email)):
# #         output = True
# #     return output
# # def check_password(password):
# #     output = False
# #     if re.fullmatch(r'[A-Za-z0-9@#$%_^&+=]{8,}', password):
# #         output = True
# #     return output





