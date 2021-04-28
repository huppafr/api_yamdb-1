from rest_framework import pagination
from rest_framework.response import Response

from titles.models import Title, Ganre, Category


class CustomTitlePagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({

            'ganre': Ganre.objects.all(),
            'category': Category.objects.all()
        })