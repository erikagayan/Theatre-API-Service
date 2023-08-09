from rest_framework import serializers
from theatre.models import Play


class PlaySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True)
    description = serializers.IntegerField()

    def create(self, validated_data):
        return Play.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.info)
        instance.description = validated_data.get("description", instance.description)

        instance.save()
        return instance
