from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Category 

# Create your views here.
# categories = [
#         {"id": 1, "name": "Electronics"},
#         {"id": 2, "name": "Clothes"},
#         {"id": 3, "name": "Books"},
#         {"id": 4, "name": "Sports"},
#         {"id": 5, "name": "Home"},
#     ]


y= 100
def index(request):

    request.session['price']=1000
    request.session["m"]= "شهر مبارك "
    
    
    categories = Category.objects.all()
    print(categories)


    x=50
    context={
        'cat':categories
        
    }

   
    response=render (request,'category/index.html',context)
    response.set_cookie(
        key='user',
        value='raghad',
        max_age=3600
    )
    return response
    
def get_name(request):
    print(y)


