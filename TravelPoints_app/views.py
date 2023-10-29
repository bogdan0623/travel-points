from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import make_password, check_password

from TravelPoints_app.models import Account, Attraction, Comment, Wishlist
from TravelPoints_app.serializers import AccountSerializer, AttractionSerializer, CommentSerializer, WishlistSerializer, \
    CommentPostPutSerializer, WishlistPostPutSerializer

from .models import Review
from .serializers import ReviewPostPutSerializer, ReviewSerializer, ReviewAttractionSerializer
from .validators import *


@csrf_exempt
def accountApi(request, id=0):
    if request.method == 'GET':
        if id == 0:
            accounts = Account.objects.all()
            accounts_serializer = AccountSerializer(accounts, many=True)
            return JsonResponse(accounts_serializer.data, safe=False)
        else:
            account = Account.objects.get(id=id)
            account_serializer = AccountSerializer(account)
            print(account.comment_set.all())
            return JsonResponse(account_serializer.data, safe=False)
    elif request.method == "POST":
        account_data = JSONParser().parse(request)

        if not validate_password(account_data['password']):
            return JsonResponse("Password not strong enough", safe=False)

        account_data["password"] = make_password(account_data["password"])

        if not validate_email_address(account_data['email']):
            return JsonResponse("Email not correct", safe=False)

        account_serializer = AccountSerializer(data=account_data)
        if account_serializer.is_valid():
            account_serializer.save()
            return JsonResponse("Account added successfully!!", safe=False)
        return JsonResponse("Failed to add account", safe=False)
    elif request.method == 'PUT':
        try:
            account_data = JSONParser().parse(request)
            if 'password' in account_data:
                account_data['password'] = make_password(account_data['password'])
            account = Account.objects.get(id=account_data['id'])
            account_serializer = AccountSerializer(account, data=account_data, partial=True)
            if account_serializer.is_valid():
                account_serializer.save()
                return JsonResponse("Account updated successfully!!", safe=False)
            else:
                return JsonResponse("Failed to update account!!", safe=False)
        except Exception:
            return JsonResponse("Failed to update account!!", safe=False)
    elif request.method == 'DELETE':
        try:
            account = Account.objects.get(id=id)
            account.delete()
            return JsonResponse("Account deleted successfully!!", safe=False)
        except Exception:
            return JsonResponse("Failed to delete account!!", safe=False)


@csrf_exempt
def login(request):
    try:
        if request.method == "POST":
            account_data = JSONParser().parse(request)
            print(account_data['password'])
            account = Account.objects.get(username=account_data['username'])
            print(account.password)
            account_serializer = AccountSerializer(account)
            if check_password(account_data['password'], account.password):
                return JsonResponse(account_serializer.data, safe=False)
            else:
                return JsonResponse({"error": "Incorrect password!"}, status=401)
    except Exception:
        pass
    return JsonResponse({"error": "LOGIN FAILED!"}, status=401)


@csrf_exempt
def attractionApi(request, id=0):
    if request.method == 'GET':
        if id == 0:
            attractions = Attraction.objects.all()
            attractions_serializer = AttractionSerializer(attractions, many=True)
            return JsonResponse(attractions_serializer.data, safe=False)
        else:
            attraction = Attraction.objects.get(id=id)
            attraction_serializer = AttractionSerializer(attraction)
            return JsonResponse(attraction_serializer.data, safe=False)
    elif request.method == "POST":
        attraction_data = JSONParser().parse(request)
        attraction_serializer = AttractionSerializer(data=attraction_data)
        if attraction_serializer.is_valid():
            attraction_serializer.save()
            return JsonResponse("Attraction added successfully!!", safe=False)
        return JsonResponse("Failed to add attraction", safe=False)
    elif request.method == 'PUT':
        try:
            attraction_data = JSONParser().parse(request)
            attraction = Attraction.objects.get(id=attraction_data['id'])
            attraction_serializer = AttractionSerializer(attraction, data=attraction_data, partial=True)
            if attraction_serializer.is_valid():
                attraction_serializer.save()
                return JsonResponse("Attraction updated successfully!!", safe=False)
            else:
                return JsonResponse("Failed to update attraction!!", safe=False)
        except Exception:
            return JsonResponse("Failed to update attraction!!", safe=False)
    elif request.method == 'DELETE':
        try:
            attraction = Attraction.objects.get(id=id)
            attraction.delete()
            return JsonResponse("Attraction deleted successfully!!", safe=False)
        except Exception:
            return JsonResponse("Failed to delete attraction!!", safe=False)


