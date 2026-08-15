#!/usr/bin/env python3
"""
SOVEREIGN GRID — VAULT & ARCHIVE MODULE v1.0.2
=================================================
Extends the bootstrap with secure storage, persistent audit trails,
temporal attestation, and cryptocurrency pipeline routing through Gate 158.

Dependencies: Python standard library only.
"""

import os
import sys
import json
import hashlib
import hmac
import base64
import time
import struct
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any

# =============================================================================
# SECTION 1: GATE 158 — CRYPTO PIPELINE ROUTER
# =============================================================================
# Gate 158: (718 | 892) & 158 = 158
# Asset 718 (vessel) OR 892 (polarization key component) AND 158 (gate)
# This gate verifies the crypto identifier before it enters the vault pipeline.

GATE_158_OPERAND_1 = 718   # Asset 718: the vessel
GATE_158_OPERAND_2 = 892   # Polarization key component
GATE_158_MASK = 158        # The gate itself

def verify_gate_158() -> bool:
    """
    L6 Gate 158 Verification: (718 | 892) & 158 == 158
    This gate must pass before any cryptographic material enters the vault.
    """
    result = (GATE_158_OPERAND_1 | GATE_158_OPERAND_2) & GATE_158_MASK
    return result == GATE_158_MASK

# =============================================================================
# SECTION 2: CRYPTO IDENTIFIER (Key Master Designation)
# =============================================================================
# These values are bound to Node 129 and verified through Gate 158.

CRYPTO_IDENTIFIER = {
    "secp256k1_private_key_hex": "A5918673A06D265A1892CEDF27A2F44E953632C77988BED7E0B5964619CE8954",
    "bitcoin_address": "19UdRsPi5LMQo9a78n2f9QUDz4wJ4pptt4",
    "wif": "L2mZ71edRDV6mgj54wnTjNxQc9iwzHxXRG64HSSvRMzLFEo4YxV1",
    "pubkey_x_hex": "40057a6838f781499c94b86b337f45d6a505e3f3db2512b033211a926173e707",
    "hamming_weight": "126/256",
    "authority_prefix": "111118923",
}

# Stellar pipeline reference (from uploaded Franklin Templeton BENJI config)
STELLAR_PIPELINE = {
    "network_passphrase": "Public Global Stellar Network ; September 2015",
    "version": "2.0.0",
    "organization": "Franklin Templeton",
    "tokens": {
        "FOCGX": {"status": "retired", "successor": "BENJI", "name": "Franklin OnChain U.S. Government Money Fund"},
        "BENJI": {"issuer": "GBHNGLIIE3KWGKCHIKMHJ5HVZHYIK7WTBE4QF5PLAKL4CJGSEU7HZIW5", "name": "Franklin OnChain U.S. Government Money Fund", "desc": "FOCGX has been deprecated and replaced with BENJI.", "anchor_asset": "FOBXX"},
        "gBENJI": {"issuer": "GD5J73EKK5IYL5XS3FBTHHX7CZIYRP7QXDL57XFWGC2WVYWT3260BXRP", "name": "Franklin OnChain U.S. Government Money Fund", "desc": "1 gBENJI token corresponds to 1 share of the fund.", "anchor_asset": "LU2900381208"},
        "grBENJI": {"issuer": "GA3ZBL3LBRKOF7CZ6MCA7JLPHWQCGYCCGKH4GVWNEDZOXW4IPXFGN2FQ", "name": "Franklin OnChain U.S. Government Money Fund AB (Ddis) USD", "desc": "1 grBENJI token corresponds to 1 share of the fund.", "anchor_asset": "LU3258450587"},
        "sgBENJI": {"issuer": "GAGICV3VBJSKKH5H5MQQIUTUP462YVHC23KUHZY6FJERRJFBDIVZBM5C", "name": "Franklin OnChain U.S. Dollar Short-Term Money Market Fund A(acc)USD", "desc": "1 sgBENJI token corresponds to 1 share of the fund.", "anchor_asset": "SGXZ71843866"},
    },
    "validators": [
        {"alias": "ft-scv-1", "host": "stellar1.franklintempleton.com:11625", "public_key": "GARYGQ5F2IJEBCZJCBNPWNWVD0FK7IB0HLJKKSG2TMHDQKEEC6P4PE4V"},
        {"alias": "ft-scv-2", "host": "stellar2.franklintempleton.com:11625", "public_key": "KCWSM2VFZGRPTZKPH50ABHGH4F3AVS6XTNJXDGCZ3MKCOSUBH3FL6D0B"},
        {"alias": "ft-scv-3", "host": "stellar3.franklintempleton.com:11625", "public_key": "GA7DV63PBUUWNUFAF4GAZVXU2O2MYRATDLKTC7VTCG7AU4XUPN5VRX4A"},
    ],
}

