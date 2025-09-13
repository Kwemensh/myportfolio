from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="portfolio_home"),          # one-page portfolio
    path("contact/submit", views.contact_submit, name="contact_submit"),  # AJAX form endpoint
]