from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class TwitterUser:
    id: int
    name: str
    username: str
    profile_image_url: str = ''
