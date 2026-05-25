# TEDxVibe

TEDxVibe è una piattaforma mobile cloud-native che suggerisce talk TEDx in base allo stato emotivo dell’utente.

L’obiettivo del progetto è ridurre il “paradosso della scelta”, aiutando le persone a trovare rapidamente il contenuto più adatto al proprio stato d’animo, favorendo benessere mentale, motivazione e crescita personale.

---

## Obiettivi

- Rendere i contenuti TEDx più accessibili e immediati
- Offrire raccomandazioni personalizzate basate sulle emozioni
- Ridurre il tempo speso nella ricerca dei contenuti
- Creare un’esperienza semplice, veloce e intuitiva

---

## Target Utenti

- Persone in cerca di motivazione quotidiana
- Studenti e lavoratori stressati
- Pendolari
- Utenti interessati alla crescita personale e al benessere mentale

---

## Tecnologie Utilizzate

### Frontend Mobile
- Flutter

### Cloud & Backend
- AWS Lambda
- AWS API Gateway

### Database
- MongoDB Atlas

### Architettura
- Cloud-native
- Serverless
- Scalabile

---

## Architettura del Sistema

L’app Flutter comunica con API Gateway, che inoltra le richieste alle funzioni AWS Lambda.

Le Lambda interrogano MongoDB Atlas contenente il dataset dei video TEDx elaborati e categorizzati per emozione.

Il sistema restituisce quindi il talk più adatto allo stato emotivo selezionato dall’utente.

---

## Release Plan

Il progetto è organizzato tramite metodologia Agile in 4 Sprint:

1. Analisi requisiti e progettazione
2. Sviluppo Data Layer
3. Sviluppo lambda functions
4. Implementazione app mobile

---

## Valore del Progetto

TEDxVibe combina empatia e tecnologia per offrire un supporto rapido e personalizzato.

Invece di cercare per minuti tra migliaia di video, l’utente riceve immediatamente il contenuto più utile per il proprio momento emotivo.

---

## Repository Contents

- `TEDxVibe.pdf` → presentazione del progetto
- `README.md` → documentazione del progetto

---

## Autori

- Giorgio Passarella
- Massimiliano Federico Gervasoni
