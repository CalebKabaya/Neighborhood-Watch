from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import Profile,Post,NeighbourHood
from .forms import  UpdateUserForm, UpdateUserProfileForm,NeighbourHoodForm
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

def join_hood(request,id):
    neighbourhood=get_object_or_404(NeighbourHood,id=id)  
    request.user.profile.neighbourhood=neighbourhood
    request.user.profile.save()
    return redirect('displayhood')  
def leave_hood(request,id):
    hood=get_object_or_404(NeighbourHood,id=id)  
    request.user.profile.neighbourhood=None
    request.user.profile.save()
    return redirect('displayhood')      


@login_required(login_url='login')
def viewhood(request,hood_id):
    hoods = NeighbourHood.objects.get(id=hood_id)
    params={
        "hoods":hoods
    }
    return render(request,'viewhood.html',params)


# def post_bussiness