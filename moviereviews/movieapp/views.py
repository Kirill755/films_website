from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView
from .forms import *


def index(request):
    reviews = Review.objects.all()
    users = User.objects.all()
    reviews_th = Review.objects.all().order_by('-pk')[:3]

    if request.user.is_authenticated:
        if request.COOKIES.get('welcome') is not None:
            context = {
                'reviews': reviews_th,
                'users': users,
                'welcome': request.COOKIES.get('welcome'),
            }
            print(context)
            response = render(request, 'movieapp/index.html', context)
            response.delete_cookie('welcome')
            return response
    context = {
        'reviews': reviews_th,
        'users': users,
    }
    return render(request,'movieapp/index.html', context)

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'movieapp/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        response =redirect('home')
        response.set_cookie('welcome', 'Thank you for registering!')
        return response

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'movieapp/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')

def show_profile(request, id):
    my = False
    if id =="my" and request.user.is_authenticated==False:
        return redirect('home')
    else:
        if id == "my" :
            #is_auth
            user = User.objects.get(pk=request.user.pk)
            my = True
        else:
            profilechek = User.objects.filter(pk=int(id))
            if len(profilechek) != 0:
                user = User.objects.get(pk=int(id))
            else:
                return redirect('home')

        if user.pk == request.user.pk:
            my = True

        reviews = Review.objects.filter(user=user.pk)
        viewed = user.users_vieved.all()
        favorites = user.users_favorites.all()


        context = {
            'user': user,
            'my': my,
            'reviews': reviews,
            'viewed': viewed,
            'favorites': favorites,
        }
        return render(request, "movieapp/profile.html", context)

def add_film(request):
    if request.user.is_authenticated and request.user.profile.is_worker:
        if request.method == 'POST':
            form = AddFilmForm(request.POST, request.FILES)
            if form.is_valid():
                film = form.save(commit=False)
                film.user = request.user
                film.save()
                return redirect('home')
        else:
            form = AddFilmForm()
        return render(request, 'movieapp/create_film.html', {'form': form})
    return redirect('home')

def show_films(request):
    films = Film.objects.order_by('film_title').all()

    context = {
        'films': films,
    }

    return render(request, 'movieapp/list_films.html', context=context)

def film_details(request, film_id):
    film = Film.objects.get(pk = film_id)
    reviews = Review.objects.filter(Moviee_id = film_id)
    users = User.objects.all()
    sumMarks = 0
    countMarks = 0
    for rev in reviews:
        sumMarks+=int(rev.Mark)
        countMarks+=1
    avg = 0
    if (countMarks>0):
        avg = round(sumMarks/countMarks, 2)

    #print(avg)
    Review_status=False
    if request.user.is_authenticated:
        is_viewed = False
        is_favourite = False
        user = request.user
        viewed_list = user.users_vieved.all()
        favourite_list = user.users_favorites.all()
        my_reviews = Review.objects.filter(user_id=request.user.id, Moviee_id=film_id)
        if len(my_reviews)!=0:
            Review_status=True

        if film in viewed_list:
            is_viewed = True

        if film in favourite_list:
            is_favourite = True
    else:
        is_viewed =[]
        is_favourite = []

    context = {
        'review_status' : Review_status,
        'is_viewed' : is_viewed,
        'is_favourite' : is_favourite,
        'film': film,
        'reviews' : reviews,
        'users' : users,
        'avg' : avg
    }

    return render(request, 'movieapp/film.html', context=context)

def add_review(request, film_id):
    if request.user.is_authenticated:
        reviews = Review.objects.filter(user_id =request.user.pk,Moviee_id=film_id)
        if len(reviews) == 0:
            filmcheck = Film.objects.filter(pk=film_id)
            if len(filmcheck) != 0:
                film = Film.objects.get(pk=film_id)
                if request.method == 'POST':
                    form = AddReviewForm(request.POST)
                    if form.is_valid():
                        review = form.save(commit=False)
                        review.user = request.user
                        review.Moviee= film
                        review.save()
                        return redirect('film', film_id = film_id)
                else:
                    form = AddReviewForm()
                return render(request, 'movieapp/create_review.html', {'form': form, 'id': film_id})
            else:
                return redirect('films')
        else:
            return redirect('films')
    else:
        return redirect('home')

