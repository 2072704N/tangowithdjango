from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request,'rango/about.html')

def category(request,category_name_slug):
   # Creates a context dictionary which we can pass to the template rendering engine
    context_dict = {}

    try:
      
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages
        context_dict['pages'] = pages
       
        context_dict['category'] = category
    except Category.DoesNotExist:
      
        pass

  
    return render(request, 'rango/category.html', context_dict)