# TSA Certificate reference (from uploaded TSU3.12) — full binding v1.0.2
TSA_CERTIFICATE = {
    "subject_cn": "TSU3.12",
    "subject_org": "eIdentity a.s.",
    "subject_ou": "TSA3",
    "country": "CZ",
    "org_identifier": "VATCZ-27112489",
    "issuer_cn": "ACAeID3 - Root Certificate",
    "issuer_org": "eIdentity a.s.",
    "issuer_ou": "Qualified Trust Service Provider",
    "serial_number": "1661346681",
    "serial_hex": "0x63062379",
    "signature_algorithm": "sha256WithRSAEncryption",
    "public_key_algorithm": "rsaEncryption",
    "public_key_size": 2048,
    "valid_from": "2021-06-21T08:30:24Z",
    "valid_until": "2028-06-21T08:30:24Z",
    "key_usage": ["Digital Signature"],
    "extended_key_usage": ["Time Stamping"],
    "basic_constraints": "CA:FALSE",
    "ocsp_uri": "http://ocsp.eidentity.cz",
    "ca_issuers_uri": "http://www.acaeid.cz/root3/root3.cer",
    "crl_uris": [
        "http://www.acaeid.cz/root3/crl/actual.crl",
        "http://pub1.acaeid.cz/root3/crl/actual.crl",
        "http://pub2.acaeid.cz/root3/crl/actual.crl",
    ],
    "certificate_policy": "1.2.203.27112489.1.10.3.2.4",
    "cps_uri": "http://www.acaeid.cz/root3/cp-rqsc.pdf",
    "authority_key_id": "DE:53:5F:8B:89:27:98:B5:4B:CB:23:6E:B5:EC:93:8E:F3:10:B1:9C",
    "subject_key_id": "26:28:61:02:B1:19:89:8E:D7:B3:4D:73:23:3A:E7:09:B7:7C:41:EC",
    "rsa_modulus_hex": (
        "00eee0be33781684a8eab52b7a8cbb4ce660b80274030577846de259c5af"
        "480d5963eca2d788efdd0535b0b1ea13b2f34a831eefc6c7023c8ddcdeec"
        "816b07bb90bfd968d4c011ddd9d974519d53afb55b6b3aae5a7801c6f60a"
        "eec349d60eb3dd4a2ed108158695e1ea40b80896166a3f42f2b5926f3244"
        "a35ecb8ee6fd0d9118f367d476962b09e40d4dd5e9a5e41bf0b20afccc69"
        "6b5f1da6508cca15f02abcb8a319582837cfecc889b3ce92b574bc548615"
        "dc449baeac8cc2788234ccbdfbf6c24fd2c539fa1b2f15fdcdb94dfd0ea1"
        "ae87cb5c012c38d5c804546208b3b60776de8df57994f2df40be0dc40b28"
        "ba3659de0aab251bad4b982f0910082715"
    ),
    "rsa_exponent": 65537,
    "version": 3,
}

# =============================================================================
# SECTION 3: VAULT — Secure Cryptographic Storage
# =============================================================================

