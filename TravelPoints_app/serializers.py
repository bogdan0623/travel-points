from rest_framework import serializers
from .models import Account, Attraction, Comment, Review, Wishlist


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id',
                  'username',
                  'password',
                  'email',
                  'role')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id',
                  'text',
                  'user')


class CommentPostPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id',
                  'text',
                  'user')


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id',
                  'rating',
                  'user')


class ReviewAttractionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    attractions = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id',
                  'rating',
                  'user',
                  'attractions')


class ReviewPostPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id',
                  'rating',
                  'user')


class WishlistAttractionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Wishlist
        fields = ('id',
                  'user')


class AttractionSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(
        many=True,
        read_only=True
    )

    reviews = ReviewSerializer(
        many=True,
        read_only=True
    )

    wishlists = WishlistAttractionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Attraction
        fields = ('id',
                  'name',
                  'location',
                  'category',
                  'description',
                  'path_to_file',
                  'role',
                  'average_review',
                  'comments',
                  'reviews',
                  'wishlists'
                  )


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    attraction = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Wishlist
        fields = ('id',
                  'user',
                  'attraction'
                  )


class WishlistPostPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id',
                  'user',
                  'attraction'
                  )
