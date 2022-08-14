# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import secrets
from base64 import urlsafe_b64encode
from enum import Enum
from hashlib import sha256
from urllib.parse import parse_qs, urlencode, urlparse

import httpx
from pydantic import BaseModel

from . import __CLIENT_ID__, headers

__MSA_AUTHORIZATION_ENDPOINT__ = (
    "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
)
__MSA_TOKEN_ENDPOINT__ = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
__XBOXLIVE_AUTH_ENDPOINT__ = "https://user.auth.xboxlive.com/user/authenticate"
__XSTS_AUTHORIZATION_ENDPOINT__ = "https://xsts.auth.xboxlive.com/xsts/authorize"
__MINECRAFT_AUTH_ENDPOINT__ = (
    "https://api.minecraftservices.com/authentication/login_with_xbox"
)
__MINECRAFT_PROFILE_ENDPOINT__ = "https://api.minecraftservices.com/minecraft/profile"
__SCOPE__ = "XboxLive.signin offline_access"
__REDIRECT_URI__: str = "http://localhost:3003"


class _CodeChallengeMethod(str, Enum):
    plain = "plain"
    S256 = "S256"


class _PKCE_Data(BaseModel):
    code_verifier: str
    code_challenge: str
    code_challenge_method: _CodeChallengeMethod


class _LoginData(BaseModel):
    uri: str
    state: str
    code_verifier: str


class _OAuth2Token(BaseModel):
    access_token: str
    refresh_token: str


class _Xui(BaseModel):
    uhs: str


class _DisplayClaims(BaseModel):
    xui: list[_Xui]


class _XBLResponse(BaseModel):
    Token: str
    DisplayClaims: _DisplayClaims


class _XSTSResponse(BaseModel):
    Token: str


class _MinecraftResponse(BaseModel):
    access_token: str


class _MinecraftProfile(BaseModel):
    id: str
    name: str


class Account(BaseModel):
    microsoft_refresh_token: str
    minecraft_access_token: str
    minecraft_username: str


class AccountEntry(BaseModel):
    minecraft_id: str
    account: Account


def _generate_pkce_data() -> _PKCE_Data:
    """
    Generates the PKCE code challenge and code verifier
    """
    code_verifier = secrets.token_urlsafe(128)[:128]
    code_challenge = urlsafe_b64encode(
        sha256(code_verifier.encode("ascii")).digest()
    ).decode("ascii")[:-1]
    code_challenge_method = _CodeChallengeMethod.S256

    return _PKCE_Data(
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
    )


def _generate_state() -> str:
    """
    Generates a random state
    """
    return secrets.token_urlsafe(16)


def get_login_data() -> _LoginData:
    pkce_data = _generate_pkce_data()
    state = _generate_state()

    data = {
        "client_id": __CLIENT_ID__,
        "response_type": "code",
        "redirect_uri": __REDIRECT_URI__,
        "response_mode": "query",
        "scope": __SCOPE__,
        "state": state,
        "code_challenge": pkce_data.code_challenge,
        "code_challenge_method": pkce_data.code_challenge_method.value,
    }

    uri = (
        urlparse(__MSA_AUTHORIZATION_ENDPOINT__)
        ._replace(query=urlencode(data))
        .geturl()
    )

    return _LoginData(uri=uri, state=state, code_verifier=pkce_data.code_verifier)


def _get_minecraft_account_data(msa_token: _OAuth2Token) -> AccountEntry:
    http_client = httpx.Client(
        headers=headers
        | {"Content-Type": "application/json", "Accept": "application/json"}
    )

    # Authenticate with Xbox Live
    data = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={msa_token.access_token}",
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT",
    }
    response = http_client.post(__XBOXLIVE_AUTH_ENDPOINT__, json=data)
    xbl_response = _XBLResponse.parse_raw(response.content)

    # Authenticate with XSTS
    data = {
        "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbl_response.Token]},
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT",
    }
    response = http_client.post(__XSTS_AUTHORIZATION_ENDPOINT__, json=data)
    xsts_response = _XSTSResponse.parse_raw(response.content)

    # Authenticate with Minecraft
    data = {
        "identityToken": f"XBL3.0 x={xbl_response.DisplayClaims.xui[0].uhs};{xsts_response.Token}"
    }
    response = http_client.post(__MINECRAFT_AUTH_ENDPOINT__, json=data)
    minecraft_response = _MinecraftResponse.parse_raw(response.content)

    # Get Minecraft profile
    http_client.headers["Authorization"] = f"Bearer {minecraft_response.access_token}"
    response = http_client.get(__MINECRAFT_PROFILE_ENDPOINT__)
    minecraft_profile = _MinecraftProfile.parse_raw(response.content)

    account = Account(
        microsoft_refresh_token=msa_token.refresh_token,
        minecraft_access_token=minecraft_response.access_token,
        minecraft_username=minecraft_profile.name,
    )

    return AccountEntry(minecraft_id=minecraft_profile.id, account=account)


def login(authorization_response: str, state: str, code_verifier: str) -> AccountEntry:
    http_client = httpx.Client(
        headers=headers
        | {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
    )

    url = urlparse(authorization_response)
    query = parse_qs(url.query)
    assert query["state"][0] == state

    data = {
        "client_id": __CLIENT_ID__,
        "scope": __SCOPE__,
        "code": query["code"][0],
        "redirect_uri": __REDIRECT_URI__,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }
    response = http_client.post(__MSA_TOKEN_ENDPOINT__, data=data)
    msa_token = _OAuth2Token.parse_raw(response.content)
    account_entry = _get_minecraft_account_data(msa_token)

    return account_entry


def refresh(account: Account) -> Account:
    http_client = httpx.Client(
        headers=headers
        | {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
    )

    data = {
        "client_id": __CLIENT_ID__,
        "scope": __SCOPE__,
        "refresh_token": account.microsoft_refresh_token,
        "grant_type": "refresh_token",
    }

    response = http_client.post(__MSA_TOKEN_ENDPOINT__, data=data)
    msa_token = _OAuth2Token.parse_raw(response.content)
    account_entry = _get_minecraft_account_data(msa_token)

    return account_entry.account
