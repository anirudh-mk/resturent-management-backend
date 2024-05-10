from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import QuerySet, Q


class CommonUtils:
    @staticmethod
    def search_and_sort(
        queryset: QuerySet,
        request,
        search_fields,
        sort_fields: dict = None,
    ) -> QuerySet:

        if sort_fields is None:
            sort_fields = {}

        search_query = request.query_params.get("search")
        sort_by = request.query_params.get("sortBy")

        if search_query:
            query = Q()
            for field in search_fields:
                query |= Q(**{f"{field}__icontains": search_query})

            queryset = queryset.filter(query)

        if sort_by:
            sort = sort_by[1:] if sort_by.startswith("-") else sort_by
            if sort_field_name := sort_fields.get(sort):
                if sort_by.startswith("-"):
                    sort_field_name = f"-{sort_field_name}"

                queryset = queryset.order_by(sort_field_name)

            return {
                "queryset": queryset,
            }

        return queryset
