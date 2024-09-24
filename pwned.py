# aus dem getpass paket brauchen wir die getpass funktion
from getpass import getpass

# aus der hashlib brauchen wir die hash funktion sha1
from hashlib import sha1

# wir brauchen einen http client
import http.client

# die host adresse vom web service
host = 'api.pwnedpasswords.com'

# getpass liest das passwort von der tastatur ohne es in der konsole wiederzugeben
# encode übersetzt den string in ein byte array, dabei kann ein zeichensatz (charset) angegeben werden, utf-8 ist der standard
password = getpass('password:').encode('utf-8')

# das password geht durch den sha1 algorithmus
# hexdigest gibt das resultat als 40 stellige hexadezimalzahl aus (0-9,a-f)
# upper mach die kleinbuchstaben groß
hash = sha1(password).hexdigest().upper()

# zwischenresultat ausgeben
print('sha1:', hash)

# der pfad für die API brauch die ersten 5 zeichen von dem hash
path = '/range/' + hash[0:5]

print('request: GET@https://' + host + path)

# wir starten eine HTTPS verbindung zu dem server
connection = http.client.HTTPSConnection(host)
# und schicken einen GET request mit dem zuvor gebastelten pfad
connection.request('GET', path)
# getresponse holt die response
# read liefert den response body, an den headers sind wir nicht interessiert
# decode übersetzt den body in einen string, unter angabe eines charsets
response = connection.getresponse().read().decode('utf-8')
# als guter client schließen wir die verbindung um keine resourcen zu verschwenden
connection.close()

# der response body wird das zeilen aufgeteilt, das ergebnis ist ein string array
lines = response.split()

# anzahl der zeilen
print('response size:', len(lines))

# mit apex definieren wir die letzten 35 zeichen vom hash
apex = hash[5:40]

# erstmal nehmen wir an, dass unser passwort nicht in der liste ist
pwned = False

# schleife über alle zeilen aus der response
# alles was im folgenden eingerückt ist wird für jedes element aus dem array ausgeführt
# line bezeichnet dann die jeweilige zeile
for line in lines:

	# wir zerteilen die zeile am doppelpunkt
	split = line.split(':')
	# wenn der erste teil unserm apex entsprich, wurd das im folgenden eingerückte ausgeführt
	if split[0] == apex:
		# der password hash war in der datenbank, der zweite teil der zeile gibt an wie oft
		print('You have been pwned', split[1], 'times!')
		# verloren
		pwned = True

# falls der hash nicht in der datenbank wahr
if not pwned:
	print('You have not been pwned, yet!')
