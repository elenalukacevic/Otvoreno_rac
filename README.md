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
- **Roditelj-dijete veza:** McDonald’s lokacija → Serviser
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

