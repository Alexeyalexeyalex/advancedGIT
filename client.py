import socket
import threading

# Выбор имени
nickname = input("Choose your nickname: ")

# Соединение с сервером
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Получение сообщений с сервера
def receive():
    while True:
        try:
            # Проверка на запрос никнейма
            message = client.recv(1024).decode('UTF-8')
            if message == 'NICK':
                client.send(nickname.encode('UTF-8'))
            else:
                print(message)
        except:
            # Закрытие связи при ошибке
            print("An error occured!")
            client.close()
            break
# Отправка сообщений на сервер
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('UTF-8'))

# создание потоков на прием и отправку сообщений
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()