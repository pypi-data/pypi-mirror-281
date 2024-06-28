""" Verify signed responses api"""

import base64
import traceback

import rfc3161ng

from authsign.utils import (
    CERT_DURATION,
    STAMP_DURATION,
    no_older_then,
    format_date,
    load_yaml,
)
from authsign import crypto
from authsign.log import log_assert, log_message, debug_error
from authsign.model import SignedHash


DEFAULT_TRUSTED_ROOTS = "pkg://authsign.trusted/roots.yaml"


# ============================================================================
class Verifier:
    """Verifies signed response from signer to check for validity"""

    def __init__(
        self, trusted_roots_filename=None, cert_duration=None, stamp_duration=None
    ):
        trusted_roots_filename = trusted_roots_filename or DEFAULT_TRUSTED_ROOTS
        log_message("Loading trusted roots from: " + trusted_roots_filename)
        trusted_roots = load_yaml(trusted_roots_filename)

        self.domain_cert_roots = trusted_roots["domain_cert_roots"]
        self.timestamp_cert_roots = trusted_roots["timestamp_cert_roots"]

        self.cert_duration = cert_duration or CERT_DURATION
        self.stamp_duration = stamp_duration or STAMP_DURATION

        log_message(f"{len(self.domain_cert_roots)} Domain Cert Root(s) Loaded")
        log_message(f"{len(self.timestamp_cert_roots)} Timestamp Cert Root(s) Loaded")

    def timestamp_verify(self, text, signature, cert_pem):
        """Verify RFC 3161 timestamp given a cert, signature and text
        Return the timestamp"""
        resp = rfc3161ng.decode_timestamp_response(base64.b64decode(signature))
        tst = resp.time_stamp_token

        # verify timestamp was signed by the existing cert
        try:
            rfc3161ng.check_timestamp(
                tst,
                certificate=cert_pem.encode("ascii"),
                data=text.encode("ascii"),
                hashname="sha256",
            )
        except Exception:
            debug_error(traceback.format_exc())
            return None

        return rfc3161ng.get_timestamp(tst)

    def check_fingerprint(self, cert, trusted, name):
        """Check if cert fingerprint matches one of trusted fingerprints (sha-256 hashes)"""
        fingerprint = crypto.get_fingerprint(cert)

        log_assert(
            fingerprint in trusted,
            f"Trusted {name} Root Cert (sha-256 fingerprint: {fingerprint})",
        )

    def __call__(self, signed_req):
        """Verify signed hash request"""

        if isinstance(signed_req, dict):
            signed_req = SignedHash(**signed_req)

        try:
            log_message(f"Signing Software: {str(signed_req.software)}")

            certs = crypto.validate_cert_chain(signed_req.domainCert.encode("ascii"))
            log_assert(certs, "Verify certificate chain for domain certificate")
            cert = certs[0]

            self.check_fingerprint(certs[-1], self.domain_cert_roots, "Domain")

            public_key = cert.public_key()
            log_assert(
                crypto.verify(signed_req.hash, signed_req.signature, public_key),
                "Verify signature of hash with public key from domain certificate",
            )

            if signed_req.crossSignedCert:
                cs_certs = crypto.validate_cert_chain(
                    signed_req.crossSignedCert.encode("ascii")
                )
                log_assert(
                    cs_certs, "Verify certificate chain for cross-signed certificate"
                )
                cs_public_key = cs_certs[0].public_key()

                log_assert(
                    crypto.verify(signed_req.hash, signed_req.signature, cs_public_key),
                    "Verify signature of hash with public key of cross-signed certificate",
                )

            domain = crypto.get_cert_subject_name(cert)
            domain_fingerprint = crypto.get_fingerprint(cert)

            log_assert(
                domain == signed_req.domain,
                f"Domain Cert Matches Expected: '{domain}' (sha-256 fingerprint: {domain_fingerprint})",
            )

            created = signed_req.created
            log_assert(created, "Parsed signature date")

            log_assert(
                cert.not_valid_before
                <= created
                <= cert.not_valid_before + self.cert_duration,
                f"Verify creation date '{created}' - cert creation date '{cert.not_valid_before}' <= '{self.cert_duration}'",
            )

            timestamp = self.timestamp_verify(
                signed_req.signature, signed_req.timeSignature, signed_req.timestampCert
            )

            log_assert(
                timestamp,
                "Verify timeSignature is a valid timestamp signature of\
 hash signature with timestamp certificate",
            )

            log_assert(
                no_older_then(created, timestamp, self.stamp_duration),
                f"Verify created date '{created}' is no older than {self.stamp_duration}' from '{timestamp}'",
            )

            timestamp_certs = crypto.validate_cert_chain(
                signed_req.timestampCert.encode("ascii")
            )

            log_assert(
                timestamp_certs, "Verify certificate chain for timestamp certificate"
            )

            self.check_fingerprint(
                timestamp_certs[-1], self.timestamp_cert_roots, "Timestamp"
            )

            return {"observer": domain, "timestamp": format_date(timestamp)}

        except Exception:
            debug_error(traceback.format_exc())
            return None
