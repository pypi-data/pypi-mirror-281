# flareec/dotedrunes/__init__.py

from .flare_encoder import FlareEncoder

_encoder = FlareEncoder()

def encode(text):
    return _encoder.encode(text)

def crack(encoded_text):
    return _encoder.decode(encoded_text)
