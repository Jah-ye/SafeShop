 Teknisk Dokumentasjon: SafeShop
 Systemversjon: 1.0.0
 Utarbeidet av: Jahye
 Dato: 12.juni 2026

Del 1: Teknisk dokumentasjon (For IT-avdelingen)

 1. Slik er systemet bygget (Tredelt modell)
 Appen består av tre deler som jobber sammen:
  
  Frontend (Nettsiden): index.html – Dette er siden kunden ser i nettleseren sin. Her velger de et produkt og skriver navnet sitt.
  Backend (Hjernen): app.py – Et Python-program som tar imot bestillingene og sjekker at alt er i orden.
  Database (Lagring): safeshop.db – En enkel SQLite-databasefil som lagrer alle bestillingene permanent.

 2. Nettverk og kommunikasjon
    Når kunden trykker på "Fullfør bestilling", sender nettsiden en digital beskjed (en POST-forespørsel) over nettverket til Python.
    Python-serveren kjører lokalt på PC-en og lytter på en egen kanal kalt Port 5000.
    I koden er CORS skrudd på. Dette gjør at nettsiden får lov til å snakke med Python-serveren uten å bli blokkert av nettleseren.

1. Sikkerhet og personvern
Sikkerhet (Input-validering):** Python-koden sjekker alltid navnet kunden skriver inn. Hvis noen prøver å hacke oss ved å skrive inn skadelige tegn (SQL-injeksjon), oppdager Python dette, stopper bestillingen og gir en rød feilmelding.

GDPR