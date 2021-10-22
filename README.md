# Ravintolasovellus

Sovelluksen ideana on mahdollistaa ravintoloiden etsiminen ja niiden tietojen hakeminen. Tiedoista selviää mm. aukioloajat, osoitteet, ruokalista ja kuinka ravintola ottaa huomioon erilaiset ruokavaliot.

Lisäksi käyttäjät voivat arvostella haluamansa ravintolan antamalla sille arvosanan ja halutessaan "vapaa sana" muotoisen arvostelun. Käyttäjän lisäksi sivuilla on ylläpitäjä, joka voi hallinnoida tietoja ravintoloista, sekä käyttäjistä ja mitä tietoja näistä julkisesti näytetään.

## Ensimmäinen versio

Sovellusta pääsee testaamaan [Heroku-sivua käyttäen](http://tsoha-raflasovellustp.herokuapp.com/).

Jos et halua luoda omaa käyttäjätunnustasi, voit hyvin käyttää testaukseen käyttäjää admintest salasanalla abc123. Voit myös halutessasi luoda oman tunnuksen.

Sovelluksessa on tällä hetkellä mahdollista luoda *vain* admin-tunnus. Vaikka valitsisit rekisteröinnin yhteydessä olevasi vain käyttäjä, sinulla on silti adminin oikeudet.

Itse ohjelman toiminnallisuus on tällä hetkellä siinä vaiheessa, että käyttäjän voi luoda ja sillä voi kirjautua sisään, uuden ravintolan voi lisätä tietokantaan nimen, ravintolan kuvauksen ja osoitteen perusteella. Ravintolalistauksesta näkee kaikki tietokannassa olevat ravintolat ja listauksen sisältä voidaan siirtyä katsomaan ravintolasivua, jossa on tällä hetkellä vain kuvaus ravintolasta.

Ohjelmaa voi siis testata luomalla käyttäjän (kirjautuu automaattisesti sisään rekisteröinnin jälkeen) ja lisäämällä ravintoloita järjestelmään. Tämän jälkeen voi tarkistaa onko ravintola ilmestynyt ravintolalistaukseen ja viekö sen linkki oikeaan paikkaan. Sivuille on lisäksi luotu jo pohjat tuleville toiminnallisuuksille, mutta sivuilla vierailu johtaa virheilmoitukseen. 

## Toinen versio

Sovellus on edennyt siihen vaiheeseen, että ravintolat voidaan etsiä kartalta ja karttatagien perusteella pääsee myös ravintolan sivuille.

Ravintolat on myös mahdollista ryhmitellä omien tagien avulla, joskin vielä niitä ei voi hakea tagien perusteella. Lisäksi ravintolan sivuilla on mahdollista kirjoittaa sanallinen arvostelu. Sanallinen arvostelu ei tällä hetkellä ole aikaleimattu tai merkitty tietyn käyttäjän arvosteluksi.

Myös ravintolan etsiminen kuvauksen perusteella on valmis. Haku palauttaa ravintolalistauksen kaikista ravintoloista, joiden kuvauksessa haettu merkkijono esiintyy.

Viimeisten pienten ominaisuuksien lisäämisen lisäksi sovelluksen ulkoasu tulee julkaistuksi viimeisessä palautuksessa. Ulkoasun jättäminen viimeiseen palautukseen on tarkoituksenmukaista, sillä ensin on haluttu varmistaa sovelluksen toimivuus.

## Huomioita

Ajoittain sivusto kaatuu, kun ravintolaa yrittää lisätä tai tietyn ravintolan sivulle yrittää mennä. Myös joskus arvostelujen yhteyksissä. En ole löytänyt tälle mitään muuta järkevää selitysä, kuin se, että geopy-kirjasto ilmoittaa Service Timeoutista. Esimerkiksi torstaina 14.10 en pystynyt testaamaan mitään lokaalisti, mutta Herokussa kaikki toimi hienosti. Toisaalta perjantaina asia oli toisinpäin. Tämä on varmaan ongelma, jonka kanssa joutuu elämään ilmaisversioiden takia.

## Ominaisuudet:

* Ravintolat voi etsiä kartasta tai sanahaun perusteella (valmis)
* Ravintolat voidaan järjestää arvosanan perusteella
* Sivustolle voi luoda käyttäjätunnuksen (myös ylläpitäjälle) (Valmis)
* Käyttäjät voivat arvostella ravintolan numeroasteikolla ja/tai sanallisesti (sanallinen arvostelu lähes valmis)
* Ylläpitäjä voi hallinoida ravintoloiden tietoja ja käyttäjien kommentteja (Osittain valmis)
* Ylläpitäjä voi luoda ravintolaluokkia (esimerkiksi vegaaniystävällinen ravintola) (valmis)
* (**Mahdollisesti**) Käyttäjä voi saada "arvonimen" arvostelujen määrän perusteella
