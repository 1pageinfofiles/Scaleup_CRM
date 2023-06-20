import base64
from django import template

register = template.Library()

@register.filter
def base64_encode(value):
    id_bytes = str(value).encode('utf-8')
    encoded_id_bytes = base64.b64encode(id_bytes)
    encoded_id = encoded_id_bytes.decode('utf-8')
    return encoded_id

@register.filter
def base64_decode(value):
    id_bytes = value.encode('utf-8')
    decoded_id_bytes = base64.b64decode(id_bytes)
    decoded_id = decoded_id_bytes.decode('utf-8')
    return decoded_id