@csrf_exempt
def attractionCategoryApi(request, category=''):
    if request.method == 'GET':
        attraction = Attraction.objects.filter(category=category)
        attraction_serializer = AttractionSerializer(attraction, many=True)
        return JsonResponse(attraction_serializer.data, safe=False)


@csrf_exempt
def attractionLocationApi(request, location=''):
    if request.method == 'GET':
        attraction = Attraction.objects.filter(location=location)
        attraction_serializer = AttractionSerializer(attraction, many=True)
        return JsonResponse(attraction_serializer.data, safe=False)


@csrf_exempt
def commentApi(request, id=0):
    if request.method == 'GET':
        if id == 0:
            comments = Comment.objects.all()
            comments_serializer = CommentSerializer(comments, many=True)
            return JsonResponse(comments_serializer.data, safe=False)
        else:
            comment = Comment.objects.get(id=id)
            comment_serializer = CommentSerializer(comment)
            return JsonResponse(comment_serializer.data, safe=False)
    elif request.method == "POST":
        comment_data = JSONParser().parse(request)
        comment_serializer = CommentPostPutSerializer(data=comment_data)
        if id != 0:
            attraction = Attraction.objects.get(id=id)
            if comment_serializer.is_valid():
                comment_added = comment_serializer.save()
                attraction.comments.add(comment_added)
                attraction.save()
                return JsonResponse("Comment added successfully!!", safe=False)
            return JsonResponse("Failed to add comment", safe=False)
    elif request.method == 'PUT':
        try:
            comment_data = JSONParser().parse(request)
            comment = Comment.objects.get(id=comment_data['id'])
            comment_serializer = CommentPostPutSerializer(comment, data=comment_data, partial=True)
            if comment_serializer.is_valid():
                comment_serializer.save()
                return JsonResponse("Comment edited successfully!!", safe=False)
            return JsonResponse("Failed to add comment", safe=False)
        except Exception:
            return JsonResponse("Failed to update comment!!", safe=False)
    elif request.method == 'DELETE':
        try:
            comment = Comment.objects.get(id=id)
            comment.delete()
            return JsonResponse("Comment deleted successfully!!", safe=False)
        except Exception:
            return JsonResponse("Failed to delete comment!!", safe=False)


@csrf_exempt
def reviewApi(request, id=0):
    if request.method == 'GET':
        if id == 0:
            reviews = Review.objects.all()
            reviews_serializer = ReviewSerializer(reviews, many=True)
            return JsonResponse(reviews_serializer.data, safe=False)
        else:
            review = Review.objects.get(id=id)
            review_serializer = ReviewSerializer(review)
            return JsonResponse(review_serializer.data, safe=False)
    elif request.method == "POST":
        review_data = JSONParser().parse(request)
        review_serializer = ReviewPostPutSerializer(data=review_data)
        if review_serializer.is_valid():
            review_serializer.save()
            return JsonResponse("Review added successfully!!", safe=False)
        return JsonResponse("Failed to add review", safe=False)
    elif request.method == 'PUT':
        try:
            review_data = JSONParser().parse(request)
            review = Review.objects.get(id=review_data['id'])
            review_serializer = ReviewPostPutSerializer(review, data=review_data, partial=True)
            if review_serializer.is_valid():
                review_serializer.save()
                return JsonResponse("Review edited successfully!!", safe=False)
            return JsonResponse("Failed to add review", safe=False)
        except Exception:
            return JsonResponse("Failed to update review!!", safe=False)
    elif request.method == 'DELETE':
        try:
            review = Review.objects.get(id=id)
            review.delete()
            return JsonResponse("Review deleted successfully!!", safe=False)
        except Exception:
            return JsonResponse("Failed to delete review!!", safe=False)


