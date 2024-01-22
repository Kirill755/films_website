from django.conf.urls.static import static
from moviereviews import settings
from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('',index, name='home' ),
    path('registration/', RegisterUser.as_view() , name = 'register'),
    path('login/', LoginUser.as_view() , name = 'login'),
    path('logout/', logout_user, name = 'logout'),
    path('addnewfilm/', add_film , name = 'add_film'),
    path('addnews/', add_news , name = 'add_news'),
    path('films/', show_films, name = 'films'),
    path('news/', show_news, name = 'news'),
    path('films/<int:film_id>', film_details, name = 'film'),
    path('addreview/<int:film_id>', add_review, name = 'add_review'),
    path('addreviewajax/<int:film_id>', add_review_ajax, name = 'add_review_ajax'),
    re_path(r'^profile/(?P<id>\w+)\/?$', show_profile, name = 'show_profile'),

    path('updateprofilepicrure/<int:id>', update_profile_picture, name = 'update_profile_picture'),
    path('updateprofilestatus/<int:id>', update_profile_status, name = 'update_profile_status'),

    path('addfavourite/<int:film_id>', add_favourite, name = 'add_favourite'),
    path('addviewed/<int:film_id>', add_viewed, name = 'add_viewed'),

    path('delfavourite/<int:film_id>', del_favourite, name = 'del_favourite'),
    path('delviewed/<int:film_id>', del_viewed, name = 'del_viewed'),

    path('delreview/<int:id>', del_review, name = 'del_review'),
    path('delnews/<int:id>', del_news, name = 'del_news'),
    path('delfilm/<int:id>', del_film, name = 'del_film'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)