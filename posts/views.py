from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .models import LunchPost, Profile
from .forms import LunchPostForm, ProfileForm, RegisterForm

def feed(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = LunchPost.objects.select_related('owner__profile').all()
    meal  = request.GET.get('meal', '')
    if meal:
        posts = posts.filter(meal=meal)
    total_posts  = LunchPost.objects.count()
    total_joined = sum(p.joined for p in LunchPost.objects.all())
    open_posts   = LunchPost.objects.filter(joined__lt=models.F('slots')).count()
    top_restaurants = (
        LunchPost.objects.values('restaurant')
        .annotate(cnt=Count('id'))
        .order_by('-cnt')[:5]
    )
    return render(request, 'posts/feed.html', {
        'posts': posts,
        'meal': meal,
        'total_posts': total_posts,
        'total_joined': total_joined,
        'open_posts': open_posts,
        'top_restaurants': top_restaurants,
    })

def post_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
    form = LunchPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.owner = request.user
        profile, _ = Profile.objects.get_or_create(user=request.user)
        post.name  = profile.display_name or request.user.username
        post.save()
        return redirect('feed')
    return render(request, 'posts/form.html', {'form': form, 'title': 'โพสต์ใหม่'})

def post_edit(request, pk):
    post = get_object_or_404(LunchPost, pk=pk)
    form = LunchPostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('feed')
    return render(request, 'posts/form.html', {'form': form, 'title': 'แก้ไขโพสต์'})

def post_delete(request, pk):
    post = get_object_or_404(LunchPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('feed')
    return render(request, 'posts/confirm_delete.html', {'post': post})

def join_post(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        post = get_object_or_404(LunchPost, pk=pk)
        if post.joined < post.slots:
            post.joined += 1
            post.save()
    return redirect('feed')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Profile.objects.create(user=user)
        login(request, user)
        return redirect('feed')
    return render(request, 'posts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('feed')
    return render(request, 'posts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    my_posts   = LunchPost.objects.filter(owner=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'posts/profile.html', {
        'profile': profile, 'my_posts': my_posts, 'form': form
    })

def stats_view(request):
    total_posts   = LunchPost.objects.count()
    total_users   = User.objects.count()
    total_joined  = sum(p.joined for p in LunchPost.objects.all())
    top_restaurants = (
        LunchPost.objects.values('restaurant')
        .annotate(cnt=Count('id'))
        .order_by('-cnt')[:5]
    )
    meal_stats = (
        LunchPost.objects.values('meal')
        .annotate(cnt=Count('id'))
        .order_by('-cnt')
    )
    return render(request, 'posts/stats.html', {
        'total_posts': total_posts,
        'total_users': total_users,
        'total_joined': total_joined,
        'top_restaurants': top_restaurants,
        'meal_stats': meal_stats,
    })

def search_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = LunchPost.objects.none()
    q    = request.GET.get('q', '')
    meal = request.GET.get('meal', '')
    area = request.GET.get('area', '')
    searched = q or meal or area
    if searched:
        posts = LunchPost.objects.select_related('owner__profile').all()
        if q:
            posts = posts.filter(Q(restaurant__icontains=q) | Q(note__icontains=q))
        if meal:
            posts = posts.filter(meal=meal)
        if area:
            posts = posts.filter(area__icontains=area)
    return render(request, 'posts/search.html', {
        'posts': posts, 'q': q, 'meal': meal, 'area': area, 'searched': searched
    })