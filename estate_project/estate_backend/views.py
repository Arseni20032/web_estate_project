import os.path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from estate_project.settings import BASE_DIR, MEDIA_ROOT
from .forms import CustomUserCreationForm, ReviewForm
from .models import Post, FAQ, Employee, PromoCode, Review, JobVacancy

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def about_company(request):
    return render(request,
                  'blog/post/about_company.html')


def faq_list(request):
    faq_items = FAQ.objects.all()
    return render(request, 'blog/post/faq_list.html', {'faq_items': faq_items})


def privacy_policy(request):
    return render(request, 'blog/post/privacy_policy.html')


def contacts(request):
    employees = Employee.objects.all()
    print(os.path.join(BASE_DIR, 'media'))
    print(MEDIA_ROOT)
    print(BASE_DIR)
    print("Текущая директория:", os.getcwd())
    return render(request, 'blog/post/contacts.html', {'employees': employees})


def promo_code(request):
    promo = PromoCode.objects.all()
    return render(request, 'blog/post/promocode.html', {'promocodes': promo})


def reviews(request):
    review = Review.objects.all()
    return render(request, 'blog/post/reviews.html', {'reviews': review})


def vacancies(request):
    vacancies = JobVacancy.objects.all()
    return render(request, 'blog/post/vacancies.html', {'vacancies': vacancies})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('blog:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# class CustomLoginView(LoginView):
#     template_name = 'blog/post/registration/login.html'  # Путь к шаблону для страницы входа
#     success_url = reverse_lazy('blog:reviews')

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('blog:reviews')
    else:
        form = ReviewForm()
    return render(request, 'blog/post/add_review.html', {'form': form})


def home(request):
    latest_post = Post.objects.latest("publish")
    return render(request, 'blog/post/home.html', {'latest_post': latest_post})


def all_elem(request):
    return render(request, 'blog/post/all_elements.html')