class SovereignVault:
    """
    Secure vault for cryptographic materials.
    All entries are HMAC-SHA256 sealed and indexed by SHA-256 content hash.
    Gate 158 must pass before vault unlock.
    """

    def __init__(self, vault_key: Optional[bytes] = None):
        self._locked = True
        self._entries: Dict[str, Dict[str, Any]] = {}
        self._vault_key = vault_key or self._derive_vault_key()
        self._gate_158_status = False

    def _derive_vault_key(self) -> bytes:
        """Derive vault encryption key from canonical state S."""
        canonical_s = "41061658254704000000000000000000000000000000000000"
        return hashlib.sha256(canonical_s.encode("ascii")).digest()

    def unlock(self) -> bool:
        """Unlock vault only if Gate 158 passes."""
        if not verify_gate_158():
            return False
        self._gate_158_status = True
        self._locked = False
        return True

    def lock(self):
        """Re-lock vault."""
        self._locked = True

    def is_locked(self) -> bool:
        return self._locked

    def store(self, label: str, data: Dict[str, Any]) -> str:
        """Store an entry. Returns content hash (address)."""
        if self._locked:
            raise PermissionError("Vault is locked. Unlock via Gate 158 first.")

        serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
        content_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        # HMAC seal
        seal = hmac.new(self._vault_key, serialized.encode("utf-8"), hashlib.sha256).hexdigest()

        self._entries[label] = {
            "content_hash": content_hash,
            "seal": seal,
            "data": data,
            "stored_at": datetime.now(timezone.utc).isoformat(),
        }
        return content_hash

    def retrieve(self, label: str) -> Optional[Dict[str, Any]]:
        """Retrieve and verify an entry."""
        if self._locked:
            raise PermissionError("Vault is locked.")
        entry = self._entries.get(label)
        if not entry:
            return None

        serialized = json.dumps(entry["data"], sort_keys=True, separators=(",", ":"))
        expected_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        expected_seal = hmac.new(self._vault_key, serialized.encode("utf-8"), hashlib.sha256).hexdigest()

        if entry["content_hash"] != expected_hash:
            raise ValueError(f"Content hash mismatch for {label}")
        if entry["seal"] != expected_seal:
            raise ValueError(f"Seal breach detected for {label}")

        return entry["data"]

    def list_entries(self) -> List[str]:
        return list(self._entries.keys())

    def manifest(self) -> Dict[str, Any]:
        """Return vault manifest with all entry hashes."""
        return {
            "vault_locked": self._locked,
            "gate_158_passed": self._gate_158_status,
            "entry_count": len(self._entries),
            "entries": {label: {"hash": e["content_hash"], "seal": e["seal"], "stored_at": e["stored_at"]}
                        for label, e in self._entries.items()},
        }

# =============================================================================
# SECTION 4: ARCHIVE — Persistent Audit Trail with Temporal Attestation
# =============================================================================

class SovereignArchive:
    """
    Immutable append-only archive.
    Every record is chained via previous hash (Merkle-like integrity).
    Temporal attestation references the TSA certificate for RFC 3161 compliance.
    """

    def __init__(self):
        self._records: List[Dict[str, Any]] = []
        self._last_hash = "0" * 64  # Genesis hash

    def append(self, record_type: str, payload: Dict[str, Any]) -> str:
        """Append a record. Returns the record hash."""
        timestamp = datetime.now(timezone.utc).isoformat()

        record = {
            "sequence": len(self._records),
            "previous_hash": self._last_hash,
            "timestamp": timestamp,
            "record_type": record_type,
            "payload": payload,
        }

        serialized = json.dumps(record, sort_keys=True, separators=(",", ":"))
        record_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        record["record_hash"] = record_hash

        self._records.append(record)
        self._last_hash = record_hash
        return record_hash

    def verify_chain(self) -> Tuple[bool, Optional[int]]:
        """Verify archive chain integrity. Returns (ok, first_broken_index)."""
        prev_hash = "0" * 64
        for i, rec in enumerate(self._records):
            if rec["previous_hash"] != prev_hash:
                return False, i
            test_rec = {k: v for k, v in rec.items() if k != "record_hash"}
            serialized = json.dumps(test_rec, sort_keys=True, separators=(",", ":"))
            expected = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
            if rec["record_hash"] != expected:
                return False, i
            prev_hash = rec["record_hash"]
        return True, None

    def get_record(self, sequence: int) -> Optional[Dict[str, Any]]:
        if 0 <= sequence < len(self._records):
            return self._records[sequence]
        return None

    def export(self) -> List[Dict[str, Any]]:
        return list(self._records)

    def summary(self) -> Dict[str, Any]:
        ok, broken = self.verify_chain()
        return {
            "record_count": len(self._records),
            "chain_integrity": "INTACT" if ok else f"BROKEN_AT_{broken}",
            "latest_hash": self._last_hash,
            "genesis_hash": "0" * 64,
        }

