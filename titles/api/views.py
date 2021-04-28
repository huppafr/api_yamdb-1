from django.db import models
from rest_framework import generics
# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters, mixins, pagination, viewsets, authentication
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from titles.models import Category, Ganre, Title
from .permission import IsOwnerOrReadOnly, IsAdmin, IsAdminOrReadOnly, IsSUandAdmin
from rest_framework.decorators import action

from .serializers import CategorySerializer, GanreSerializer, TitleReadSerializer, TitleWriteSerializer 

class GetViewSet(mixins.ListModelMixin):
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class ParrentViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    pass


class PageNumberSetPagination(pagination.PageNumberPagination):
    '''Кастомная пагинация для TitleViewSet'''
    page_size = 6
    page_size_query_param = 'page_size'


class CategoryViewSet(ParrentViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['name', ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = PageNumberSetPagination


    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return HttpResponse(status=404)
        return HttpResponse(status=204)


class GanreViewSet(ParrentViewSet):
    queryset = Ganre.objects.all()
    serializer_class = GanreSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['name', ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = PageNumberSetPagination
    authentication_classes = [authentication.TokenAuthentication]


    @action(detail=True, methods=['post'], permission_classes=[IsSUandAdmin])
    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return HttpResponse(status=404)
        return HttpResponse(status=204)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleReadSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['name', ]
    pagination_class = PageNumberSetPagination

    def get_serializer_class(self):
        actions = ['list', 'retrieve']
        if self.action in actions:
            return TitleReadSerializer
        return TitleWriteSerializer

    # @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def perform_create(self, serializer):
        # if serializer.is_valid():
        # if self.request.method == 'POST':
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

    # def get_queryset(self):
    #     return Title.objects.filter(title_id=self.kwargs['title_id'])



    # def get_queryset(self):
    #     object = get_object_or_404(Title, pk=self.kwargs.get("id"))
    #     queryset = object.titles.all()
    #     return queryset





# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['group', ]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class GroupViewSet(GetOrCreateViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, ]
#     search_fields = ['user__username']

#     def perform_create(self, serializer):
#         serializer.save()


# class CommentViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     serializer_class = CommentSerializer

#     def perform_create(self, serializer):
#         post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
#         serializer.save(author=self.request.user, post=post)

#     def get_queryset(self):
#         post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
#         queryset = post.comments.all()
#         return queryset


# class FollowViewSet(GetOrCreateViewSet):
#     serializer_class = FollowSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['user__username', 'following__username']

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def get_queryset(self):
#         return self.request.user.following.all()
