"""
PyCrypTools is a library that provides various cryptography tools for Python.
It provides functionalities to verify and sign files, as well as encrypt and decrypt files using AES in CBC mode.
"""

__copyright__  = """
Copyright (c) 2023 LixNew; lixnew2@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__version__ = '1.0.0'
__title__ = 'PyCrypTools'
__description__ = "PyCrypTools is a library that provides various cryptography tools for Python."
__autor__ = 'LixNew'
__twitter__ = '@LixNew2'
__url__ = "https://github.com/LixNew2/PyCrypTools"

#Import
import subprocess, os
from typing import Union
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

#Variables
SIGCHECK = (os.path.dirname(__file__) + '/bin/sigcheck64.exe').replace("\\", "/")
SIGNTOOL = (os.path.dirname(__file__) + '/bin/signtool.exe').replace("\\", "/")

#Functions
def is_signed(file_path : str, infos : bool = False) -> Union[bool, dict]:
    """
    Check if a file is digitally signed and optionally retrieve signing information.

    **Args**:
        file_path (str): Path of the file to check
        infos (bool): If True, returns information about the signed file

    Returns:
        Union[bool, dict]: Returns True if the file is signed and infos is False.
            Returns a dictionary with signing information if the file is signed and infos is True.
            Returns False if the file is not signed.

    Raises:
        FileNotFoundError: If the file at file_path does not exist.
        ValueError: If the signature information could not be determined.

    Example:
        >>> result = is_signed("path/to/file", infos=True)
        >>> print(result)
        {'Signed': True, 'Signing date': '16:14 27/06/2024', 'Publisher': 'Example Publisher', 
        'Company': 'Example Company', 'Description': 'Example Description'}
    """

    # Check if the file exists
    if os.path.exists(file_path) == False:
        raise FileNotFoundError(f"The file at {file_path} does not exist.")

    # Check if the file is signed
    result = subprocess.Popen(SIGCHECK + " " + '"' + file_path + '"', shell=False, stdout=subprocess.PIPE)
    # Decode the command output
    output = result.stdout.read().decode('latin-1')
    # Split the lines
    lines = output.split("\n")

    for line in lines:
        if 'Verified:' in line:
            if 'Signed' in line:
                # If infos is True, then return the signing information of the signed file, otherwise return True
                if infos:
                    data = {"Signed": True}

                    for line in lines:
                        if "Signing date:" in line:
                            data["Signing date"] = line.split("Signing date:")[1].strip()
                        elif "Publisher:" in line:
                            data["Publisher"] = line.split("Publisher:")[1].strip()
                        elif "Company:" in line:
                            data["Company"] = line.split("Company:")[1].strip()
                        elif "Description:" in line:
                            data["Description"] = line.split("Description:")[1].strip()
                        else:
                            pass
                    
                    return data
                
                return True
            else:
                return False

    raise ValueError("The file signature could not be determined.")

def sign_file(file_path, certificate_path, certificate_pdw, encryption_algorithm : str = "SHA256"):
    
    """
    Sign a file with a specified certificate and encryption algorithm.

    Args:
        file_path (str): Path of the file to sign.
        certificate_path (str): Path of the certificate to use for signing.
        certificate_pdw (str): Certificate password.
        encryption_algorithm (str, optional): Encryption algorithm to use. Default is SHA256.

    Raises:
        FileNotFoundError: If the file or certificate does not exist.
        ValueError: If the encryption algorithm is invalid or if the file is already signed.
    """

    # Check if the file extension is valid
    if file_path.lower().endswith((
        ".exe", ".dll", ".sys", ".msi", ".cab", ".cat", ".vbs", ".js", ".ps1",
        ".psm1", ".psd1", ".ps1xml", ".psc1", ".msh", ".msh1", ".msh2", ".mshxml",
        ".msh1xml", ".msh2xml", ".inf", ".reg", ".manifest", ".config", ".policy",
        ".application", ".gadget"
    )) == False:
        raise ValueError(f"Invalid file type: {file_path}")
    
    # Check if the file exists
    if os.path.exists(file_path) == False:
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    # Check if the certificate exists
    if os.path.exists(certificate_path) == False:
        raise FileNotFoundError(f"The certificate at {certificate_path} does not exist.")
    
    # Check if the encryption algorithm is valid
    if encryption_algorithm not in ["SHA1", "SHA256", "SHA384", "SHA512"]:
        raise ValueError(f"Invalid encryption algorithm: {encryption_algorithm}")
    
    # Check if the file is already signed
    if is_signed(file_path):
        raise ValueError(f"The file at {file_path} is already signed.")
    
    # Sign the file using SignTool
    result = subprocess.run([SIGNTOOL, "sign", "/fd", encryption_algorithm, "/f", certificate_path, "/p", certificate_pdw, file_path], capture_output=True, text=True)
    
    if result.returncode == 0:
         print(f"The file at {file_path} has been successfully signed.")
    else:
         print(f"Failed to sign the file at {file_path}. Error: {result.stderr.splitlines()[0]}")

def encrypt_file(file_path : str, password : str):

    """
    Encrypts a file using AES in CBC mode.

    Args:
        file_path (str): Path of the file to encrypt.
        password (str): Password to encrypt the file (password must be 16, 24, or 32 bytes long).

    Raises:
        FileNotFoundError: If the file at file_path does not exist.
        ValueError: If the password is not 16, 24, or 32 bytes long.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    if len(password) not in [16, 24, 32]:
        raise ValueError("The password must be 16, 24, or 32 bytes long. (1 character = 1 byte)")

    # Generate a random initialization vector (IV)
    iv = os.urandom(16)  # 16-bytes IV for AES

    # Create a Cipher object with AES in CBC mode
    cipher = Cipher(algorithms.AES(bytes(password.encode("utf-8"))), modes.CBC(iv), backend=default_backend())

    # Add PKCS7 padding
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Encrypt the data
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Save the IV and ciphertext to a file
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + ciphertext)

    # Return the path of the encrypted file
    print(f"The file {encrypted_file_path} has been successfully encrypted.")

def decrypt_file(file_path, password):

    """
    Decrypts a file using AES in CBC mode.

    Args:
        file_path (str): Path of the file to decrypt.
        password (str): Password to decrypt the file (password must be 16, 24, or 32 bytes long).

    Raises:
        FileNotFoundError: If the file at file_path does not exist.
        ValueError: If the password is not 16, 24, or 32 bytes long.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")

    if len(password) not in [16, 24, 32]:
        raise ValueError("The password must be 16, 24, or 32 bytes long. (1 character = 1 byte)")

    # Read the encrypted file
    with open(file_path, 'rb') as f:
        iv = f.read(16)  # Read the first 16 bytes as IV
        ciphertext = f.read()

    # Create a Cipher object with AES in CBC mode
    cipher = Cipher(algorithms.AES(bytes(password.encode("utf-8"))), modes.CBC(iv), backend=default_backend())

    # Decrypt the data
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove the padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    # Save the decrypted data to a new file
    decrypted_file_path = file_path.replace('.enc', '_decrypted')
    with open(decrypted_file_path, 'wb') as f:
        f.write(unpadded_data)

    # Return the path of the decrypted file
    print(f"The file {decrypted_file_path} has been successfully decrypted.")