@csrf_exempt
def reviewToAttractionApi(request, id_attraction=0):
    if request.method == 'POST':
        if id_attraction != 0:
            attraction = Attraction.objects.get(id=id_attraction)
            print(attraction)
            review_data = JSONParser().parse(request)
            review_serializer = ReviewPostPutSerializer(data=review_data)
            if review_serializer.is_valid():
                review_added = review_serializer.save()
                attraction.reviews.add(review_added.id)
                review_sum = 0
                count = 0
                for review in attraction.reviews.all():
                    review_sum += review.rating
                    count += 1
                average = review_sum / count
                attraction.average_review = average
                attraction.save()
                return JsonResponse("Review added successfully!!", safe=False)
            return JsonResponse("Failed to add review", safe=False)
    elif request.method == 'DELETE':
        if id_attraction != 0:
            attraction = Attraction.objects.get(id=id_attraction)
            review_data = JSONParser().parse(request)
            review_serializer = ReviewPostPutSerializer(data=review_data)
            if review_serializer.is_valid():
                review_sum = 0
                count = 0
                rev_id = 0
                for review in attraction.reviews.all():
                    print(review.user)
                    if review.rating == review_data['rating'] and review.user == Account.objects.get(
                            id=review_data['user']):
                        rev_id = review.id
                    else:
                        review_sum += review.rating
                        count += 1
                average = review_sum / count
                attraction.reviews.remove(rev_id)
                attraction.average_review = average
                attraction.save()
                return JsonResponse("Review deleted successfully!!", safe=False)
            return JsonResponse("Failed to delete review", safe=False)


@csrf_exempt
def getAllReviews(request, id=0):
    if request.method == 'GET':
        if id != 0:
            review = Review.objects.filter(user=id)
            print(review)
            review_serializer = ReviewAttractionSerializer(review, many=True)
            return JsonResponse(review_serializer.data, safe=False)


@csrf_exempt
def wishlistApi(request, id=0):
    if request.method == 'GET':
        if id == 0:
            wishlists = Wishlist.objects.all()
            wishlists_serializer = WishlistSerializer(wishlists, many=True)
            return JsonResponse(wishlists_serializer.data, safe=False)
        else:
            wishlist = Wishlist.objects.get(id=id)
            wishlist_serializer = WishlistSerializer(wishlist)
            return JsonResponse(wishlist_serializer.data, safe=False)
    elif request.method == "POST":
        wishlist_data = JSONParser().parse(request)
        wishlist_serializer = WishlistPostPutSerializer(data=wishlist_data)
        if wishlist_serializer.is_valid():
            wishlist_serializer.save()
            return JsonResponse("Wishlist added successfully!!", safe=False)
        return JsonResponse("Failed to add wishlist", safe=False)
    elif request.method == 'PUT':
        try:
            wishlist_data = JSONParser().parse(request)
            wishlist = Wishlist.objects.get(id=wishlist_data['id'])
            wishlist_serializer = WishlistPostPutSerializer(wishlist, data=wishlist_data, partial=True)
            print(wishlist_serializer.data)
            if wishlist_serializer.is_valid():
                wishlist_serializer.save()
                return JsonResponse("Wishlist updated successfully!!", safe=False)
            else:
                return JsonResponse("Failed to update wishlist!!", safe=False)
        except Exception:
            return JsonResponse("Failed to update wishlist!!", safe=False)
    elif request.method == 'DELETE':
        print("HELOOO")
        if id == 0:
            wishlist_data = JSONParser().parse(request)
            wishlist_serializer = WishlistPostPutSerializer(data=wishlist_data)
            if wishlist_serializer.is_valid():
                try:
                    wishlist = Wishlist.objects.get(user=wishlist_data["user"], attraction=wishlist_data["attraction"])
                    wishlist.delete()
                    return JsonResponse("Wishlist deleted successfully!!", safe=False)
                except Exception:
                    return JsonResponse("Failed to delete wishlist!!", safe=False)
        else:
            try:
                wishlist = Wishlist.objects.get(id=id)
                wishlist.delete()
                return JsonResponse("Wishlist deleted successfully!!", safe=False)
            except Exception:
                return JsonResponse("Failed to delete wishlist!!", safe=False)


@csrf_exempt
def wishlistUserApi(request, user=0):
    if request.method == 'GET':
        wishlist = Wishlist.objects.filter(user=user)
        wishlist_serializer = WishlistSerializer(wishlist, many=True)
        wishlist_serializer = list(wishlist_serializer.data)
        return JsonResponse({'wishlist': wishlist_serializer})

