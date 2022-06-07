Postagalamb
=========
Discord robot projekt.

Készítés kezdete: 2022.05.16

# Tartalom
* [Készítők](#készítette)
* [Parancsok](#parancsok)
* [A projekt menete](#a-projekt-menete)

# Készítette
[**Valek Dániel**](https://github.com/HazzyWazz)
* API parancsok
* Feladatok kezelése, kiosztása

[**Tóthmajor Dóra**](https://github.com/AkrodKitten)
* Ötletadó
* Prezentáció
* Hetesek parancs
* Robot felhasználó tulajdonságai

[**Fodor Martin**](https://github.com/NoOnesSoul)
* Alap parancsok
* Economy

# Parancsok
Az alap parancsok listáját le lehet kérni a `/help` parancssal

További parancsok listájának megtekintéséhez használhatóak:
* `/help fun`
* `/help eco`

![alap help](https://media.discordapp.net/attachments/579188421067538442/983657173974388756/unknown.png)
![fun help](https://media.discordapp.net/attachments/579188421067538442/981883391693701170/unknown.png?width=474&height=630)
![economy help](https://media.discordapp.net/attachments/579188421067538442/981883738566852658/unknown.png?width=600&height=630)

**Kész parancsok:**
* `/hetesek` Kiírja a megadott számú hét hetesei nevét.
* `/dice` Dob egyszer egy kockát.
* `/coinflip` Feldob egy érmét.
* `/slotmachine` Játszik egy félkarú rablót.
* `/whois` A saját/egy megadott felhasználó alap adatait írja ki.
* `/kimi` Küld egy random Kimi Räikkönen idézetet.
* `/funfact` Küld egy random tényt.
* `/catboy` Küld egy random macska fiú képet.
* `/fox` Küld egy random rókás képet.
* `/dog` Küld egy random kutyás képet.
* `/akasztofa` Elindít egy akasztófa játékot.
* `/work` A parancs használatáért kapsz pénzt. 5 percenként lehet használni.
* `/shop` Kiírja a megvehető tárgyak listáját és azok árát.
* `/buy` A parancs használatával megveheted a boltban lévő tárgyakat.
* `/sell` A parancs használatával eladhatod a leltáradban lévő tárgyakat.
* `/fish` A parancs használatával horgászhatsz.
* `/inv` Felsorolja a leltáradban lévő tárgyakat és azok darabszámát.
* `/bal` A parancs használatával megtudod, hogy mennyi pénzed van összesen.
* `/ascii` A megadott szöveget ASCII-ban kiadja.

**Tervben lévő/felfüggesztett parancsok:**

* `/chop` A parancs használatával fát vághatsz.
* `/mine` A parancs használatával bányászhatsz.
* `/build` A parancs használatával építhetsz. (koncepció)

A `/chop` és `/mine` parancsok működnek, de módosításra várnak.

# A projekt menete
A fő funkció, ami tervben volt, hogy egy adott csatornába elküldi egy bizonyos Facebook oldal posztjait, hogy az emberek értesüljenek eseményekről.
Ezzel a probléma az volt, hogy a Facebook oldal az esetek többségében olyan eseményekről posztol, amelyeknek már vége volt.
Ennek tekintetében ezt az ötletet el kellett vetnünk.
[Dani](https://github.com/HazzyWazz) mindenkinek kiosztotta a feladatokat [Trello](https://trello.com)-n, amiknek illett késznek lennie a határidőre.
Ez magában foglalja a prezentációt, a robot alap parancsait és az API parancsokat.
Mindenki neki is állt a kiosztott feladatok elkészítéséhez.
