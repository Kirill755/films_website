from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="photos/%Y/%m/%d/")
    status = models.CharField(verbose_name="User status", null=True, blank=True, max_length=255)
    time_create=models.DateTimeField(auto_now_add=True)
    time_update=models.DateTimeField(auto_now=True)
    is_worker = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Film(models.Model):
    film_title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="photos/%Y/%m/%d/")
    Year = models.CharField(verbose_name="Production year", max_length=50)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    genre = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    description = models.TextField()
    users_favorites = models.ManyToManyField(User, related_name = "users_favorites")
    users_viewed = models.ManyToManyField(User, related_name = "users_vieved")


    def __str__(self):
        return self.film_title

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Films"

class News(models.Model):
    News_title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Main_text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.News_title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

class Review(models.Model):
    FILM_MARKS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Review_title = models.CharField(max_length=255)
    Mark = models.CharField(max_length=2, choices=FILM_MARKS)
    Main_text = models.TextField()
    Moviee=models.ForeignKey(Film, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Review_title

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"