import json
from uuid import UUID

from django.core import serializers
from django.db import transaction

from channels.generic.websocket import WebsocketConsumer

from .models import Geofield

class GeoConsumer(WebsocketConsumer):

    def connect(self) -> None:
        self.user = self.scope['user']
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        create_data = [
            Geofield(
                user=self.user,
                feature_id=UUID(feature.get("id")),
                geometry=feature.get("geometry")
            )
            for feature in data.get("features")
        ]

        with transaction.atomic():
            created_objects = Geofield.objects.bulk_create(
                create_data,
                update_conflicts=True,
                update_fields=["geometry"],
                unique_fields=["feature_id"]   
            )

        content = {
            'msg': 'Successfully saved the coordinates into the database',
            'op': 'Save coordinates',
            'success': True,
            'error': None,
            'data': [
                {
                    'geometry': item.geometry,
                    # 'id': item.feature_id.hex if item.feature_id else None,
                    'properties': {},
                    'type': 'Feature',
                }
                for item in created_objects
            ]
        }
        self.send(text_data=json.dumps(content))

    def disconnect(self):
        pass