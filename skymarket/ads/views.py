from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema

from ads.models import Ad, Comment
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer

from ads.filters import AdTitleFilter
from ads.permissions import IsOwner, IsAdmin


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


@extend_schema_view(
    list=extend_schema(
        description="Return a list of advertisements sorted by creation date",
        summary="A list of advertisements"
    ),
    retrieve=extend_schema(
        description="Return a detail advertisement",
        summary="A detail advertisement"
                           ),
    create=extend_schema(
        description="Add a new advertisement",
        summary="Add advertisement"
    ),
    update=extend_schema(
        description="Updates all fields of the current advertisement",
        summary="Update current advertisement"
    ),
    partial_update=extend_schema(
        description="Updates chosen fields of the current advertisement",
        summary="Partially update current advertisement"
    ),
    destroy=extend_schema(
        description="Deletes current advertisement",
        summary="Delete advertisement"
    ),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()

    default_serializer = AdDetailSerializer
    serializers = {"list": AdSerializer}

    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdTitleFilter

    default_permission = [IsAuthenticated]
    permissions = {
        "list": [AllowAny, ],
        "retrieve": [IsAuthenticated, ],
        "update": [IsAuthenticated, IsOwner | IsAdmin],
        "destroy": [IsAuthenticated, IsOwner | IsAdmin],
    }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    @action(detail=False, url_path="me", serializer_class=AdSerializer)
    def me(self, request):
        ads = Ad.objects.filter(author_id=request.user.pk)
        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        description="Returns a list of all comments",
        summary="A list of comments"
    ),
    retrieve=extend_schema(
        description="Returns a detail comment",
        summary="A detail comment"
    ),
    create=extend_schema(
        description="Adds a new comment",
        summary="Add comment"
    ),
    update=extend_schema(
        description="Updates all fields of the certain comment",
        summary="Update comment"
    ),
    partial_update=extend_schema(
        description="Updates chosen fields of the certain comment",
        summary="Partially update comment"
    ),
    destroy=extend_schema(
        description="Deletes the comment from the database",
        summary="Delete comment"
    ),
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = AdPagination
    default_permission = [IsAuthenticated]
    permissions = {
        "list": [AllowAny, ],
        "retrieve": [IsAuthenticated, ],
        "update": [IsAuthenticated, IsOwner | IsAdmin],
        "destroy": [IsAuthenticated, IsOwner | IsAdmin],
    }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]
