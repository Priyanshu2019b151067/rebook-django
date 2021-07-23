from django.urls import path
from .views import *
urlpatterns = [
    path("enlist_book/",enlist_book, name="enlist_book"),
    path("buy_book/", buy_book, name="buy_book"),

# language
    # path("buy_book/language/English/",lang_english, name="english"),
    # path("buy_book/language/French/",lang_french, name="french"),
    # path("buy_book/language/Hindi/",lang_hindi, name="hindi"),
    # path("buy_book/language/Sanskrit/",lang_sans, name="sanskrit"),
    # path("buy_book/language/others/",lang_others, name="others"),

    path("buy_book/search/",search, name ="search"),
    path("buy_book/location/",location, name="location"),

    # path("buy_book/search_all/",search_all, name ="search_all"),
    # path("buy_book/location_all/",location_all, name="location_all"),


    path("buy_book/mainsearch/",mainsearch, name="mainsearch"),
    path("buy_book/search-location/<bs>",searchlocation, name="Searchlocation"),
    path("buy_book/<reseller_name>/<bookname>/delete/",delete_view, name="delete_page1"),
    path("buy_book/<reseller_name>/<bookname>/details/", details, name="resell_details"),
    path("buy_book/error/",error, name="error"),
    path("category/", all_rounder, name="category"),
    # path("category1/", competitive , name="category1"),


]
