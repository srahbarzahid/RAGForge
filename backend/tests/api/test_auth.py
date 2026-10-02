from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from app.core import security
from app.main import app

client = TestClient(app)
private_key = ec.generate_private_key(ec.SECP256R1())
user_id = uuid4()
issuer = "https://example.supabase.co/auth/v1"


@pytest.fixture(autouse=True)
def configure_supabase(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    key = SimpleNamespace(key=private_key.public_key())
    jwks_client = SimpleNamespace(get_signing_key_from_jwt=lambda token: key)
    monkeypatch.setattr(security, "_jwks_client", lambda url: jwks_client)


def access_token(**overrides):
    claims = {
        "sub": str(user_id),
        "email": "reader@example.com",
        "iss": issuer,
        "aud": "authenticated",
        "role": "authenticated",
        "exp": datetime.now(UTC) + timedelta(minutes=5),
    }
    claims.update(overrides)
    return jwt.encode(claims, private_key, algorithm="ES256", headers={"kid": "test"})


def test_auth_me_requires_bearer_token():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_auth_me_rejects_malformed_and_badly_signed_tokens():
    for token in (
        "not-a-jwt",
        jwt.encode(
            {
                "sub": str(user_id),
                "iss": issuer,
                "aud": "authenticated",
                "role": "authenticated",
                "exp": datetime.now(UTC) + timedelta(minutes=5),
            },
            ec.generate_private_key(ec.SECP256R1()),
            algorithm="ES256",
            headers={"kid": "test"},
        ),
    ):
        response = client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 401


def test_auth_me_returns_verified_identity():
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token()}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": str(user_id),
        "email": "reader@example.com",
    }


@pytest.mark.parametrize(
    "overrides",
    [
        {"aud": "service_role"},
        {"iss": "https://other.supabase.co/auth/v1"},
        {"role": "anon"},
        {"exp": datetime.now(UTC) - timedelta(minutes=1)},
        {"sub": "not-a-uuid"},
        {"nbf": datetime.now(UTC) + timedelta(minutes=5)},
    ],
)
def test_auth_me_rejects_invalid_claims(overrides):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token(**overrides)}"},
    )
    assert response.status_code == 401


def test_auth_me_requires_project_configuration(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token()}"},
    )
    assert response.status_code == 503