def add_news(request):
    if request.user.is_authenticated and request.user.profile.is_worker:
        if request.method == 'POST':
            form = AddNewsForm(request.POST)
            if form.is_valid():
                news = form.save(commit=False)
                news.user = request.user
                news.save()
                return redirect('home')
        else:
            form = AddNewsForm()
        return render(request, 'movieapp/create_news.html', {'form': form})
    else:
        return redirect('home')

#@cache_page(60)
def show_news(request):
    news = News.objects.order_by('-time_create').all()

    context = {
        'news': news,
    }

    return render(request, 'movieapp/news.html', context=context)

def update_profile_picture(request, id):
    if request.user.is_authenticated:
        check_profile = Profile.objects.filter(pk=id)
        if len(check_profile) != 0:
            if request.method == 'POST' and request.FILES:
                profile = Profile.objects.get(pk =id)
                profile.avatar = request.FILES["avatarfile"]
                profile.save()
                my = True

                return redirect('show_profile', id = 'my')
            return render(request, 'movieapp/update_profile_picture.html', {'id':id})
        else:
            return redirect('show_profile', id='my')
    else:
        return redirect('home')

def update_profile_status(request, id):
    if request.user.is_authenticated:
        check_profile = Profile.objects.filter(pk = id)
        if len(check_profile) != 0:
            profile = Profile.objects.get(pk = id)
            if request.method == "POST":
                profile.status = request.POST.get("status")
                profile.save()
                return redirect('show_profile', id='my')
            return render(request, 'movieapp/update_profile_status.html', {'profile': profile, 'id':id})
        else:
            return redirect('show_profile', id='my')
    else:
        return redirect('home')

def add_favourite(request, film_id):
    if request.user.is_authenticated:
        check_film = Film.objects.filter(pk=film_id)
        if len(check_film) != 0:
            film = Film.objects.get(pk = film_id)
            user = request.user
            user.users_favorites.add(film)
            film = Film.objects.get(pk=film_id)
            reviews = Review.objects.filter(Moviee_id=film_id)
            users = User.objects.all()

            is_viewed = False
            is_favourite = False
            user = request.user
            viewed_list = user.users_vieved.all()
            favourite_list = user.users_favorites.all()

            if film in viewed_list:
                is_viewed = True

            if film in favourite_list:
                is_favourite = True

            context = {
                'is_viewed': is_viewed,
                'is_favourite': is_favourite,
                'film': film,
                'reviews': reviews,
                'users': users
            }

            return render(request, 'movieapp/film.html', context=context)
        else:
            return redirect('home')
    else:
        return redirect('home')

def add_viewed(request, film_id):
    if request.user.is_authenticated:
        check_film = Film.objects.filter(pk=film_id)
        if len(check_film) != 0:
            film = Film.objects.get(pk = film_id)
            user = request.user
            user.users_vieved.add(film)
            film = Film.objects.get(pk=film_id)
            reviews = Review.objects.filter(Moviee_id=film_id)
            users = User.objects.all()

            is_viewed = False
            is_favourite = False
            user = request.user
            viewed_list = user.users_vieved.all()
            favourite_list = user.users_favorites.all()
            print(viewed_list)

            if film in viewed_list:
                is_viewed = True

            if film in favourite_list:
                is_favourite = True

            context = {
                'is_viewed': is_viewed,
                'is_favourite': is_favourite,
                'film': film,
                'reviews': reviews,
                'users': users
            }

            return render(request, 'movieapp/film.html', context=context)
        else:
            return redirect('home')
    else:
        return redirect('home')

