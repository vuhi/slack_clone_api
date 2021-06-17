from typing import TypedDict


# https://www.python.org/dev/peps/pep-0589/
class Claim(TypedDict):
    id: str
    iss: str
    aud: str
    iat: int
    exp: int


# Check type of dict value
# print([type(k) for k in claims.values()])
