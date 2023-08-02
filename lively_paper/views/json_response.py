import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class JsonObjectResponse(JsonResponse):

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs):
        data_string = json.dumps(data, default=lambda o: o.__dict__, ensure_ascii=False)
        data = json.loads(data_string)
        super().__init__(data, encoder, safe, json_dumps_params, **kwargs)
