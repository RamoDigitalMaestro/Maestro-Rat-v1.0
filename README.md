
[![Instagram](https://img.shields.io/badge/-Instagram-ff69b4?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/rootramo?igsh=c2ptcHhjZGRnMGV2)

#🇹🇷 Türkçe

Bu Python betiği, bir arka kapı saldırısı simülasyonu için tasarlanmıştır. Attacker.py adlı betik, bir saldırganın belirli komutları hedef makineye göndermesini sağlar. Target.py adlı betik ise, bu komutları alır ve hedef makinede ilgili işlemleri gerçekleştirir.

Attacker.py, hedef IP adresi ve port numarasını argüman olarak alır ve ardından hedefe bağlanır. Ardından, saldırganın komutları girmesini sağlar. Kullanıcı, çeşitli komutlar aracılığıyla hedefe komut gönderebilir ve hedef makinedeki işlemleri gerçekleştirebilir.

Target.py, sunucunun IP adresini ve dinlemek istediği port numarasını kullanıcıdan alır. Ardından, belirli komutları alır ve bu komutlara göre işlem yapar. Örneğin, 'ls' komutuyla dizin içeriğini listeler veya 'execute' komutuyla belirli bir terminal komutunu çalıştırır.

Bu iki betik, kötü amaçlı yazılım analizi veya siber güvenlik eğitimi gibi senaryolar için kullanılabilir. Ancak, bu tür aktiviteleri gerçek sistemlerde gerçekleştirmek yasa dışı olabilir ve izinsiz erişim gerektirebilir.

#Nasıl Kullanılır?

attacker.py -lport (aktif portunuzu giriceksiniz) -lhost(kendi ip adresini giriceksiniz)

examples;

attacker.py -lhost 192.168.1.33 -lport 8080

Kurban target.py başlattığı zaman bağlantı size gelicektir.
not: target.py deki ip ve portu kendinize gore ayarlayın.
Kötü kullanımdan ben sorumlu değilim.

#🇬🇧 English

This Python script is designed to simulate a backdoor attack. The script, called attacker.py, allows an attacker to send certain commands to the target machine. The script named target.py receives these commands and performs the relevant operations on the target machine.

Attacker.py takes the target IP address and port number as arguments and then connects to the target. It then allows the attacker to enter commands. The user can send commands to the target through various commands and perform operations on the target machine.

Target.py receives the server's IP address and the port number it wants to listen on from the user. Then, it receives certain commands and acts according to those commands. For example, it lists directory contents with the 'ls' command or runs a specific terminal command with the 'execute' command.

These two scripts can be used for scenarios such as malware analysis or cybersecurity training. However, performing such activities on real systems may be illegal and require unauthorized access.

#How to use?

attacker.py -lport (you will enter your active port) -lhost (you will enter your own IP address)

examples;

attacker.py -lhost 192.168.1.33 -lport 8080

When the victim starts target.py you will receive the link.
note: Set the ip and port in target.py according to your needs.
I am not responsible for any misuse.
