from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from rango.models import Category
from rango.models import Page
from rango.models import UserProfile
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.shortcuts import redirect

def index(request):
    category_list = Category.objects.all()
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response


def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    #context_dict['visits'] = count
    return render(request,'rango/about.html',{'visits':count})

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

def category(request,category_name_slug):
   # Creates a context dictionary which we can pass to the template rendering engine
    context_dict = {}

    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query
    
    try:
      
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance
        pages = Page.objects.filter(category=category).order_by('-views')

        # Adds our results list to the template context under name pages
        context_dict['pages'] = pages
       
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
      
        pass
    if not context_dict['query']:
        context_dict['query'] = category.name
  
    return render(request, 'rango/category.html', context_dict)


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html',{})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
        
            form.save(commit=True)

            # call index() view.
            # User will be shown homepage
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
            
    return redirect(url)

def register_profile(request):
    
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print profile_form.errors
    else:
        profile_form = UserProfileForm()
        
    return render(request, 'rango/profile_registration.html', {'profile_form': profile_form,'registered':registered})

def profile(request):
    user = request.user
    context_dict = {}
    context_dict['user'] = user
    try:
        profile = UserProfile.objects.get(user=user)
        context_dict['profile'] = profile
    except:
        pass

    return render(request, 'rango/profile.html',context_dict)

def edit_profile(request):
    registered = False
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
            profile_form = UserProfileForm(request.POST, instance=profile)
        except:
            profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            if request.user.is_authenticated():
                profile = profile_form.save(commit=False)
                user = request.user
                profile.user = user
                try:
                    profile.picture = request.FILES['picture']
                except:
                    pass
                profile.save()
                registered = True
        else:
             print profile_form.errors
        return index(request)
    else:
        profile_form = UserProfileForm(request.GET)
    
    context_dict = {}
    context_dict['profile'] = profile_form
    context_dict['registered'] = registered 
    return render(request,'rango/edit_profile.html',context_dict)

def user_profile(request,user_name):
    context_dict = {}
    
    other_user = User.objects.get(username = user_name)
    context_dict['other_user'] = other_user
    try:
        profile = UserProfile.objects.get(user=other_user)
        context_dict['profile'] = profile
    except:
        pass
    return render(request, 'rango/user_profile.html',context_dict)

def all_users(request):
    context_dict = {}
    people = User.objects.order_by('-email')
    context_dict={"people": people}
    return render(request, 'rango/all_users.html',context_dict)

@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat, 'category_name_slug': category_name_slug}

    return render(request, 'rango/add_page.html', context_dict)

from rango.forms import UserForm, UserProfileForm

