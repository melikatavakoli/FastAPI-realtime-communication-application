from enum import Enum

class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"
    
class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    VOICE = "voice"
    FILE = "file"
    DOCUMENT = "document"
    GIF = "gif"