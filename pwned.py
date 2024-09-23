from getpass import getpass
from hashlib import sha1
import http.client

host = 'api.pwnedpasswords.com'

password = getpass('password:').encode('utf-8')
hash = sha1(password).hexdigest().upper()
print('sha1:', hash)

path = '/range/' + hash[0:5]
print('request: GET@https://' + host + path)

connection = http.client.HTTPSConnection(host)
connection.request('GET', path)
response = connection.getresponse().read().decode('utf-8')
connection.close()

# print(response)

lines = response.split()
print('response size:', len(lines))

apex = hash[5:40]
pwned = False
for line in lines:
	split = line.split(':')
	if split[0] == apex:
		print('You have been pwned', split[1], 'times!')
		pwned = True

if not pwned:
	print('You have not been pwned, yet!')
