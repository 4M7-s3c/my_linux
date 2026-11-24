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
## 8. Operatori în Terminal (Pipe si AND)
- `|` (Pipe): Trimite rezultatul comenzii din stânga ca input pentru comanda din dreapta.
  - Exemplu: `cat server.log | grep "ERROR"` (filtreaza textul).
- `&&` (AND): Executa comanda din dreapta DOAR DACA comanda din stanga a reusit (a avut succes).
  - Exemplu: `cd /my_linux && git push` (daca intrarea in folder a reusit, atunci trimite pe Git).
  - Daca prima comanda da eroare, a doua nu se mai executa.
- ATENTIE la Git: Nu folosi `|` intre comenzile Git (ex: `ga | gc`), foloseste `&&` (ex: `ga && gc "mesaj" && gp`).
## 9. Alias vs Funcție în Bash (Diferența crucială)

Deși ambele scurtează comenzile, ele funcționează diferit:

- **Aliasul** este o simplă înlocuire de text. Nu poate primi argumente (precum un cuvânt pe care vrei să îl cauți).
  - Exemplu: `alias ll='ls -la'` (când scriu `ll`, rulează `ls -la`).
  - *De ce a eșuat `gitpush "mesaj"`?* Pentru că aliasul nu știe să preia textul dintre ghilimele ca argument.

- **Funcția** este un mini-program care poate primi argumente. Se folosește când vrei să transmiți date (ex: `$1`).
  - Exemplu: 
    ```bash
    cauta() {
        grep -i --color=auto "$1" ~/my_linux/dictionar.md
    }
    ```
  - Când scriu `cauta "git"`, funcția ia cuvântul "git" ca prim argument (`$1`) și îl folosește în comandă.

**Concluzie:** Dacă vrei doar să scurtezi o comandă simplă, folosește `alias`. Dacă vrei să creezi o comandă nouă care să primească date de la tine, folosește o `funcție`.
## 10. Descompunerea funcției `cauta` (Bucată cu bucată)

Funcția:
`cauta() { grep -i --color=auto "$1" ~/my_linux/dictionar.md; }`

- `cauta()` = Numele funcției. Parantezele goale sunt obligatorii, ele îi spun lui Bash că e o funcție, nu o variabilă.
- `{ ... }` = Acoladele. Ele delimitează începutul și sfârșitul „rețetei” (blocul de cod).
- `grep` = Comanda care face treaba (caută text).
- `-i` = Opțiunea care ignoră majusculele/minusculele.
- `--color=auto` = Opțiunea care colorează cuvântul căutat.
- `"$1"` = Primul argument (cuvântul pe care îl scrii după comandă). Ghilimelele duble sunt esențiale pentru a păstra textul ca un singur șir (ex: "git push").
- `~/my_linux/dictionar.md` = Fișierul țintă (calea absolută, ca să meargă din orice folder).
## 11. Criptarea fișierelor cu GPG (Seif digital)

Am creat un fișier securizat pentru parole folosind GPG. Algoritmul este atât de puternic încât, fără parola master, fișierul nu poate fi deschis.

- **Criptare (punem parola):**
  `gpg -c --pinentry-mode loopback ~/parole.txt`
  *(Creează fișierul `parole.txt.gpg`. Opțiunea `loopback` este esențială în Termux ca să nu dea eroare de timeout).*

- **Decriptare (citim parolele):**
  `gpg -d --pinentry-mode loopback ~/parole.txt.gpg`
  *(Ne cere parola master și ne afișează textul).*

- **Aliasuri utile (le-am pus în .bashrc):**
  `alias cripteaza='gpg -c --pinentry-mode loopback'`
  `alias decripteaza='gpg -d --pinentry-mode loopback'`

- **Regulă de aur:** Dacă uit parola master, pierd tot. Nu există „resetare parolă” la criptare!
## 12. Brute-force (Atac prin forță brută)

Metodă de a ghici o parolă sau un PIN încercând toate combinațiile posibile. În Bandit nivelul 24, am folosit un script pentru a ghici un PIN de 4 cifre (10.000 de combinații).

**Scriptul folosit (brute.sh):**
`#!/bin/bash`
`PAROLA="PAROLA_TA"`
`for i in {0000..9999}`
`do`
`    echo "$PAROLA $i"`
`done | nc localhost hostul propriu-zis | grep -v "Wrong"`

**Cum funcționează:**
- `for i in {0000..9999}` = Buclă care generează toate numerele de la 0000 la 9999.
- `echo "$PAROLA $i"` = Afișează parola și PIN-ul curent.
- `| nc localhost host-ul propriu-zis` = Trimite textul către serverul de pe portul host propriu-zis.
- `| grep -v "Wrong"` = Filtrează rezultatul, ascunzând răspunsurile greșite (opțiunea `-v` inversează căutarea). Astfel, va apărea doar răspunsul corect.

**Sfat:** Întotdeauna rulați scripturile de brute-force în foldere precum `/tmp`, unde aveți permisiuni de scriere.
## 13. Shell-uri limitate și SUID (Concepte generale)

**1. Shell-uri limitate (Restricted Shells):**
Uneori, un utilizator este configurat să ruleze un program în loc de un shell normal (precum `more`, `less`, `vi` sau un script simplu). Acest lucru împiedică execuția comenzilor.
- **Cum verifici:** `grep utilizator /etc/passwd` (te uiți la ultima coloană, unde e trecut shell-ul).
- **Cum evadezi:** Dacă programul are o funcție de tip „shell” sau „editor” (ex: în `vi` poți scrie `:shell` sau `:!bash`), poți scăpa de restricție.

**2. Permisiunea SUID (Set User ID):**
Un fișier cu SUID (permisiunea 4755) rulează cu privilegiile proprietarului său, nu ale utilizatorului care îl execută.
- **Exemplu:** Dacă un executabil aparține lui `root` și are SUID, orice utilizator care îl rulează va executa comenzile ca și cum ar fi `root`.
- **Cum cauți fișiere SUID:** `find / -perm -4000 -type f 2>/dev/null`
- **Cum exploatezi:** Dacă găsești un astfel de executabil, îl poți folosi pentru a citi fișiere la care nu ai acces (ex: `./executabil cat /etc/parola`).

## 14. transfer de pe Pc pe telefon
scp -P 8022 UTILIZATOR@IP_TELEFON:ghid.txt ~/
scp -P 8022 UTILIZATOR@IP_TELEFON:locatia_lui_ghid ~/ghid
