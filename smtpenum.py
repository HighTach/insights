import socket
import sys
import re
from socket import error as SocketError
import errno

count = 0

if not sys.argv[1]:
    print("Wordlist não informada\r\n")
    print("Modo de uso: python smtpenum.py [wordlist] [ip]")

elif not sys.argv[2]:
    print("Ip não informado\r\n")
    print("Modo de uso: python smtpenum.py [wordlist] [ip]")


def connect():        #Se conecta com o serviço SMTP e devolve o banner e a variável com a conexão
    so_cket = (sys.argv[2],25)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(so_cket)
    banner = s.recv(1024)
    return s, banner

def brute(count):
    with open(sys.argv[1], 'r') as file:
        content = file.readlines()

    while True:
        s, banner = connect()
        try:
            #Itera pela wordlist e enumera todas as linhas começando a partir do valor de count
            for i,line in enumerate(content, start=count):
                line = content[i]
                data = f'VRFY {line}'
                s.send(bytes(data, encoding='utf-8'))
                #print(f"testando {i}-{line}\r\n")
                count += 1
                user = s.recv(1024)
                # Filtra a saida | se quiser ver todo o stdout só descomentar o print
                if re.search(b"252", user):
                    print(f"Usuário encontrado: {user.strip(b'252 2.0.0')}\r\n")
        #Se triggar um erro de reset pelo server continua o loop, se conectando novamente e voltando a partir do index incrementado em count
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise 
            print("Conexão resetada, reconectando...\r\n")
            continue


brute(count)