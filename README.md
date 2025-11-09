# Otvoreno_rac

# McDonald's Ice Cream Machines Dataset
Ovaj otvoreni skup podataka sadrži informacije o statusu i karakteristikama McDonald's mašina za sladoled u Hrvatskoj.

## Opis skupa
Skup podataka sadrži 10 zapisa, svaki koji opisuje jednu mašinu. Podaci uključuju tehničke detalje, servisne informacije, lokaciju i status.

## Metapodaci
- **Autor:** Elena Lukačević
- **Verzija:** 1.0
- **Jezik:** hrvatski
- **Licencija:** Creative Commons Zero v1.0 Universal
- **Datum izrade:** 2025-10-26
- **Format:** JSON, CSV
- **Broj zapisa:** 10
- **Broj atributa:** 12
- **Roditelj-dijete veza:** McDonald’s lokacija, Serviser
- **Baza podataka:** PostgreSQL
- **Atributi:**
  - ID (broj)
  - Lokacija (string)
  - Grad (string)
  - Država (string)
  - GPS (objekt s lat/lon)
  - Model (string)
  - Status (string)
  - Datum_posljednjeg_servisa (datum)
  - Serviser (objekt: Naziv, Kontakt)
  - Broj_porcija_dnevno (broj)
  - Napomena (tekst)

## App.py

Web aplikacija za pregled i preuzimanje podataka o McDonald’s mašinama za sladoled u Hrvatskoj. Podaci su pohranjeni u PostgreSQL bazi i povezani tablicama `machines`, `locations` i `services`.

## Funkcionalnosti

* Pregled podataka u tablici na web stranici.
* Filtriranje po svim atributima: Lokacija, Grad, Serviser, Model, Status, Datum posljednjeg servisa, Broj porcija dnevno, Napomena.
* Preuzimanje filtriranih ili svih podataka u **JSON** i **CSV** formatu.

## Instalacija

1. Kloniranje repozitorija:

   ```bash
   git clone https://github.com/elenalukacevic/Otvoreno_rac.git
   ```
2. Instalacija:

   ```bash
   pip install -r requirements.txt
   ```
3. Postavljanje PostgreSQL baze (`icecream`) i SQL dump iz repozitorija.
4. Pokretanje aplikacije:

   ```bash
   python app.py
   ```



