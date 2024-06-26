import ssl
import warnings
from typing import TYPE_CHECKING, Optional

from faststream.exceptions import SetupError
from faststream.security import (
    BaseSecurity,
    SASLPlaintext,
    SASLScram256,
    SASLScram512,
    ssl_not_set_error_msg,
)

if TYPE_CHECKING:
    from faststream.types import AnyDict


def parse_security(security: Optional[BaseSecurity]) -> "AnyDict":
    if security and isinstance(security.ssl_context, ssl.SSLContext):
        raise SetupError(
            "ssl_context in not supported by confluent-kafka-python, please use config instead."
        )

    if security is None:
        return {}
    elif type(security) == BaseSecurity:
        return _parse_base_security(security)
    elif type(security) == SASLPlaintext:
        return _parse_sasl_plaintext(security)
    elif type(security) == SASLScram256:
        return _parse_sasl_scram256(security)
    elif type(security) == SASLScram512:
        return _parse_sasl_scram512(security)
    else:
        raise NotImplementedError(f"KafkaBroker does not support `{type(security)}`.")


def _parse_base_security(security: BaseSecurity) -> "AnyDict":
    return {
        "security_protocol": "SSL" if security.use_ssl else "PLAINTEXT",
    }


def _parse_sasl_plaintext(security: SASLPlaintext) -> "AnyDict":
    if not security.use_ssl:
        warnings.warn(
            message=ssl_not_set_error_msg,
            category=RuntimeWarning,
            stacklevel=1,
        )

    return {
        "security_protocol": "SASL_SSL" if security.use_ssl else "SASL_PLAINTEXT",
        "sasl_mechanism": "PLAIN",
        "sasl_plain_username": security.username,
        "sasl_plain_password": security.password,
    }


def _parse_sasl_scram256(security: SASLScram256) -> "AnyDict":
    return {
        "security_protocol": "SASL_SSL" if security.use_ssl else "SASL_PLAINTEXT",
        "sasl_mechanism": "SCRAM-SHA-256",
        "sasl_plain_username": security.username,
        "sasl_plain_password": security.password,
    }


def _parse_sasl_scram512(security: SASLScram512) -> "AnyDict":
    return {
        "security_protocol": "SASL_SSL" if security.use_ssl else "SASL_PLAINTEXT",
        "sasl_mechanism": "SCRAM-SHA-512",
        "sasl_plain_username": security.username,
        "sasl_plain_password": security.password,
    }
