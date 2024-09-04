from rest_framework import serializers

from analysis.models import WebhookEvent


class WebhookEventSerializer(serializers.Serializer):
    body = serializers.JSONField()
    event_name = serializers.CharField()
    proccessed = serializers.BooleanField(default=False)
    proccessing_error = serializers.CharField(default='')

    def create(self, validated_data):
        """Create and return a new `WebhookEvent` instance from the validated data.
        """
        return WebhookEvent.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.event_name = validated_data.get('body', instance.event_name)
        instance.proccessed = validated_data.get('proccessed', instance.proccessed)
        instance.proccessing_error = validated_data.get(
            'proccessing_error', instance.proccessing_error
        )

        instance.save()
        return instance