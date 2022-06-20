from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import Profile,Post,NeighbourHood,Business
from .forms import  UpdateUserForm, UpdateUserProfileForm,NeighbourHoodForm,BusinessForm,PostForm
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    all_hoods=NeighbourHood.objects.all()

    return render (request, 'index.html',{"all_hoods":all_hoods})

def signin(request):
    if request.method== "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have successfuly logged in")
            return redirect ("/")
    return render(request,'login.html')

       
def register(request):
    if request.method== "POST":
        username=request.POST["username"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        if password1 != password2:
            messages.error(request,"Your Passwords do not Match!! Please Try Again")
            return redirect('/register')
        new_user=User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1,
        )
        new_user.save()
        return render (request,'login.html')
    return render(request,'register.html')

def signout(request):
    logout(request)
    messages.success(request,"You have logged out, we will be glad to have you back again")
    return redirect ("login")


def profile(request):
    user=request.user
    my_profile=Profile.objects.get(user=user)
    return render(request,"profile.html",{'my_profile':my_profile,"user":user})

@login_required(login_url='login')
def update_profile(request):
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            # return HttpResponseRedirect(request.path_info)
            return redirect('profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    contex = {
        'user_form': user_form,
        'prof_form': prof_form,

    }
    return render(request, 'update_profile.html', contex)    

@login_required(login_url='/accounts/login/')
def posthood(request):
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user=request.user
            project.save()
            
        return redirect('/')
    else:
        form = NeighbourHoodForm()
    try:
        posts=Post.objects.all() 
        posts=posts[::-1]
    except Post.DoesNotExist:
        posts=None

    context = {
        'form':form,
    }
    return render(request, 'addhood.html', context)


def displayhood(request):
    all_hoods=NeighbourHood.objects.all()

    return render(request,'displayhood.html',{"all_hoods":all_hoods})
@login_required(login_url='login')
def join_hood(request,id):
    neighbourhood=get_object_or_404(NeighbourHood,id=id)  
    request.user.profile.neighbourhood=neighbourhood
    request.user.profile.save()
    return redirect('displayhood')  
    
@login_required(login_url='login')
def leave_hood(request,id):
    hood=get_object_or_404(NeighbourHood,id=id)  
    request.user.profile.neighbourhood=None
    request.user.profile.save()
    return redirect('displayhood')      


@login_required(login_url='login')
def viewhood(request,hood_id):
    hoods = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hoods)
    mypost=Post.objects.filter(hood=hoods)


    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighbourhood = hoods
            b_form.user = request.user.profile
            b_form.save()
            return redirect('viewhood', hoods.id)
    else:
        form = BusinessForm()
    params={
        "hoods":hoods,
        'business': business,
        'form': form,
        'mypost':mypost,
    }
    return render(request,'viewhood.html',params)

@login_required(login_url='login')
def create_post(request,hood_id):

    hood = NeighbourHood.objects.get(id=hood_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.hood = hood
            post.user = request.user.profile
            post.save()
            return redirect('newpost', hood.id)
    else:
        post_form = PostForm()
    params={
        'post_form': post_form,
        'hood':hood
    }    
    return render(request, 'viewhood.html', params)
 
# def addpost(request, hood_id):
#     current_user = request.user.id
#     profile = Profile.objects.get(user=request.user.id)
#     # profile=request.user.profile
#     post = NeighbourHood.objects.get(id=hood_id)
#     # hood=request.user.profile.neighbourhood
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user_id = current_user
#             comment.user_profile=profile
#             comment.post_id = post
#             comment.post=post
#             comment.save()
#         return redirect('viewhood')
#     else:
#         form = PostForm()
#     ctx = {
#         'form': form,
#         # 'post': post
#     }
#     return render(request, 'post.html', ctx)

# @login_required(login_url='login')
# def create_post(request):
#     if request.method == 'POST':

#         title=request.POST["title"]
#         post=request.POST["post"]

#         new_post=Post.objects.create_post(
#             title=title,
#             post=post,
#         )
#         new_post.save()
#         return render (request,'viewhood.html')
#     return render(request,'viewhood.html')
# def create_post(request):
#     current_user=request.user
#     profile =Profile.objects.get(user=current_user)
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = current_user
#             post.neighbourhood = profile.neighbourhood
#             post.save()
#             return redirect('viewhood')
#     else:
#         form = PostForm()
#     return render(request, 'post.html', {'form': form})

def hood_members(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    members = Profile.objects.filter(neighbourhood=hood)
    return render(request, 'members.html', {'members': members})

def search_business(request):
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, "results.html")

def search_business(request):
    if request.method == 'GET':
        name = request.GET.get("title")
        results = NeighbourHood.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'hoodresults.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, "hoodresults.html")

@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    profile = request.user.profile
    neighbourhood = request.user.profile.neighbourhood
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.author_profile = profile
            post.hood = neighbourhood
            post.save()
        return redirect('addpost')
    else:
        form = PostForm()
    return render(request, 'post.html', {"form": form})

def create_post(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.hood = hood
            post.user = request.user.profile
            post.save()
            return redirect('viewhood', hood.id)
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})

def add_post(request,hood_id):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    myhoods = NeighbourHood.objects.get(id=hood_id)
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # form.save()
            comment = form.save(commit=False)
            comment.user = user
            comment.hood = myhoods
            comment.save()
            return redirect('/')
        else:
            form = PostForm()
    ctx = {
        'form': form,
        'myhoods': myhoods
    }
    return render(request, 'post.html', ctx)

# def add_post(request, hood_id):

#     hooda = Business.objects.get(id=hood_id)
#     ctx = {
#         'hooda': hooda
#     }
#     return render(request, 'post.html', ctx)    