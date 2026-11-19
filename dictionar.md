# Dictionarul meu de Linux

## 1. Permisiuni (Cine are voie sa faca ce?)
- `ls -l` = imi arata cine are voie sa citeasca/scrie/ruleze un fisier.
- `chmod 777` = dau voie la toata lumea sa faca orice (PERICULOS).
- `chmod 755` = eu pot face orice, ceilalti doar sa citeasca si sa ruleze.
- **SUID** (`chmod 4755`) = fisierul ruleaza cu puterile altui utilizator (ex: bandit24).
- 'chmod +w numele_fisierului' ii dai drept de scriere fisierului
- 'sudo -u numele_utilizatorului comanda' poti citi fisierul ca fiind utilizatorul
- ## Tabel permisiuni (chmod)
- 0 = --- (Nimic)
- 1 = --x (Executare)
- 2 = -w- (Scriere)
- 3 = -wx (Scriere + Executare)
- 4 = r-- (Citire)
- 5 = r-x (Citire + Executare)
- 6 = rw- (Citire + Scriere)
- 7 = rwx (Citire + Scriere + Executare)

Exemplu: chmod 755 = Proprietar (rwx), Grup (r-x), Restul (r-x).

## 2. Cautare (Unde e fisierul/cuvantul?)
- `grep "cuvant" fisier.txt` = cauta un cuvant in text.
- `grep -i` = ignora majusculele.
- `find . -name "parola.txt"` = cauta fisierul in folderul curent.
- `find / -perm -4000` = cauta fisiere cu SUID in tot sistemul.

## 3. Rețea (Cum vorbesc cu alte calculatoare?)
- `nmap 127.0.0.1` = scanez porturile locale (ce usi sunt deschise).
- `nc -l -p 1234` = deschid o usa (port) si ascult.
## 4. Variabile si Aliasuri (Cum scurtez comenzile)
- `echo $USER` = imi arata numele de utilizator.
- `echo $HOME` = imi arata unde e folderul principal.
- `alias salut="echo 'Salut'"` = creez o comanda noua numita "salut".
- `alias ll="ls -la"` = daca scriu "ll", ruleaza automat "ls -la".
- 'alias dic='nano ~/my_linux/dictionar.md'' deschide direct dictionar.md
## 5. Aliasuri permanente
- `nano ~/.bashrc` = deschid fisierul de configurare.
- `source ~/.bashrc` = aplic modificarile fara sa inchid terminalul.
## 6. Fluxul de lucru Git (Cum salvez pe GitHub)
De fiecare dată când modific dicționarul, fac 3 pași:
- `ga` = (git add .) Adaug toate modificările.
- `gc "Mesajul meu"` = (git commit -m) Salvez modificările cu un mesaj clar.
- `gp` = (git push) Trimit totul pe GitHub.

## 7. Termux vs Ubuntu (Atenție la confuzii!)
- Sunt sisteme separate! Fiecare are propriul `~/.bashrc` și propriile aliasuri.
- Ce fac într-un sistem, nu se reflectă automat în celălalt.
- Pentru a sincroniza codul între ele, folosesc GitHub-ul: fac `gp` pe unul, iar pe celălalt fac `git pull`. 
