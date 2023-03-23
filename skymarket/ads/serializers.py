from rest_framework import serializers

from ads.models import Ad, Comment
from users.models import User


# TODO Сериалайзеры. Предлагаем Вам такую структуру, однако вы вправе использовать свою

class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source="author.first_name", required=False)
    author_last_name = serializers.CharField(source="author.last_name", required=False)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author_id"] = request.user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get("request").user
        validated_data["author_id"] = user

        return super().update(instance, validated_data)

    class Meta:
        model = Comment
        fields = "__all__"


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["pk", "image", "title", "price", "description"]


class AdDetailSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="author.phone", required=False)
    author_first_name = serializers.CharField(source="author.first_name", required=False)
    author_last_name = serializers.CharField(source="author.last_name", required=False)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author_id"] = request.user.pk
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get("request").user
        validated_data["author_id"] = user
        validated_data['ad'] = instance.ad

        return super().update(instance, validated_data)

    class Meta:
        model = Ad
        fields = ["pk", "image", "title", "price", "phone", "description", "author_first_name", "author_last_name",
                  "author_id"]
