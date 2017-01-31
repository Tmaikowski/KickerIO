from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count

from .forms import UserCreateForm, ProfileForm
from .models import Profile

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.
def index(request):
    #if logged in, go to news:index
    if request.user.is_authenticated():
        return redirect(reverse('news:index'))
    form = AuthenticationForm
    context = {
        'authform': form
    }
    return render(request, 'login_register/login.html', context)

def process_login(request):
    if request.method == "POST":
        bound_form = AuthenticationForm(request.POST)
        testuser = authenticate(username=request.POST['username'], password=request.POST['password'])
        if testuser:
            login(request, testuser)
            return redirect(reverse("news:index"))
        else:
            return redirect(reverse("login_register:index"))

    return redirect(reverse("news:index"))

def register(request):
    user_form = UserCreateForm
    profile_form = ProfileForm
    context = {
        'register_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'login_register/register.html', context)

def process_registration(request):
    user_form = UserCreateForm(request.POST)
    profile_form = ProfileForm(request.POST)
    print "*"*50
    print request.POST['bio']
    print request.POST['birthday']
    print "*"*50
    if user_form.is_valid() and profile_form.is_valid():
        print "BOTH FORMS VALID!!!!"
        user = user_form.save(commit=False) #in case we want to do something else with the user object before committing...
        user.save()
        print "SAVED USER"
        profile = profile_form.save(commit=False, on_register=True, user_obj=user)
        profile.save()
        print profile
        print "SAVED PROFILE"
        login(request, user)
        print "GOING TO NEWS INDEX"
        return redirect(reverse('news:index'))
    else:
        print "Back to register..."
        return redirect(reverse('login_register:register'))

def logout(request):
    auth.logout(request)
    return redirect(reverse("login_register:index"))

def account(request, id):
    if request.user.id == int(id):
        profile = Profile.objects.get(user_id=request.user.id)
        follows = profile.follows.all()
        context = {
            'follows': follows
        }
        return render(request, 'login_register/account.html', context)
    else:
        return redirect(reverse('login_register:index'))

def edit(request, id):
    if request.user.id == int(id):
        user = User.objects.get(id=request.user.id)

        #use initial parameter to initialize preset values for form
        user_form = UserCreateForm(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email
            }
        )
        profile_form = ProfileForm(
            initial={
                'bio': user.profile.bio,
                'birthday': user.profile.birthday
            }
        )
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'login_register/edit.html', context)
    else:
        return redirect(reverse('login_register:index'))

def update_account(request, id):
    if request.method == "POST":
        bound_user = UserCreateForm(request.POST)
        bound_profile = ProfileForm(request.POST)
        print bound_user['first_name'].value()

        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)

        user.first_name = bound_user['first_name'].value()
        user.last_name = bound_user['last_name'].value()
        user.username = bound_user['username'].value()
        user.email = bound_user['email'].value()
        profile.bio = bound_profile['bio'].value()
        profile.birthday = bound_profile['birthday'].value()
        user.save()
        profile.save()
        return redirect(reverse("login_register:account_settings", args=(request.user.id,)))

    return redirect(reverse('login_register:edit', args=(request.user.id,)))

def follow(request, id):
    #Go through the profile to set the M2M relationship
    profile = User.objects.get(id=request.user.id).profile
    profile_to_follow = User.objects.get(id=id).profile
    # user.follows.add(to_follow)
    print "*"*50
    print profile
    print "*"*50
    print profile_to_follow
    print "*"*50
    profile.follows.add(profile_to_follow)
    return redirect(reverse('news:newsreel'))

def profile(request, id):
    user = User.objects.get(id=id)
    recent_articles = user.article_set.all().order_by("-created_at")[:3]
    popular_articles = user.article_set.all().annotate(num_likes=Count('like')).order_by("-num_likes")[:3]
    followers = Profile.objects.filter(follows=user.profile.id).count()
    context = {
        'user': user,
        'recent_articles': recent_articles,
        'popular_articles': popular_articles,
        'followers': followers
    }
    return render(request, 'login_register/profile.html', context)
