import base64
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# -------------------------
# Decrypt QR content
# -------------------------
def decrypt_qr_content(qr_b64: str, private_key_path="private_key.pem") -> dict:
    # Decode Base64 QR content
    payload_json = base64.b64decode(qr_b64)
    payload = json.loads(payload_json)

    encrypted_key = base64.b64decode(payload["key"])
    iv = base64.b64decode(payload["iv"])
    encrypted_data = base64.b64decode(payload["data"])

    # Load private key
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # 1️⃣ Decrypt AES key using RSA private key
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 2️⃣ Decrypt metadata using AES key
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_bytes = decryptor.update(encrypted_data) + decryptor.finalize()

    # Return metadata as dict
    return json.loads(decrypted_bytes.decode())


# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    qr_content = input("Enter Base64 QR content: ")

    try:
        metadata = decrypt_qr_content(qr_content)
        print("✅ Decrypted certificate metadata:")
        print(json.dumps(metadata, indent=4))
    except Exception as e:
        print("❌ Decryption failed:", str(e))
