# Research Group Showroom

Helsingin yliopiston tietojenkäsittelytieteen laitoksen keväällä 2021 järjestämän harjoituskurssin 'Tietokantasovellus' harjoitustyö.

Sovellus tarjoaa tutkimusryhmien käyttöön työkalut tutkimusryhmän jäsenten, tutkimusryhmän ohjauksessa opinnäytteitä työstävien opiskelijoiden ja tutkimusryhmän toiminnasta kiinnostuneiden ulkopuolisten henkilöiden vuorovaikutukseen. Tutkimusryhmän jäsenille sovellus tarjoaa henkilökohtaisen esittelysivun, opiskelijoille mahdollisuuden tarkastella opinnäytetöiden aiheita ja niihin liittyviä aineistoja, ja vierailijoille yleiskuvan tutkimusryhmän julkaisemasta tutkimuksesta.

## Sovelluksen testaaminen

Sovellusta voi testata osoitteessa: [http://resgshowroom.herokuapp.com/](linkki)

Sovelluksella on neljä eri käyttäjäryhmää:

1. Vierailija: voit tarkastella tutkimusryhmän etusivua ja tutkimusryhmän jäsenten henkilökohtaisia sivuja, jotka on listattu etusivulla. Lisäksi voit jättää palautetta etusivun lomakkeella.

2. Opiskelija: voit rekisteröidä uuden tunnuksen etusivun login-lomakkeen alapuolella. Opiskelijana voit tarkastella opinnäytteiden aiheita. Linkki löytyy "Current role: Student" -tekstin alapuolelta, kun olet kirjautuneena sisään opiskelijatunnuksella.

3. Tutkimusryhmän jäsen: voit kirjautua sisään tutkimusryhmän jäsenenä seuraavilla tunnuksilla:
⋅⋅* käyttäjäni: member + lukuarvo väliltä 3 ja 6
⋅⋅* salasana: pass + sama lukuarvo väliltä 3 ja 6
Tutkimusryhmän jäsenenä voit luoda oman henkilökohtaisen alasivun kaikkien alasivujen listauksen alapuolelta ("Add new personal page").

4. Tutkimusryhmän johtaja (PI eli primary investigator): voit kirjautua sisään tutkimusryhmän johtajana seuraavalla tunnuksella:
⋅⋅* käyttäjänimi: pi
⋅⋅* salasana: sama kuin tutkimusryhmän jäsenillä yllä, mutta ilman lukuarvoa
Tutkimusryhmän johtajana voi muokata etusivulla tutkimusryhmän nimeä ja kuvausta sekä minkä tahansa alasivun nimeä ja kuvausta. Lisäksi voit tarkastella palautelomakkeen kautta lähetettyä palautetta sivun alalaidan 'View Feedback' -napista. Nähdyn palautteen voi arkistoida.

## Sovelluksen ominaisuudet

Sovelluksen ominaisuudet ovat seuraavat:

* Tutkimusryhmän johtaja voi luoda tutkimusryhmälle digitaalisena käyntikorttina toimivan sovelluksen etusivun, joka esittelee tutkimusryhmän toimintaa. [perustoteutus OK]
* Tutkimusryhmän jäsenet voivat kirjautua sisään ja ulos sekä luoda uuden tunnuksen ja henkilökohtaisen esittelysivun. [perustoteutus OK, uusien tunnusten luominen puuttuu]
* Etusivulle ja henkilökohtaisille esittelysivuille voi liittää mukaan asiantuntijuutta kuvaavia asiasanoja, julkaisuja ja yhteistyökumppaneita. [ainoastaan elementit asetettu paikoilleen]
* Tutkimusryhmän jäsenet voivat luoda uusia (tai poistaa vanhoja) opinnäytteiden aiheita. Aiheisiin voi liittää julkaisuja, aineistoja ja asiasanoja. [ei toteutettu]
* Opiskelijat voivat kirjautua sisään ja ulos sekä luoda uuden tunnuksen päästäkseen tarkastelemaan tutkimusryhmän jäsenten valitsemia opinnäytetöiden aiheita sekä niihin liittyviä julkaisuja ja aineistoja. [perustoteutus OK, julkaisut ja aineistot puuttuu]
* Opiskelijat, jotka ovat valinneet opinnäytteensä aiheen, pääsevät käsiksi opinnäytteen aiheeseen liitettyihin julkaisuihin ja aineistoihin. [ei toteutettu]
* Tutkimusryhmän jäsenet ja opiskelijat voivat kommunikoida keskenään. Opiskelijat voivat palauttaa opinnäytteiden versioita kommentointia varten. Sekä tutkimusryhmän jäsenet että opiskelijat voivat kommentoida keskeneräisiä opinnäytteitä. [ei toteutettu]
* Vierailijat voivat katsoa tutkimusryhmän etusivua ja tarkastella tutkimusryhmän jäsenten henkilökohtaisia esittelysivuja. [OK]
* Vierailijat voivat hakea sovelluksesta asiasanojen perusteella tutkimusryhmän jäseniä, joilla on tietty asiantuntijuus tai menetelmäosaaminen. [ei toteutettu]
* Vierailijat voivat jättää tutkimusryhmälle palautetta tai yhteydenottopyynnön esimerkiksi haastattelua varten. [perustoteutus OK]
