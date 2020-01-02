# Zadání semestrální práce

Úkolem je vytvořit propojení s github api, které bude zajištovat, že pro jednotlivé projekty bude možnost vytvořit github repozitář, do kterého se pak budou nahrávat
všechny soubory, které se v rámci projektu vytvoří. Neboť dokumenty i moduly jsou vlastně pouze rst soubory, bude jednoduché je nahrávat a poté také stahovat.

Pokud někdo přistoupi z gitu z vnejška appka to pomocí webhooku pozná a aktualizuje data i na své straně, tedy vytvoří nové moduly či dokumenty. Také aktualizuje již stávající dokumenty.

## Podrobnější popis

Pokud se uživatel rozhodne, že chce data odesílat i na github, bude muset nejdříve přidat vygenerovaný klíč pro github api a poté bude nutné u nových repozitářů vždy nastavit webhook pro správnou funkcionalitu.
Uživatel se může rozhodnout jaké své projekty chce, či nechce nahrávat na github.

- [ ] Možnost vytvořit pro projekt repozitář za pomoci zadaného klíče (tuto možnost má pouze majitel projektu)
- [ ] Možnost nastavit naslouchání pomocí github webhooku pro pull, pokud se změní data v repozitáři automaticky se aktualizují i v aplikaci (toto půjde nastavit)
- [ ] Možnost nastavení toho jestli je repozitář výchozí zdroj dat, či ne
- [ ] Půjde nastavit větev, ze které si má aplikace brát/ukládat do ní změny (default master)
- [ ] Logy komunikace
