from enum import Enum


class OAuthType(str, Enum):
    GoogleOAuth = 'GOOGLE_OAUTH'
    FaceBookOAuth = 'FACEBOOK_OAUTH'

    @classmethod
    def values(cls):
        return [value for att_name, value in cls.__members__.items()]