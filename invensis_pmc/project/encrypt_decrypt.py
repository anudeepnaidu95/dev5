import base64
import hashlib
import os, random, struct
from hashlib import md5
from Crypto import Random
from Crypto.Cipher import AES
from django.core.files.storage import default_storage

class AESCipher(object):

	def __init__(self, key): 
		self.bs = 32
		self.key = hashlib.sha256(key.encode()).digest()

	def encrypt(self, raw):
		raw = self._pad(raw)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return base64.b64encode(iv + cipher.encrypt(raw))

	def decrypt(self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:AES.block_size]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

	def _pad(self, s):
		return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

	@staticmethod
	def _unpad(s):
		return s[:-ord(s[len(s)-1:])]
		#return s[0:-ord(s[-1])]


	def encrypt_file(self, in_filename, out_filename=None, chunksize=64*1024):
		""" Encrypts a file using AES (CBC mode) with the
			given key.

			key:
				The encryption key - a string that must be
				either 16, 24 or 32 bytes long. Longer keys
				are more secure.

			in_filename:
				Name of the input file

			out_filename:
				If None, '<in_filename>.enc' will be used.

			chunksize:
				Sets the size of the chunk which the function
				uses to read and encrypt the file. Larger chunk
				sizes can be faster for some files and machines.
				chunksize must be divisible by 16.
		"""
		if not out_filename:
			#out_filename = in_filename
			out_filename = in_filename + '.enc'
		else:
			out_filename = out_filename + '.enc'

		iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
		encryptor = AES.new(self.key, AES.MODE_CBC, iv)

		#print in_filename.readlines()
		with open(in_filename, 'rb') as infile:
			filesize = os.path.getsize(in_filename)
			with open(out_filename, 'wb') as outfile:
				outfile.write(struct.pack('<Q', filesize))
				outfile.write(iv)

				while True:
					chunk = infile.read(chunksize)
					if len(chunk) == 0:
						break
					elif len(chunk) % 16 != 0:
						chunk += ' ' * (16 - len(chunk) % 16)
					print chunk
					outfile.write(encryptor.encrypt(chunk))
			return out_filename



	def decrypt_file(self, in_filename, out_filename=None, chunksize=24*1024):
		""" Decrypts a file using AES (CBC mode) with the
			given key. Parameters are similar to encrypt_file,
			with one difference: out_filename, if not supplied
			will be in_filename without its last extension
			(i.e. if in_filename is 'aaa.zip.enc' then
			out_filename will be 'aaa.zip')
		"""
		if not out_filename:
			#file_name = in_filename.split('/')[-1]
			out_filename = os.path.splitext(in_filename)[0]

		with open(in_filename, 'rb') as infile:
			origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
			iv = infile.read(16)
			decryptor = AES.new(self.key, AES.MODE_CBC, iv)

			with open(out_filename, 'wb') as outfile:
				while True:
					chunk = infile.read(chunksize)
					if len(chunk) == 0:
						break
					#print "chunks", decryptor.decrypt(chunk)
					outfile.write(decryptor.decrypt(chunk))
				outfile.truncate(origsize)

			return out_filename
		#f = open(out_filename, 'r')
		#print f.read()
			





def derive_key_and_iv(password, salt, key_length, iv_length):
	d = d_i = ''
	while len(d) < key_length + iv_length:
		d_i = md5(d_i + password + salt).digest()
		d += d_i
	return d[:key_length], d[key_length:key_length+iv_length]

def encrypt_file(in_file, out_file, password, key_length=32):
	print "infile", in_file
	bs = AES.block_size
	salt = Random.new().read(bs - len('Salted__'))
	key, iv = derive_key_and_iv(password, salt, key_length, bs)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	out_file.write('Salted__' + salt)
	finished = False
	while not finished:
		chunk = in_file.read(1024 * bs)
		#print "chunk", chunk
		if len(chunk) == 0 or len(chunk) % bs != 0:
			padding_length = bs - (len(chunk) % bs)
			chunk += padding_length * chr(padding_length)
			finished = True
		#print "chunk", chunk
		#print "cipher.encrypt(chunk)", cipher.encrypt(chunk)
		out_file.write(cipher.encrypt(chunk))
	return out_file


def decrypt_file(in_file, out_file, password, key_length=32):
	#print "infile", in_file.read()
	bs = AES.block_size
	salt = in_file.read(bs)[len('Salted__'):]
	key, iv = derive_key_and_iv(password, salt, key_length, bs)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	next_chunk = ''
	finished = False
	while not finished:
		#print in_file.read(1024 * bs)
		chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
		#print "chunk",chunk
		#print "next_chunk", next_chunk

		if len(next_chunk) == 0:

			padding_length = ord(chunk[-1])
			if padding_length < 1 or padding_length > bs:
			   raise ValueError("bad decrypt pad (%d)" % padding_length)
			# all the pad-bytes must be the same
			if chunk[-padding_length:] != (padding_length * chr(padding_length)):
			   # this is similar to the bad decrypt:evp_enc.c from openssl program
			   raise ValueError("bad decrypt")
			chunk = chunk[:-padding_length]
			finished = True
		out_file.write(chunk)
	return out_file
	



