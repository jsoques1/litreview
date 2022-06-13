from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
# from PIL import Image


class Ticket(models.Model):
    # class Meta:
    #     ordering = ["-time_created"]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'self.user=[{self.user}]  self.title=[{self.title}] self.image=[{self.image}]'


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'self.user=[{self.user}] self.headline=[{self.headline}]'


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name="followed_by")

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )

        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_no_self_stalking",
                check=~models.Q(user=models.F("followed_user")),
            ),
        ]

    def __str__(self):
        return f'self.user=[{self.user}] self.followed_user=[{self.followed_user}]'
