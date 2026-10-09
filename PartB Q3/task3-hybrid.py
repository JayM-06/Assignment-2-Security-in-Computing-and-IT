# make sure you have installed cryptography library
# pip install cryptography

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode
import os

# Making sure the file path is able to work on all os
BASE = os.path.dirname(os.path.abspath(__file__))

# Folder paths built from BASE so they work on any operating system
input_file = os.path.join(BASE, "input", "task2.txt")
keys_dir = os.path.join(BASE, "keys")
output_dir = os.path.join(BASE, "output")
public_key_file = os.path.join(keys_dir, "public.hybrid.pem")
private_key_file = os.path.join(keys_dir, "private.hybrid.pem")
encrypted_file = os.path.join(output_dir, "task2_enc")
encrypted_key_file = os.path.join(output_dir, "task2_aes_key_enc")
decrypted_file = os.path.join(output_dir, "task2_dec.txt")

# make sure the folders exist before saving files
os.makedirs(keys_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)


# Step 1: friend generates RSA keys, each key is saved in its own file
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # turn the keys into PEM text so they can be saved and displayed
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # save each key in its own file
    with open(private_key_file, "wb") as private_file:
        private_file.write(private_pem)
    with open(public_key_file, "wb") as public_file:
        public_file.write(public_pem)

    return private_pem, public_pem


# Step 2: I encrypt the file with AES, then encrypt the AES key with RSA
def encrypt_message():
    # read the file to be sent
    with open(input_file, "rb") as in_file:
        message = in_file.read()

    # Generate a random symmetric key for AES (32 bytes = AES-256)
    symmetric_key = os.urandom(32)

    # Encrypt the data with AES (CFB mode, no padding needed)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message) + encryptor.finalize()

    # load the friend's public key from its file
    with open(public_key_file, "rb") as public_file:
        public_key = serialization.load_pem_public_key(public_file.read())

    # Encrypt the symmetric key with RSA (OAEP padding)
    encrypted_key = public_key.encrypt(
        symmetric_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # save the encrypted file (IV first, then data) and the encrypted AES key
    with open(encrypted_file, "wb") as enc_file:
        enc_file.write(iv + encrypted_message)
    with open(encrypted_key_file, "wb") as enc_key_file:
        enc_key_file.write(encrypted_key)

    return message, symmetric_key, iv, encrypted_message, encrypted_key


# Step 3: friend decrypts the AES key with RSA, then decrypts the file with AES
def decrypt_message():
    # read the encrypted file, the first 16 bytes are the IV
    with open(encrypted_file, "rb") as enc_file:
        iv = enc_file.read(16)
        encrypted_message = enc_file.read()
    with open(encrypted_key_file, "rb") as enc_key_file:
        encrypted_key = enc_key_file.read()

    # load the friend's private key from its file
    with open(private_key_file, "rb") as private_file:
        private_key = serialization.load_pem_private_key(private_file.read(), password=None)

    # Decrypt the symmetric key
    symmetric_key = private_key.decrypt(
        encrypted_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt the data
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()

    # save the decrypted file in its own file
    with open(decrypted_file, "wb") as dec_file:
        dec_file.write(decrypted_message)

    return symmetric_key, decrypted_message


if __name__ == "__main__":
    # Generate RSA keys
    private_pem, public_pem = generate_rsa_keys()
    print("RSA public key:")
    print(public_pem.decode())
    print("RSA private key:")
    print(private_pem.decode())

    # Encrypt the file
    message, symmetric_key, iv, encrypted_message, encrypted_key = encrypt_message()
    print("Original:", message.decode())
    print("AES key:", b64encode(symmetric_key).decode())
    print("IV (Initialization Vector):", b64encode(iv).decode())
    print("Encrypted Message:", b64encode(encrypted_message).decode())
    print("Encrypted Symmetric Key:", b64encode(encrypted_key).decode())

    # Decrypt the file
    recovered_key, decrypted_message = decrypt_message()
    print("Recovered AES key:", b64encode(recovered_key).decode())
    print("Decrypted:", decrypted_message.decode())
    print("Decrypted file saved in the output folder")