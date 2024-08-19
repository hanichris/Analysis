import json
from uuid import UUID

from channels.generic.websocket import WebsocketConsumer

from .models import Geofield

class GeoConsumer(WebsocketConsumer):

    def connect(self) -> None:
        self.user = self.scope['user']
        self.accept()

    def receive(self, text_data):
        content = {'msg': '', 'op': '', 'success': None,
                   'error': None, 'content': []}

        data:dict = json.loads(text_data)
        operation = data.get('OP')

        if operation == 'POST':
            create_data = [
                Geofield(
                    user=self.user,
                    feature_id=UUID(feature.get("id")),
                    geometry=feature.get("geometry")
                )
                for feature in data.get("features") # type: ignore
            ]

            created_objects = Geofield.objects.bulk_create(
                create_data,
                update_conflicts=True,
                update_fields=["geometry"],
                unique_fields=["feature_id"]   
            )

            content['msg'] = 'Successfully saved the coordinates into the database'
            content['op'] = "POST",
            content['success'] = True,
            content['content'] = [
                {
                    'geometry': item.geometry,
                    'id': item.feature_id.hex if item.feature_id else None,
                    'properties': {},
                    'type': 'Feature',
                }
                for item in created_objects
            ]

        elif operation == 'GET':
            qs = Geofield.objects.select_related(
                "user"
            ).filter(user__email=self.user)
            content['msg'] = 'Successfully retrieved data from the database'
            content['op'] = 'GET'
            content['success'] = True
            content['content'] = [
                {
                    'geometry': entry.geometry,
                    'id': entry.feature_id.hex if entry.feature_id else None,
                    'properties': {},
                    'type': 'Feature',
                }
                for entry in qs
            ]
        self.send(text_data=json.dumps(content))

    def disconnect(self):
        pass