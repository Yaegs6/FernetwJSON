# FernetwJSON/FernetWPassword
Encryption and Decryption functions using fernet keys

In the 'FernetwJSON.py' are two short functions that encrypt/decrypt a json file using a fernet key.

In the 'FernetWPassword.py', the user chooses a password to create the fernet key itself. The salt is stored 
in a location of the users choosing, then used later in conjuction with the password entered to create the exact
same fernet key to encrypt/decrypt values chosen.

Use the 'pip install cryptography' command to install the necessary libraries. 
