# Research Group Showroom

Helsingin yliopiston tietojenkäsittelytieteen laitoksen keväällä 2021 järjestämän harjoituskurssin 'Tietokantasovellus' harjoitustyö.

Sovellus tarjoaa tutkimusryhmien käyttöön työkalut tutkimusryhmän jäsenten, tutkimusryhmän ohjauksessa opinnäytteitä työstävien opiskelijoiden ja tutkimusryhmän toiminnasta kiinnostuneiden ulkopuolisten henkilöiden vuorovaikutukseen. Tutkimusryhmän jäsenille sovellus tarjoaa henkilökohtaisen esittelysivun, opiskelijoille mahdollisuuden tarkastella ja varata tutkimusryhmän jäsenten ohjaamien opinnäytetöiden aiheita sekä palauttaa keskeneräisiä tekstejä kommentteja varten, ja vierailijoille yleiskuvan tutkimusryhmän julkaisemasta tutkimuksesta.

## Sovelluksen testaaminen

Sovellusta voi testata seuraavassa osoitteessa: [linkki](http://resgshowroom.herokuapp.com/)

Sovelluksella on neljä eri käyttäjäryhmää:

1. Vierailija: voit tarkastella tutkimusryhmän etusivua ja tutkimusryhmän jäsenten henkilökohtaisia sivuja, jotka on listattu etusivulla. Lisäksi voit jättää palautetta etusivun lomakkeella.

2. Opiskelija: voit rekisteröidä uuden tunnuksen etusivun login-lomakkeen alapuolella. Opiskelijana voit tarkastella opinnäytteiden aiheita vasemmalta löytyvän "Student Topics" -napin takaa, joka tulee näkyviin, kun olet kirjautuneena sisään opiskelijatunnuksella. Kun olet varannut itsellesi halutun aiheen "Reserve this topic" -napilla, pääset uppaamaan työsi viimeisimmän version, lukemaan sen ohjaajan antamaa palautetta, ja lähettämään omat kysymyksesi ja kommenttisi ohjaajalle. Viimeisin upattu tiedosto on myös aina ladattavissa.

3. Tutkimusryhmän jäsen: voit kirjautua sisään tutkimusryhmän jäsenenä seuraavilla tunnuksilla:
* käyttäjäni: member + lukuarvo väliltä 3 ja 6
* salasana: pass + sama lukuarvo väliltä 3 ja 6

Tutkimusryhmän jäsenenä voit luoda oman henkilökohtaisen alasivun kaikkien alasivujen listauksen alapuolelta ("Add new personal page"). Testatessa huomaa, että member3 omaa jo oman alasivun ([Duis Sagittis](http://resgshowroom.herokuapp.com/member_page/3)), mutta ryhmän jäsenet eivät. Omalle alasivullesi voit lisätä tai poistaa julkaisujasi ja tutkimustasi kuvaavia asiasanoja. Julkaisujen ja asiasanojen poistamisen jälkeen ohjaudut takaisin koko sovelluksen etusivulle. Lisäksi voit opinnäytteiden aiheiden [pääsivulla](http://resgshowroom.herokuapp.com/student_topics/0) lisätä uuden aiheen, jonka vastuuhenkilöksi asetut. Voit jättää oman vastualueesi aiheisiin kommentteja ja palautetta niille opiskelijoille, jotka työskentelevät aiheen parissa, upata dokumentteja sekä ladata viimeisimmäksi upatun dokumentin.

4. Tutkimusryhmän johtaja (PI eli primary investigator): voit kirjautua sisään tutkimusryhmän johtajana seuraavalla tunnuksella:
* käyttäjänimi: pi
* salasana: sama kuin tutkimusryhmän jäsenillä yllä, mutta ilman lukuarvoa

Tutkimusryhmän johtajana voit muokata etusivulla tutkimusryhmän nimeä, kuvausta, julkaisuja sekä tutkimusryhmän tutkimusta kuvaavia asiasanoja. (PI omaa käytännössä admin-oikeudet: voit myös muokata minkä tahansa alasivun kaikkia kenttiä.) Myös etusivulla alalaidasta löytyviä yhteistyökumppaneiden logoja voidaan lisätä tai poistaa. Etusivulta voit lisäksi siirtyä tarkastelemaan palautelomakkeen kautta lähetettyjä palautteita sivun alalaidan 'View Feedback' -napista. Nähdyn palautteen voi arkistoida.

## Sovelluksen ominaisuudet

Sovelluksen ominaisuudet ovat seuraavat:

* Tutkimusryhmän johtaja voi luoda tutkimusryhmälle digitaalisena käyntikorttina toimivan sovelluksen etusivun, joka esittelee tutkimusryhmän toimintaa.
* Tutkimusryhmän jäsenet voivat kirjautua sisään ja ulos sekä luoda henkilökohtaisen esittelysivun.
* Etusivulle ja henkilökohtaisille esittelysivuille voi liittää mukaan asiantuntijuutta kuvaavia asiasanoja ja julkaisuja. Lisäksi etusivulle voi liittää yhteistyökumppaneiden logoja.
* Tutkimusryhmän jäsenet voivat luoda uusia opinnäytteiden aiheita.
* Opiskelijat voivat kirjautua sisään ja ulos sekä luoda uuden tunnuksen päästäkseen tarkastelemaan tutkimusryhmän jäsenten valitsemia opinnäytetöiden aiheita sekä valitsemaan itselleen aiheen.
* Tutkimusryhmän jäsenet ja opiskelijat voivat kommunikoida keskenään. Opiskelijat voivat palauttaa opinnäytteiden versioita kommentointia varten. Sekä tutkimusryhmän jäsenet että opiskelijat voivat kommentoida keskeneräisiä opinnäytteitä.
* Vierailijat voivat katsoa tutkimusryhmän etusivua ja tarkastella tutkimusryhmän jäsenten henkilökohtaisia esittelysivuja.
* Vierailijat voivat jättää tutkimusryhmälle palautetta tai yhteydenottopyynnön esimerkiksi haastattelua varten.

## Lisensseihin liittyviä huomioita

Kaikki käytetyt logot ovat peräisin [Pexels-sivustolta](https://www.pexels.com/), jossa ne on lisensoitu seuraavasti:

* Free to use.
* No attribution required.
