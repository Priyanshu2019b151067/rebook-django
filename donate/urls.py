
from django.urls import path,include
from .views import *
urlpatterns = [
    path("", donate_home, name="donate"),
    path("create_ngo/",create_ngo, name="create_ngo"),
    path("verify/<auth_token>",verify, name="verify"),
    path("verify_donar/<ngo_name>/<auth_token>",verify_donar, name="verify_donar"),
    path("success",success,name="success"),
    path("<str:ngo_name>/", book_donater_view, name="bookdonater"),
    path("individual/listfordonation/", list_for_donation, name="listdonation"),
    # available_book
    path("individual/available_books/", available_books, name="available_books"),
    path("buy_book/mainsearch/",mainsearch, name="mainsearch1"),
    path("buy_book/search-location/<bs>",searchlocation, name="Searchlocation1"),
    path("donate/<str:donarname>/<str:bookname>/details", details, name="donate_details"),
    # path("buy_book/<donar_name>/<bookname>/details/", details, name="donar_details"),
#     # path("academics/X_and_below/",academics_x_below, name="donate_X_and_below"),
#     path("academics/I_and_XII/",academics_begin, name="donate_I_and_XII"),
#     path("academics/Jee/",academics_jee, name="donate_jee"),
#     path("academics/Competitive_exam/",academics_competitive, name="donate_Competitive_exam"),
#     path("academics/Government_exam",academics_government, name="donate_Government_exam"),
#     path("academics/Engineering_Books_and_Modules/",academics_engineering, name="donate_engineering"),
#     path("academics/Commerce_and_accounting/",academics_commerce_arts, name="donate_Commerce_and_Account"),
#     path("academics/Others/",academics_others, name="donate_AccOthers"),
#     # non academics
#     path("non_academics/self_help_spirituality/",self_help, name="donate_shsp"),
#     path("non_academics/Entertainment/",entertainment, name="donate_Entertainment"),
#     path("non_academics/Finance_and_Economy/",finance, name="donate_Finance_and_Economy"),
#     path("non_academics/others/",non_acc_other, name="donate_nonacc"),

# # language
#     path("language/English/",lang_english, name="donate_english"),
#     path("language/French/",lang_french, name="donate_french"),
#     path("language/Hindi/",lang_hindi, name="donate_hindi"),
#     path("language/Sanskrit/",lang_sans, name="donate_sanskrit"),
#     path("language/others/",lang_others, name="donate_others"),

    # path("donate/location/",location, name="donate_location"),
    # path("donate/search/",search, name="donate_search"),
    path("donate/<donarname>/<bookname>", delete_page, name="delete_page"),

    # Page detail
    path("buy_book/category/", all_rounder, name="category1"),
    path("buy_book/search/",search, name ="search1"),
    path("buy_book/location/",location, name="location1"),

    # Acknow
    # path("donate/acknowledge/", acknowledge, name="acknowledge")

]