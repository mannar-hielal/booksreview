from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from books.models import Review, Book
from .pagination import SmallSetPagination
from .permissions import IsAdminUserOrReadOnly, IsReviewAuthorOrReadOnly
from .serializers import (
    # ArticleSerializer,
    # JournalistSerializer,
    BookSerializer,
    ReviewSerializer
)


# create or list functionality? according to the request
# @api_view(['GET', 'POST'])
# def article_list_create_api_view(request):
#     if request.method == 'GET':
#         articles = Article.objects.filter(active=True)
#         # feed the qs to the articleserializer to return the data as response
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         # inistialize serializer passing him the data of the request
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # if serializer is not valid
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def article_detail_api_view(request, pk):
#     # check if pk is valid
#     try:
#         article = Article.objects.get(pk=pk)
#     except article.DoesNotExist:
#         # define customized error message
#         return Response({'error': {
#             'code': 404,
#             'message': 'Article not found!'}},
#             status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ArticleListCreateAPIView(APIView):
#     def get(self, request):
#         articles = Article.objects.filter(active=True)
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # class ArticleDetailAPIView(APIView):
# #     # instead of try except in the functional method
# #     def get_object(self, pk):
# #         article = get_object_or_404(Article, pk=pk)
# #         return article
# #
# #     def get(self, request, pk):
# #         article = self.get_object(pk)
# #         # call serializer and return its data
# #         serializer = ArticleSerializer(article)
# #         return Response(serializer.data)
# #
# #     def put(self, request, pk):
# #         article = self.get_object(pk)
# #         serializer = ArticleSerializer(article, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def delete(self, request, pk):
# #         article = self.get_object(pk)
# #         article.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
# #
#
# class JournalistCreateAPIView(APIView):
#     def get(self, request):
#         journalists = Journalist.objects.all()
#         serializer = JournalistSerializer(journalists,
#                                           many=True,
#                                           context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = JournalistSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# mixins are used to provide further functionalities
# they provide action methods: list(), create()
# rather than defining get(), post() as in APIView
# class BookListCreateAPIView(mixins.ListModelMixin,
#                             mixins.CreateModelMixin,
#                             generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# refactor using concrete classes
# because of thier abstraction level they are teh fastest
# to write and the most magical
# i.d RetrieveUPdateAPIView extends GenericAPIView
# and RetrieveModelMixin + UpdateModelMixin
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [IsAdminUserOrReadOnly]
    # setting pagination per view, we must order here
    pagination_class = SmallSetPagination
    name = 'book-list'


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAdminUserOrReadOnly]
    name = 'book-detail'


class ReviewList(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    name = 'review-list'

    # we need to link to a book because of one-to-many rs
    # here we are linking the passed book with the newely
    # created instance of bookreview
    # p.s: pay attention to url creation
    def perform_create(self, serializer):
        # the kwargs that's coming from the url path
        book_pk = self.kwargs.get("pk")
        book = get_object_or_404(Book, pk=book_pk)
        review_author = self.request.user

        # check if author already made a review
        review_qs = Review.objects.filter(book=book,
                                          review_author=review_author)
        if review_qs.exists():
            raise ValidationError('You have already made a review!')
        serializer.save(book=book, review_author=review_author)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # allow only review owners to edit this
    permission_classes = [IsReviewAuthorOrReadOnly]
    name = 'review-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'books': reverse(BookList.name, request=request),
        })
