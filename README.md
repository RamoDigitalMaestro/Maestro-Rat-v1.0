
[![Instagram](https://img.shields.io/badge/-Instagram-ff69b4?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/rootramo?igsh=c2ptcHhjZGRnMGV2)

#🇹🇷

Bu Python betiği, bir arka kapı saldırısı simülasyonu için tasarlanmıştır. Attacker.py adlı betik, bir saldırganın belirli komutları hedef makineye göndermesini sağlar. Target.py adlı betik ise, bu komutları alır ve hedef makinede ilgili işlemleri gerçekleştirir.

Attacker.py, hedef IP adresi ve port numarasını argüman olarak alır ve ardından hedefe bağlanır. Ardından, saldırganın komutları girmesini sağlar. Kullanıcı, çeşitli komutlar aracılığıyla hedefe komut gönderebilir ve hedef makinedeki işlemleri gerçekleştirebilir.

Target.py, sunucunun IP adresini ve dinlemek istediği port numarasını kullanıcıdan alır. Ardından, belirli komutları alır ve bu komutlara göre işlem yapar. Örneğin, 'ls' komutuyla dizin içeriğini listeler veya 'execute' komutuyla belirli bir terminal komutunu çalıştırır.

Bu iki betik, kötü amaçlı yazılım analizi veya siber güvenlik eğitimi gibi senaryolar için kullanılabilir. Ancak, bu tür aktiviteleri gerçek sistemlerde gerçekleştirmek yasa dışı olabilir ve izinsiz erişim gerektirebilir.

#Nasıl Kullanılır?

attacker.py -lport (aktif portunuzu giriceksiniz) -lhost(kendi ip adresini giriceksiniz)

examples;

attacker.py -lhost 192.168.1.33 -lport 8080
