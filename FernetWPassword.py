import base64
import os
import sys

from cryptography.fernet import Fernet 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QPlainTextEdit, QMessageBox



class Application(object):
	def __init__(self, app):
		self.app = app

		# load the main UI
		self.ui = uic.loadUi('FernetMain.ui')

		# bind button clicks to events
		self.ui.Continue.clicked.connect(self.CheckPassword)
		self.ui.Cancel.clicked.connect(self.Quit)

		# bind enter to button pushes
		self.ui.keyPressEvent = self.keyPressEvent

		# show the ui
		self.ui.show()
		self.run()

	def run(self):
		self.app.exec_()

	def Quit(self):
		self.app.exit()

	def keyPressEvent(self, event):
		'''
		This overrides the keypressevent to enter
		to envoke the button functions

		'''
		fwidget = self.ui.focusWidget()
		if fwidget.objectName() == "Continue":
			if event.key() == Qt.Key_Return:	
				self.CheckPassword()
		else:
			if event.key() == Qt.Key_Return:
				self.Quit()

	def CheckPassword(self):
		'''
		This will check the user entered password against the password
		used to encrypt by generating the same fernet key with the stored
		salt.

		'''

		with open('salt.key', 'rb') as salt:
			salt = salt.read()

		kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=390000,
		)

		password = (self.ui.PasswordEntry.text()).encode()

		# opening the key
		with open('newkey.key', 'rb') as filekey:
			key = filekey.read()

		# check equality of generated key and key from password entered
		userkey = base64.urlsafe_b64encode(kdf.derive(password))

		if userkey == key:
			print('keys are equal')
			f = Fernet(userkey)

			'''
			whatever you'd like to encrypt/decrypt

			'''

			# a small string to encrypt/decrypt for syntax reference 
			encrypted = f.encrypt(('encrypted text').encode())
			decrypted = f.decrypt(encrypted).decode()
			print(decrypted)

			self.Quit()

		else:
			print('Invalid Password')
			self.Quit()


def generateKey():
	password = b"YourPassword"

	salt = os.urandom(16)

	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=390000,
		)

	key = base64.urlsafe_b64encode(kdf.derive(password))

	# string the key in a file
	with open('newkey.key', 'wb') as filekey:
		filekey.write(key)

	# string the salt in a file
	with open('salt.key', 'wb') as saltkey:
		saltkey.write(salt)


if __name__ == "__main__":

	generateKey()
	
	app = QtWidgets.QApplication(sys.argv)
	Application(app)
