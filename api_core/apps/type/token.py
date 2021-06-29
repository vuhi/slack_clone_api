import abc

from .claim import Claim


RawToken = str


class IToken(metaclass=abc.ABCMeta):

    class CLAIM:
        ID = 'id'
        ISSUER = 'iss'
        AUDIENCE = 'aud'
        ISSUED_AT = 'iat'
        EXP_TIME = 'exp'

    @abc.abstractmethod
    def sign(self, user_id: str) -> RawToken:
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, raw_token: str, should_verify=True) -> Claim:
        raise NotImplementedError



