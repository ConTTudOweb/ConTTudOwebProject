# from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):

        if self.page_size_query_param:
            if request.query_params.get(self.page_size_query_param, None) == '-1':
                request.GET._mutable = True
                request.GET[self.page_size_query_param] = len(queryset)
                request.GET._mutable = False

        return super().paginate_queryset(queryset, request, view)

    # def get_paginated_response(self, data):
    #     return Response(OrderedDict([
    #         ('count', self.page.paginator.count),
    #         # ('next', self.get_next_link()),
    #         # ('previous', self.get_previous_link()),
    #         ('results', data)
    #     ]))
