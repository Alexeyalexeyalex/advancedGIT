#!/bin/python3
import socket
import threading, os


# Подключение
host = '127.0.0.1'
port = 55555

# Запуск сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Никнеймы и данные пользователей
clients = []
nicknames = []

# Отправка новых сообщений всем
def broadcast(message):
    for client in clients:
        client.send(message)


# Проверка пользователей на активность
def handle(client):
    while True:
        try:
            # Сообщение пользователю для проверки
            message = client.recv(1024)
            broadcast(message)
        except:
            # Удаление ушедших пользователей
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('UTF-8'))
            nicknames.remove(nickname)
            break

# Основная функция работы сервера
def receive():
    while True:

        
        # Подключение пользователя
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Добавление информации о пользователе
        client.send('NICK'.encode('UTF-8'))
        nickname = client.recv(1024).decode('UTF-8')
        nicknames.append(nickname)
        clients.append(client)

        # Оповещение сервера и всех пользователей о новом
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('UTF-8'))
        client.send('Connected to server!'.encode('UTF-8'))

        print("Joing people: {}".format(nicknames))

        # Проверка пользователей на активность
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def exit():
    while True:
        # Выход из программы
        if (input("") == "q"):
            os._exit(os.X_OK)

print("Server if listening...")
rec_thread = threading.Thread(target=receive)
rec_thread.start()

exit()
