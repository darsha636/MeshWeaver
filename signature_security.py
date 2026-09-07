from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Get public key
public_key = private_key.public_key()


# Task execution request
task = b"Execute Task-1"


# Sign the task
signature = private_key.sign(
    task,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print("========================================")
print("MESHWEAVER DIGITAL SIGNATURE TEST")
print("========================================")

print("Task:", task.decode())
print("Signature generated successfully!")


# Verify signature
try:
    public_key.verify(
        signature,
        task,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print("Signature verification: PASSED")
    print("Task request is authentic.")
    
except Exception:
    print("Signature verification: FAILED")


# Test tampered task
tampered_task = b"Execute Task-2"

try:
    public_key.verify(
        signature,
        tampered_task,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print("Tampered task verification: PASSED")

except Exception:
    print("Tampered task verification: FAILED")
    print("Tampered task rejected.")


print("========================================")