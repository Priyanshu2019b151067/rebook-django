
from django.urls import path,include
from .views import (
    home_view,
    about_view,
    privacy_view,
    terms_view,
    contact_view,
    profile,
)
urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("privacy_view/", privacy_view, name="privacy"),
    path("terms_view/", terms_view, name="terms"),
    path("contact_view/", contact_view, name="contact"),
    path("profile", profile, name="profile")


]