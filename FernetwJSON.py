# import required module
from cryptography.fernet import Fernet
import json



def EncryptJson(json_filepath):
	'''
	This function encrypts a json file's value for 'Password'
	by generating a fernet key. The fernet key is stored for 
	later access when decrypting value.

	'''
    # key generation
    key = Fernet.generate_key()
 
    # string the key in a file location of your chosing
    with open('C:/somelocationofyourchoosing/key', 'wb') as filekey:
        filekey.write(key)

    # opening the key from that location
    with open('C:/somelocationofyourchoosing/key', 'rb') as filekey:
	    key = filekey.read()
 
    # using the generated key
    fernet = Fernet(key)
 
    # opening the original file to encrypt
    with open(json_filepath, 'r+') as file:
        original = json.load(file)

        # loop through json file and encrypt 'Password' value for every entry
        for i in original['Employees']:
            password = i['Password']
            encrypted = fernet.encrypt(password.encode('ascii'))
            i['Password'] = i['Password'].replace(password, str(encrypted))
            file.seek(0)
            json.dump(original, file, indent = 4)

    file.close()
    filekey.close()


def DecryptJson(json_filepath, key_filepath):
	'''
	This function uses the previously generated Fernet key
	to decrypt the 'Password' keys value.

	'''

    # opening the key
    with open(key_filepath, 'rb') as filekey:
	    key = filekey.read()
 
    # using the generated key
    fernet = Fernet(key)
 
    # opening the original file to decrypt
    with open(json_filepath, 'r+') as file:
        original = json.load(file)
        # loop through json file and decrypt and print 'Password' value for each entry
        for i in original['Employees']:
            password = i['Password']
            stringasbytes = eval(password)
            decrypt_pass = fernet.decrypt(stringasbytes)
            new_pass = decrypt_pass.decode("utf-8")
            print(new_pass)

    file.close()
    filekey.close()


if __name__ == '__main__':
    # your code here