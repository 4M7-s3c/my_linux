# Dictionarul meu de Linux

## 1. Permisiuni (Cine are voie sa faca ce?)
- `ls -l` = imi arata cine are voie sa citeasca/scrie/ruleze un fisier.
- `chmod 777` = dau voie la toata lumea sa faca orice (PERICULOS).
- `chmod 755` = eu pot face orice, ceilalti doar sa citeasca si sa ruleze.
- **SUID** (`chmod 4755`) = fisierul ruleaza cu puterile altui utilizator (ex: bandit24).

## 2. Cautare (Unde e fisierul/cuvantul?)
- `grep "cuvant" fisier.txt` = cauta un cuvant in text.
- `grep -i` = ignora majusculele.
- `find . -name "parola.txt"` = cauta fisierul in folderul curent.
- `find / -perm -4000` = cauta fisiere cu SUID in tot sistemul.

## 3. Rețea (Cum vorbesc cu alte calculatoare?)
- `nmap 127.0.0.1` = scanez porturile locale (ce usi sunt deschise).
- `nc -l -p 1234` = deschid o usa (port) si ascult.
