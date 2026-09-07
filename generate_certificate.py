from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from datetime import datetime, timedelta
from ipaddress import IPv4Address
import os


os.makedirs("certs", exist_ok=True)

# Generate private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Certificate subject
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MeshWeaver"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

# Create certificate
certificate = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.IPAddress(IPv4Address("127.0.0.1"))
        ]),
        critical=False
    )
    .sign(key, hashes.SHA256())
)

# Save private key
with open("certs/server.key", "wb") as f:
    f.write(
        key.private_bytes(
            Encoding.PEM,
            PrivateFormat.TraditionalOpenSSL,
            NoEncryption()
        )
    )

# Save certificate
with open("certs/server.crt", "wb") as f:
    f.write(
        certificate.public_bytes(Encoding.PEM)
    )

print("========================================")
print("MESHWEAVER TLS CERTIFICATE")
print("========================================")
print("Certificate created successfully!")
print("Location: certs/server.crt")
print("Private key: certs/server.key")
print("Validity: 365 days")
print("========================================")