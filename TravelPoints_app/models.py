from django.db import models


# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=30, unique=True, null=False)
    password = models.CharField(max_length=200, unique=True, null=False)
    email = models.CharField(max_length=60, null=False)
    role = models.CharField(default="client", max_length=6, null=False)


class Review(models.Model):
    rating = models.IntegerField(null=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=1000, null=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Attraction(models.Model):
    name = models.CharField(max_length=30, null=False)
    location = models.CharField(max_length=30, null=False)
    category = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=1000, null=False)
    path_to_file = models.CharField(max_length=500, null=False)
    role = models.CharField(max_length=50, null=False)
    average_review = models.FloatField(null=False)
    comments = models.ManyToManyField(Comment, related_name="attractions")
    reviews = models.ManyToManyField(Review, related_name="attractions")


class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='wishlists')
