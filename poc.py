from typing import Dict, Optional
from uuid import uuid1
import os
import json
from requests import Session


HEADER_DATA = {
    "X-Apple-ID-Account-Country": "account_country",
    "X-Apple-ID-Session-Id": "session_id",
    "X-Apple-Session-Token": "session_token",
    "X-Apple-TwoSV-Trust-Token": "trust_token",
    "scnt": "scnt",
}

SESSION_DATA = {}


class CustomSesh(Session):
    def request(self, method, url, **kwargs):  # pyright: ignore
        response = super().request(method, url, **kwargs)

        for header, value in HEADER_DATA.items():
            if response.headers.get(header):
                session_arg = value
                SESSION_DATA.update({session_arg: response.headers.get(header)})

        return response


class ICloud:
    AUTH_ENDPOINT = "https://idmsa.apple.com/appleauth/auth"
    HOME_ENDPOINT = "https://www.icloud.com"
    SETUP_ENDPOINT = "https://setup.icloud.com/setup/ws/1"

    def auth_headers(self, overrides: Optional[Dict[str, str]] = None):
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "X-Apple-OAuth-Client-Id": "d39ba9916b7251055b22c7f910e2ea796ee65e98b2ddecea8f5dde8d9d1a815d",
            "X-Apple-OAuth-Client-Type": "firstPartyAuth",
            "X-Apple-OAuth-Redirect-URI": "https://www.icloud.com",
            "X-Apple-OAuth-Require-Grant-Code": "true",
            "X-Apple-OAuth-Response-Mode": "web_message",
            "X-Apple-OAuth-Response-Type": "code",
            "X-Apple-OAuth-State": client_id,
            "X-Apple-Widget-Key": "d39ba9916b7251055b22c7f910e2ea796ee65e98b2ddecea8f5dde8d9d1a815d",
        }

        if overrides:
            headers.update(overrides)

        return headers


def auth_headers(overrides=None):
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "X-Apple-OAuth-Client-Id": "d39ba9916b7251055b22c7f910e2ea796ee65e98b2ddecea8f5dde8d9d1a815d",
        "X-Apple-OAuth-Client-Type": "firstPartyAuth",
        "X-Apple-OAuth-Redirect-URI": "https://www.icloud.com",
        "X-Apple-OAuth-Require-Grant-Code": "true",
        "X-Apple-OAuth-Response-Mode": "web_message",
        "X-Apple-OAuth-Response-Type": "code",
        "X-Apple-OAuth-State": client_id,
        "X-Apple-Widget-Key": "d39ba9916b7251055b22c7f910e2ea796ee65e98b2ddecea8f5dde8d9d1a815d",
    }

    if overrides:
        headers.update(overrides)
    return headers


AUTH_ENDPOINT = "https://idmsa.apple.com/appleauth/auth"
HOME_ENDPOINT = "https://www.icloud.com"
SETUP_ENDPOINT = "https://setup.icloud.com/setup/ws/1"

s = CustomSesh()

user = {"accountName": os.environ["USER"], "password": os.environ["PASS"]}
client_id = f"auth-{str(uuid1()).lower()}"

if SESSION_DATA.get("client_id"):
    client_id = SESSION_DATA.get("client_id")
else:
    SESSION_DATA.update({"client_id": client_id})

s.headers.update({"Origin": HOME_ENDPOINT, "Referer": "%s/" % HOME_ENDPOINT})

# Intro
data = dict(user)
data["rememberMe"] = True
data["trustTokens"] = []

if SESSION_DATA.get("trust_token"):
    data["trustTokens"] = [SESSION_DATA.get("trust_token")]


headers = auth_headers()

if SESSION_DATA.get("scnt"):
    headers["scnt"] = SESSION_DATA.get("scnt")

if SESSION_DATA.get("session_id"):
    headers["X-Apple-ID-Session-Id"] = SESSION_DATA.get("session_id")

res = s.post(
    f"{AUTH_ENDPOINT}/signin",
    params={"isRememberMeEnabled": "true"},
    data=json.dumps(data),
    headers=headers,
)

print(res)
# ====

data = {
    "accountCountryCode": SESSION_DATA.get("account_country"),
    "dsWebAuthToken": SESSION_DATA.get("session_token"),
    "extended_login": True,
    "trustToken": SESSION_DATA.get("trust_token", ""),
}

res = s.post(f"{SETUP_ENDPOINT}/accountLogin", data=json.dumps(data))
print(res)
print(res.json().keys())

# 2FA
code = input(">>")

data = {"securityCode": {"code": code}}
headers = auth_headers({"Accept": "application/json"})

if SESSION_DATA.get("scnt"):
    headers["scnt"] = SESSION_DATA.get("scnt")

if SESSION_DATA.get("session_id"):
    headers["X-Apple-ID-Session-Id"] = SESSION_DATA.get("session_id")

res = s.post(
    f"{AUTH_ENDPOINT}/verify/trusteddevices/securityCode",
    data=json.dumps(data),
    headers=headers,
)

print(res)
print(res.json())

# Trust Session
headers = auth_headers()

if SESSION_DATA.get("scnt"):
    headers["scnt"] = SESSION_DATA.get("scnt")

if SESSION_DATA.get("session_id"):
    headers["X-Apple-ID-Session-Id"] = SESSION_DATA.get("session_id")

s.get(f"{AUTH_ENDPOINT}/2sv/trust", headers=headers)


# 1. Retrieve pass
# 2. Load cookies and session info

# 3. Start session and auth
#   3a. If session_token exists and is valid => GG
#   3b.

# Trust Session
