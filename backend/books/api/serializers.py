from rest_framework import serializers
from datetime import datetime
from django.utils.timesince import timesince
from books.models import Book, Review

#
# class ArticleSerializer(serializers.ModelSerializer):
#     time_since_publication = serializers.SerializerMethodField()
#
#     # author = serializers.StringRelatedField()
#     """like so we face problem when creating article instance,
#     it needs an author, JournalistSerializer(read_only=true)
#     also doesn't help. we need to make the rs explicit"""
#
#     # author = JournalistSerializer()
#
#     class Meta:
#         model = Article
#         fields = '__all__'
#
#     def get_time_since_publication(self, object):
#         publication_date = object.publication_date
#         now = datetime.now()
#         time_delta = timesince(publication_date, now)
#         return time_delta
#
#     def validate(self, data):
#         """ Validator (object level validation: applies on multiple fields)
#          to check if title and body are different"""
#         if data['title'] == data['description']:
#             raise serializers.ValidationError('Title & description must be different from one another')
#         return data
#
#     def validate_title(self, value):
#         """ Validator (field level validation: applies on a field)
#          60 character long for title"""
#         if len(value) < 60:
#             raise serializers.ValidationError('The title must be at least 60 character long')
#         return value
#
#
# class JournalistSerializer(serializers.ModelSerializer):
#     # we serialize the children telling django here it's a one-to-many rs
#     """ many=True: means no need to pass articles list when
#     creating a journalist instance """
#     # articles = ArticleSerializer(many=True,
#     #                              read_only=True)
#
#     """or like this, if we want to render them as links,
#     ps: add context to the serliazer to pass request"""
#     articles = serializers.HyperlinkedRelatedField(many=True,
#                                                    read_only=True,
#                                                    view_name='article_detail')
#
#     user = serializers.StringRelatedField(read_only=True)
#
#     class Meta:
#         model = Journalist
#         fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    review_author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('book',)
        # fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True,
                               read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     author = serializers.CharField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     body = serializers.CharField()
#     location = serializers.CharField()
#     publication_date = serializers.DateField()
#     active = serializers.BooleanField()
#     # read_only because this field is managed by django automatically
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)
#
#     def update(self, instance, validated_data):
#         # if no data is passed, use the one that you already have
#         instance.author = validated_data.get('author', instance.author)
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.body = validated_data.get('body', instance.body)
#         instance.location = validated_data.get('location', instance.location)
#         instance.publication_date = validated_data.get('publication_date', instance.publication_date)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
#     def validate(self, data):
#         """ Validator (object level validation: applies on multiple fields)
#          to check if title and body are different"""
#         if data['title'] == data['description']:
#             raise serializers.ValidationError('Title & description must be different from one another')
#         return data
#
#     def validate_title(self, value):
#         """ Validator (field level validation: applies on a field)
#          60 character long for title"""
#         if len(value) < 60:
#             raise serializers.ValidationError('The title must be at least 60 character long')
#         return value
#
#     # to create instance of article
#     def create(self, validated_data):
#         print(validated_data)
#         return Article.objects.create(**validated_data)
