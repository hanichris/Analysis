from rest_framework import serializers

from analysis.models import WebhookEvent


class WebhookEventSerializer(serializers.Serializer):
    body = serializers.JSONField()
    event_name = serializers.CharField()
    processed = serializers.BooleanField(default=False)
    processing_error = serializers.CharField(default='')

    def create(self, validated_data):
        """Create and return a new `WebhookEvent` instance from the validated data.
        """
        return WebhookEvent.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.event_name = validated_data.get('event_name', instance.event_name)
        instance.processed = validated_data.get('processed', instance.processed)
        instance.processing_error = validated_data.get(
            'processing_error', instance.processing_error
        )

        instance.save()
        return instance