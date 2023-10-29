from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^accounts/$', views.accountApi),
    re_path(r'^accounts/([0-9]+)$', views.accountApi),
    re_path(r'^attractions/$', views.attractionApi, name='attractionApi'),
    re_path(r'^attractions/([0-9]+)$', views.attractionApi),
    re_path(r'^attractions/category/([a-zA-Z0-9]+)$', views.attractionCategoryApi),
    re_path(r'^attractions/location/([a-zA-Z0-9]+)$', views.attractionLocationApi),
    re_path(r'^comments/$', views.commentApi),
    re_path(r'^comments/([0-9]+)$', views.commentApi),
    re_path(r'^review/$', views.reviewApi),
    re_path(r'^review/([0-9]+)$', views.reviewApi),
    re_path(r'^getAllReviews/([0-9]+)$', views.getAllReviews),
    re_path(r'^reviewToAttraction/([0-9]+)$', views.reviewToAttractionApi, name='reviewToAttractionApi'),
    re_path(r'^wishlist/$', views.wishlistApi),
    re_path(r'^wishlist/([0-9]+)$', views.wishlistApi),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^wishlist/user/([0-9]+)$', views.wishlistUserApi),

]
