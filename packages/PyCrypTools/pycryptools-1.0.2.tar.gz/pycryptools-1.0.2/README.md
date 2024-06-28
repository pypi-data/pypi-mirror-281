# PyCrypTools

[![Downloads](https://img.shields.io/pepy/dt/PyCrypTools)](https://pypi.org/project/PyCrypTools/)
[![Version](https://img.shields.io/pypi/v/PyCrypTools)](https://pypi.org/project/PyCrypTools/)
[![Python Version](https://img.shields.io/pypi/pyversions/PyCrypTools)](https://pypi.org/project/PyCrypTools/)

PyCrypTools is a library that provides various cryptography tools for Python.
It provides functionalities to verify and sign files, as well as encrypt and decrypt files using AES in CBC mode.

## Set up
----
### Install

~~~python
pip install pycryptools
~~~

### Upgrade
~~~~python
pip install --upgrade pycryptools
~~~~

## Support

If you want to contact me for questions, bugs, or problems or other : lixnew2@gmail.com

## Python version

PyCrypTools was written for python 3.

## Functions

Checks whether a file is digitally signed
~~~python
is_signed()
# You can use the "infos" parameter to retrieve all the signature information of the file.
# By default, the parameter is set to false and the function returns true or false if the file is signed.
args = file_path, infos
~~~


Allows you to digitally sign a file
~~~python
sign_file()
# The "encryption_algorithm" parameter is set by default to the "SHA256" algorithm.
# If you wish, you can change it to another hashing/encryption algorithm.
args = file_path, certificate_path, certificate_pdw, encryption_algorithm
~~~


Encrypts a file
~~~python
encrypt_file()
# The password must be 16, 24, or 32 bytes long. (1 character = 1 byte)
args = file_path, password
~~~


Decrypts a file
~~~python
decrypt_file()
# To decrypt the ".enc" file, you must use the same password as during encryption.
# WARNING: If the password entered to decrypt the file is incorrect, the data in your file will be altered and it will be permanently unreadable.
args = file_path, password
~~~