def del_viewed(request, film_id):
    if request.user.is_authenticated:
        check_film = Film.objects.filter(pk=film_id)
        if len(check_film) != 0:
            film = Film.objects.get(pk=film_id)
            user = request.user
            user.users_vieved.remove(film)
            film = Film.objects.get(pk=film_id)
            reviews = Review.objects.filter(Moviee_id=film_id)
            users = User.objects.all()

            is_viewed = False
            is_favourite = False
            user = request.user
            viewed_list = user.users_vieved.all()
            favourite_list = user.users_favorites.all()

            if film in viewed_list:
                is_viewed = True

            if film in favourite_list:
                is_favourite = True

            context = {
                'is_viewed': is_viewed,
                'is_favourite': is_favourite,
                'film': film,
                'reviews': reviews,
                'users': users
            }

            return render(request, 'movieapp/film.html', context=context)
        else:
            return redirect('home')
    else:
        return redirect('home')

def del_favourite(request, film_id):
    if request.user.is_authenticated:
        check_film = Film.objects.filter(pk=film_id)
        if len(check_film) != 0:
            film = Film.objects.get(pk=film_id)
            user = request.user
            user.users_favorites.remove(film)
            film = Film.objects.get(pk=film_id)
            reviews = Review.objects.filter(Moviee_id=film_id)
            users = User.objects.all()

            is_viewed = False
            is_favourite = False
            user = request.user
            viewed_list = user.users_vieved.all()
            favourite_list = user.users_favorites.all()

            if film in viewed_list:
                is_viewed = True

            if film in favourite_list:
                is_favourite = True

            context = {
                'is_viewed': is_viewed,
                'is_favourite': is_favourite,
                'film': film,
                'reviews': reviews,
                'users': users
            }

            return render(request, 'movieapp/film.html', context=context)
        else:
            return redirect('home')
    else:
        return redirect('home')

def del_review(request, id):
    if request.user.is_authenticated:
        review = Review.objects.get(pk=id)
        film_id = review.Moviee_id
        review_user = review.user
        if review_user == request.user or request.user.profile.is_worker == True:
            review.delete()
            return redirect("film", film_id=film_id)
        else:
            return redirect('home')
    else:
        return redirect('home')


def del_news(request, id):
    if request.user.is_authenticated:
        news = News.objects.get(pk=id)
        if request.user.profile.is_worker == True:
            news.delete()
            return redirect('news')
        else:
           return redirect('news')
    else:
        return redirect('news')

def del_film(request, id):
    if request.user.is_authenticated:
        film = Film.objects.get(pk=id)
        if request.user.profile.is_worker == True:
            film.delete()
            return redirect('films')
        else:
           return redirect('films')
    else:
        return redirect('films')

def add_review_ajax(request, film_id):
    success = False
    id = None
    avg = 0
    if request.method == "POST" and request.user.is_authenticated:
        filmcheck = Film.objects.filter(pk=film_id)
        if len(filmcheck) != 0:
            reviews = Review.objects.filter(user_id=request.user.pk, Moviee_id=film_id)
            if len(reviews) == 0:
                film = Film.objects.get(pk=film_id)
                rev = Review()
                rev.Review_title = request.POST.get('name')
                rev.Mark = request.POST.get('mark')
                rev.Main_text = request.POST.get('review')
                rev.Moviee = film
                rev.user = request.user
                rev.save()

                review = Review.objects.get(user_id=request.user.pk, Moviee_id=film_id)
                reviews = Review.objects.filter(Moviee_id=film_id)
                sumMarks = 0
                countMarks = 0
                for rev in reviews:
                    sumMarks += int(rev.Mark)
                    countMarks += 1

                if (countMarks > 0):
                    avg = round(sumMarks / countMarks, 2)

                id = review.id

                success = True
    data = {"success": success, "review_id": id, "avg": avg}
    return JsonResponse(data)