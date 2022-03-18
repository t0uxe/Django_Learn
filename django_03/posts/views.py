from django.views.generic import ListView
from .models import Post

"""
Creamos la vista para 
"""

class HomePageView(ListView):
    model = Post
    template_name = "home.html"

