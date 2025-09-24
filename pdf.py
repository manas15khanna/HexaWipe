import qrcode
import json, base64
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from datetime import datetime

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# -------------------------
# Key generation
# -------------------------
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    public_key = private_key.public_key()
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print("✅ RSA keys generated")

# Run once
generate_keys()


# -------------------------
# AES-RSA Hybrid Encryption
# -------------------------
def encrypt_metadata(metadata: dict, public_key_path="public_key.pem") -> str:
    # Serialize metadata to JSON
    data = json.dumps(metadata).encode()

    # 1️⃣ Generate random 32-byte AES key + IV
    aes_key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    # 2️⃣ Encrypt AES key with RSA
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # 3️⃣ Combine and encode as Base64
    payload = {
        "key": base64.b64encode(encrypted_key).decode(),
        "iv": base64.b64encode(iv).decode(),
        "data": base64.b64encode(encrypted_data).decode()
    }
    return base64.b64encode(json.dumps(payload).encode()).decode()


# -------------------------
# Digital signature
# -------------------------
def sign_metadata(metadata: dict, private_key_path="private_key.pem") -> dict:
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    message = json.dumps(metadata).encode()
    signature = private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())
    metadata["signature"] = base64.b64encode(signature).decode()
    return metadata


# -------------------------
# Certificate generation
# -------------------------
def generate_certificate_with_qr(name, cert_id, date, course="Data Wipe", filename="certificate.pdf"):
    # Metadata
    metadata = {
        "Certificate ID": cert_id,
        "Name": name,
        "Course": course,
        "Issued Date": date,
        "Created At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    signed_metadata = sign_metadata(metadata)

    # Encrypt using hybrid AES-RSA
    qr_data = encrypt_metadata(signed_metadata)

    # Generate QR
    qr = qrcode.make(qr_data)
    qr_filename = "temp_qr.png"
    qr.save(qr_filename)

    # Create PDF
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Border
    c.setLineWidth(4)
    c.rect(30, 30, width - 60, height - 60)

    # Title & text
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width / 2, height - 150, "Certificate of Complete Data Wipe")
    c.setFont("Helvetica", 20)
    c.drawCentredString(width / 2, height - 200, "This certifies that data from")
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - 260, name)
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height - 320, "has been securely wiped")
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height - 340, "using HexaWipe")
    c.setFont("Helvetica-Oblique", 14)
    c.drawCentredString(width / 2, height - 420, f"Date: {date}")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, 80, "Scan the QR to verify encrypted certificate details")

    # QR
    qr_size = 120
    c.drawImage(qr_filename, width - qr_size - 60, 60, qr_size, qr_size)

    c.save()
    print(f"✅ Certificate generated: {filename}")


# -------------------------
# Example
# -------------------------
generate_certificate_with_qr("HDD", "CERT-2025-001", "24 Sept 2025")
