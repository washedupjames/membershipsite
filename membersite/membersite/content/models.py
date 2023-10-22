from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.signals import user_logged_in
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from allauth.account.signals import email_confirmed
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()

class Pricing(models.Model):
    name = models.CharField(max_length=100)  # Basic / Pro / Premium
    slug = models.SlugField()
    stripe_price_id = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    currency = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='subscriptions')
    created = models.DateTimeField(auto_now_add=True)
    stripe_subscription_id = models.CharField(max_length=50)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email

    @property
    def is_active(self):
        return self.status == "active" or self.status == "trialing"


class Course(models.Model):
    pricing_tiers = models.ManyToManyField(Pricing, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to="thumbnails/")
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("content:course-detail", kwargs={"slug": self.slug})


class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    vimeo_id = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ["order"]    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("content:video-detail", kwargs={
            "video_slug": self.slug,
            "slug": self.course.slug
        })


def pre_save_course(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


def pre_save_video(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


def post_email_confirmed(request, email_address, *args, **kwargs):
    user = User.objects.get(email=email_address.email)
    free_trial_pricing = Pricing.objects.get(name='Free Trial')
    subscription = Subscription.objects.create(
        user=user, 
        pricing=free_trial_pricing
    )
    stripe_customer = stripe.Customer.create(
        email=user.email
    )
    stripe_subscription = stripe.Subscription.create(
        customer=stripe_customer["id"],
        items=[{'price': 'price_1N8c7gGBYNWOlq9ALiwYNxDZ'}],
        trial_period_days=7
    )
    subscription.status = stripe_subscription["status"]  # trialing
    subscription.stripe_subscription_id = stripe_subscription["id"]
    subscription.save()
    user.stripe_customer_id = stripe_customer["id"]
    user.save()ssssss


def user_logged_in_receiver(sender, user, **kwargs):
    subscription = user.subscription
    sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id)

    subscription.status = sub["status"]
    subscription.save()


user_logged_in.connect(user_logged_in_receiver)
email_confirmed.connect(post_email_confirmed)
pre_save.connect(pre_save_course, sender=Course)
pre_save.connect(pre_save_video, sender=Video)