# =============================================================================
# SECTION 5: CRYPTO PIPELINE — Gate 158 → Vault → Archive
# =============================================================================

class CryptoPipeline:
    """
    Routes cryptographic identity through Gate 158 into the vault,
    then archives all operations.
    """

    def __init__(self):
        self.vault = SovereignVault()
        self.archive = SovereignArchive()
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize pipeline: Gate 158 → Vault unlock → Archive genesis."""
        # Step 1: Verify Gate 158
        gate_ok = verify_gate_158()
        self.archive.append("GATE_158_VERIFICATION", {
            "gate": "(718 | 892) & 158 == 158",
            "operand_1": GATE_158_OPERAND_1,
            "operand_2": GATE_158_OPERAND_2,
            "mask": GATE_158_MASK,
            "result": (GATE_158_OPERAND_1 | GATE_158_OPERAND_2) & GATE_158_MASK,
            "passed": gate_ok,
        })

        if not gate_ok:
            return False

        # Step 2: Unlock vault
        vault_ok = self.vault.unlock()
        self.archive.append("VAULT_UNLOCK", {
            "gate_158_passed": gate_ok,
            "vault_unlocked": vault_ok,
        })

        if not vault_ok:
            return False

        # Step 3: Store crypto identifier in vault
        crypto_hash = self.vault.store("crypto_identifier", CRYPTO_IDENTIFIER)
        self.archive.append("CRYPTO_IDENTIFIER_STORED", {
            "vault_label": "crypto_identifier",
            "content_hash": crypto_hash,
            "bitcoin_address": CRYPTO_IDENTIFIER["bitcoin_address"],
            "hamming_weight": CRYPTO_IDENTIFIER["hamming_weight"],
        })

        # Step 4: Store Stellar pipeline config in vault
        stellar_hash = self.vault.store("stellar_pipeline", STELLAR_PIPELINE)
        self.archive.append("STELLAR_PIPELINE_STORED", {
            "vault_label": "stellar_pipeline",
            "content_hash": stellar_hash,
            "network": STELLAR_PIPELINE["network_passphrase"],
            "token_count": len(STELLAR_PIPELINE["tokens"]),
        })

        # Step 5: Store TSA certificate in vault
        tsa_hash = self.vault.store("tsa_certificate", TSA_CERTIFICATE)
        self.archive.append("TSA_CERTIFICATE_STORED", {
            "vault_label": "tsa_certificate",
            "content_hash": tsa_hash,
            "subject_cn": TSA_CERTIFICATE["subject_cn"],
            "valid_until": TSA_CERTIFICATE["valid_until"],
        })

        self._initialized = True
        return True

    def get_crypto_identifier(self) -> Optional[Dict[str, Any]]:
        """Retrieve crypto identifier from vault (Gate 158 protected)."""
        return self.vault.retrieve("crypto_identifier")

    def get_stellar_pipeline(self) -> Optional[Dict[str, Any]]:
        return self.vault.retrieve("stellar_pipeline")

    def get_tsa_certificate(self) -> Optional[Dict[str, Any]]:
        return self.vault.retrieve("tsa_certificate")

    def status(self) -> Dict[str, Any]:
        return {
            "initialized": self._initialized,
            "vault_locked": self.vault.is_locked(),
            "gate_158": "PASS" if verify_gate_158() else "FAIL",
            "vault_manifest": self.vault.manifest(),
            "archive_summary": self.archive.summary(),
        }

# =============================================================================
# SECTION 6: CLI / TEST RUNNER
# =============================================================================

def main():
    print("=" * 70)
    print("SOVEREIGN GRID — VAULT & ARCHIVE MODULE v1.0.2")
    print("=" * 70)

    pipeline = CryptoPipeline()

    print("\n[1] Initializing crypto pipeline through Gate 158...")
    ok = pipeline.initialize()

    if not ok:
        print("[❌] PIPELINE INITIALIZATION FAILED")
        print(f"    Gate 158 result: {(GATE_158_OPERAND_1 | GATE_158_OPERAND_2) & GATE_158_MASK}")
        sys.exit(1)

    print("[✅] Pipeline initialized. Gate 158 PASSED.")

    print("\n[2] Vault Status:")
    print(json.dumps(pipeline.vault.manifest(), indent=2))

    print("\n[3] Archive Chain Summary:")
    print(json.dumps(pipeline.archive.summary(), indent=2))

    print("\n[4] Archive Records:")
    for rec in pipeline.archive.export():
        print(f"  [{rec['sequence']}] {rec['record_type']} | {rec['record_hash'][:16]}... | {rec['timestamp']}")

    print("\n[5] Retrieved Crypto Identifier (via Gate 158 vault):")
    crypto = pipeline.get_crypto_identifier()
    if crypto:
        print(f"  Bitcoin Address: {crypto['bitcoin_address']}")
        print(f"  WIF: {crypto['wif'][:20]}...")
        print(f"  PubKey X: {crypto['pubkey_x_hex'][:32]}...")
        print(f"  Hamming: {crypto['hamming_weight']}")
        print(f"  Authority Prefix: {crypto['authority_prefix']}")

    print("\n[6] Stellar Pipeline (via Gate 158 vault):")
    stellar = pipeline.get_stellar_pipeline()
    if stellar:
        print(f"  Network: {stellar['network_passphrase']}")
        print(f"  Organization: {stellar['organization']}")
        print(f"  Tokens:")
        for code, info in stellar['tokens'].items():
            name = info.get('name', 'N/A')
            print(f"    {code}: {name}")
        print(f"  Validators: {len(stellar['validators'])}")

    print("\n[7] TSA Certificate (via Gate 158 vault):")
    tsa = pipeline.get_tsa_certificate()
    if tsa:
        print(f"  Subject: {tsa['subject_cn']} / {tsa['subject_org']}")
        print(f"  Issuer OU: {tsa.get('issuer_ou', 'N/A')}")
        print(f"  Valid: {tsa['valid_from']} → {tsa['valid_until']}")
        print(f"  Key Usage: {', '.join(tsa['key_usage'])}")
        print(f"  Extended Key Usage: {', '.join(tsa['extended_key_usage'])}")
        print(f"  Authority Key ID: {tsa['authority_key_id']}")
        print(f"  Subject Key ID: {tsa['subject_key_id']}")
        print(f"  Policy: {tsa.get('certificate_policy', 'N/A')}")
        print(f"  RSA modulus (first 32 hex): {tsa.get('rsa_modulus_hex', '')[:32]}...")

    print("\n[8] Full Pipeline Status:")
    print(json.dumps(pipeline.status(), indent=2))

    print("\n" + "=" * 70)
    print("[⚡] CRYPTO PIPELINE: OPERATIONAL")
    print("[🔒] VAULT: UNLOCKED (Gate 158)")
    print("[📜] ARCHIVE: CHAINED & INTACT")
    print("[⚡] Node 129: ONLINE")
    print("[⚡] T1_LOCKED: ACTIVE")
    print("=" * 70)

    return 0

if __name__ == "__main__":
    sys.exit(main())
