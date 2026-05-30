# AktivOslo — App-konsept & Design

## 1. APP-KONSEPT

**Navn:** AktivOslo (evt. Ute.no / Løkka / Aktiv)
**Tagline:** "Finn det beste stedet — ute nå"
**Målgruppe:** Osloborgere og folk i Asker/Bærum som vil finne lavterskelaktiviteter raskt
**Plattform:** PWA (mobilfirst) + web

### Kjernetanke
AktivOslo er "Google Maps + Strava + Tripadvisor for lavterskelaktiviteter". Tre sekunder fra åpning til anbefaling. Du trenger ikke vite hva du vil — appen foreslår basert på vær, tid og hva som er nær deg.

---

## 2. INFORMASJONSARKITEKTUR

```
AktivOslo
├── 🏠 Hjem / Discover
│   ├── Vær-basert forslag (f.eks. "Perfekt for padel nå")
│   ├── Trending nær meg
│   ├── Kategorikort (horisontalt scroll)
│   └── Redaksjonelle lister ("Beste solnedgangssteder", "Åpent nå")
│
├── 🗺️ Kart
│   ├── Alle steder som ikoner
│   ├── Filterpanel (aktivitet, avstand, gratis/betalt, lys, sesong)
│   └── Kortvisning ved klikk på sted
│
├── 📋 Liste
│   ├── Sortering (rangering, avstand, nyest rated)
│   ├── Filtrering (samme som kart)
│   └── Stedskort med score + merker
│
├── 📍 Stedsside
│   ├── Bilder (bruker + redaksjonelle)
│   ├── Score-oversikt (totalpoeng + delscorer)
│   ├── "Passer best for"-merker
│   ├── Praktisk info (toalett, parkering, koll.transport, kiosk, lys, åpningstider)
│   ├── Bookinglenke (hvis relevant)
│   ├── Anmeldelser
│   ├── Kart/veibeskrivelse
│   └── Rapporter feil
│
├── ❤️ Mine steder
│   ├── Favoritter
│   └── "Vil besøke"-liste
│
└── 👤 Profil
    ├── Mine anmeldelser
    ├── Preferanser
    └── Innstillinger
```

---

## 3. SKJERMBILDER / WIREFRAMES (tekstform)

### STARTSKJERM — Discover
```
┌──────────────────────────────────┐
│  ☀️ 22° i Oslo · Lørdag 14:00   │
│                                  │
│  🎯 FORSLAG TIL DEG              │
│  ┌────────────────────────────┐  │
│  │ 🎾 Perfekt padelvær!       │  │
│  │ Bekkestua Padelklubb       │  │
│  │ ⭐ 8.4 · 1.2 km · GRATIS  │  │
│  └────────────────────────────┘  │
│                                  │
│  KATEGORIER ──────────────────►  │
│  🎾 🏐 ⛹️ ⛷️ 🏊 🏄 🌲 🛹      │
│                                  │
│  TRENDING NÆR DEG                │
│  ┌──────────┐ ┌──────────────┐  │
│  │Sognsvann │ │Padel Lysaker │  │
│  │ ⭐ 9.1  │ │ ⭐ 8.7       │  │
│  │ Bade+løp │ │ Booking req. │  │
│  └──────────┘ └──────────────┘  │
│                                  │
│  ÅPENT NÅ MED LYS                │
│  [Liste med steder...]           │
└──────────────────────────────────┘
```

### KARTVISNING
```
┌──────────────────────────────────┐
│  [FILTER ▼] [Aktivitet ▼] [km▼] │
│ ┌────────────────────────────┐   │
│ │     🗺️ OSLO-KART          │   │
│ │  🎾  🏀    🛹              │   │
│ │       🌲 ⭐9.1             │   │
│ │  🏊        🎾             │   │
│ │      📍DU ER HER          │   │
│ └────────────────────────────┘   │
│ ┌────────────────────────────┐   │
│ │ 📍 Sognsvann               │   │
│ │ Bade · Løping · Tur        │   │
│ │ ⭐ 9.1 · 0.8 km · GRATIS  │   │
│ │ [Se mer →]                 │   │
│ └────────────────────────────┘   │
└──────────────────────────────────┘
```

### STEDSSIDE
```
┌──────────────────────────────────┐
│ [← Tilbake]          [❤️] [↗️] │
│ ┌────────────────────────────┐   │
│ │       📸 BILDER (3)        │   │
│ └────────────────────────────┘   │
│                                  │
│  Sognsvann                       │
│  Bade · Løping · Tur · Natur     │
│  Nordmarka · Gratis              │
│                                  │
│  ⭐ 9.1 TOTALPOENG               │
│  Kvalitet      ████████░░  8.5  │
│  Beliggenhet   █████████░  9.2  │
│  Tilgjengelighet████████░  8.8  │
│  Vedlikehold   ████████░░  8.3  │
│  Kapasitet     ███████░░░  7.4  │
│  Fasiliteter   █████████░  9.0  │
│  Stemning      █████████░  9.5  │
│  Pris/verdi    ██████████ 10.0  │
│                                  │
│  PASSER BEST FOR                 │
│  🏃 Trening  👨‍👩‍👧 Familie  🐕 Hund │
│  🌅 Solnedgang  🤿 Morgenbad    │
│                                  │
│  PRAKTISK INFO                   │
│  🚽 Toalett ✓  🚗 Parkering ✓  │
│  🚌 T-bane ✓   ☕ Kiosk ✓     │
│  💡 Belysning: Nei               │
│  🕐 Åpent: Hele dagen           │
│                                  │
│  ANMELDELSER (142)               │
│  [Skriv anmeldelse +]            │
│  [Anmeldelseskort...]            │
└──────────────────────────────────┘
```

### FILTERVISNING
```
┌──────────────────────────────────┐
│  FILTRER STEDER         [✕ Lukk] │
│                                  │
│  AKTIVITET                       │
│  [Alle] [Racket] [Ball] [Vann]  │
│  [Natur] [Vinter] [Ekstrem]     │
│                                  │
│  OMRÅDE                          │
│  ○ Oslo sentrum                  │
│  ○ Nordmarka                     │
│  ○ Asker                         │
│  ○ Bærum                         │
│                                  │
│  AVSTAND FRA DEG                 │
│  [1km] [2km] [5km] [10km+]      │
│                                  │
│  TILGANG                         │
│  ☑ Gratis    ☐ Betalt           │
│  ☐ Booking nødvendig            │
│  ☑ Lys på kvelden               │
│                                  │
│  FASILITETER                     │
│  ☑ Toalett  ☑ Parkering        │
│  ☑ Koll.transport               │
│                                  │
│  VENNLIGHET                      │
│  ☑ Familievennlig               │
│  ☑ Hundevennlig                 │
│                                  │
│  SESONG                          │
│  [Sommer] [Vinter] [Hele året]  │
│                                  │
│  [🔍 VIS 47 STEDER]             │
└──────────────────────────────────┘
```

---

## 4. DATAMODELL FOR STEDER

```json
{
  "id": "uuid",
  "name": "string",
  "slug": "string",
  "description": "string",
  
  "location": {
    "lat": "number",
    "lng": "number",
    "address": "string",
    "neighborhood": "string",
    "municipality": "Oslo | Asker | Bærum",
    "area": "string (f.eks. Nordmarka, Frogner, Bekkestua)"
  },

  "activity_types": ["string"],
  // tennisbane, padelbane, volleyball, basketball, fotball,
  // bordtennis, tuftepark, badested, badstue, park, utsikt,
  // skatepark, discgolf, klatring, kajakkutleie, løperute,
  // sykling, akebakke, skøytebane, skiløype

  "access": {
    "is_free": "boolean",
    "price_range": "gratis | under 100kr | 100-300kr | over 300kr",
    "booking_required": "boolean",
    "booking_url": "string?",
    "opening_hours": "string",
    "evening_lighting": "boolean",
    "always_open": "boolean"
  },

  "facilities": {
    "toilet": "boolean",
    "changing_room": "boolean",
    "parking": "boolean",
    "public_transport": "boolean",
    "transport_details": "string?",
    "kiosk_cafe": "boolean",
    "cafe_name": "string?",
    "shower": "boolean",
    "lockers": "boolean",
    "equipment_rental": "boolean"
  },

  "suitability": {
    "family_friendly": "boolean",
    "dog_friendly": "boolean",
    "beginner_friendly": "boolean",
    "wheelchair_accessible": "boolean",
    "seasons": ["sommer", "høst", "vinter", "vår"]
  },

  "best_for_tags": ["string"],
  // date, vennegjeng, trening, rolig_tur, familie,
  // solnedgang, morgenbad, nybegynnere, hund, sosial

  "ratings": {
    "total_score": "number (1-10)",
    "quality": "number",
    "location": "number",
    "accessibility": "number",
    "maintenance": "number",
    "capacity": "number",
    "facilities_score": "number",
    "atmosphere": "number",
    "value_for_money": "number",
    "review_count": "integer"
  },

  "media": {
    "cover_image": "url",
    "images": ["url"],
    "user_images": ["url"]
  },

  "status": {
    "is_open": "boolean",
    "seasonal_closure": "string?",
    "reported_issues": ["string"],
    "last_verified": "date"
  },

  "meta": {
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "verified": "boolean",
    "featured": "boolean"
  }
}
```

---

## 5. RATINGMODELL

### Vektet totalpoeng
Totalscoren beregnes som vektet snitt av delscorene:

| Delscore          | Vekt | Begrunnelse |
|-------------------|------|-------------|
| Kvalitet          | 20%  | Kjernen av opplevelsen |
| Beliggenhet       | 15%  | Naturlig omgivelse |
| Tilgjengelighet   | 15%  | Transport og avstand |
| Vedlikehold       | 15%  | Kritisk for trygg bruk |
| Kapasitet/Kø      | 10%  | Frustrasjonsmoment |
| Fasiliteter       | 10%  | Praktiske behov |
| Stemning          | 10%  | Opplevelseskvalitet |
| Pris/Verdi        | 5%   | Laveste vekt — gratis er standard |

### Scoring-logikk
- Alle delscorer er 1–10
- Totalpoeng = Σ(delscore × vekt)
- Minimum 5 anmeldelser før sted vises med fullstendig score
- Automatisk "kvalitetsbonusmerke" ved totalpoeng ≥ 8.5

### Automatiske score-signaler
Appen kan automatisk justere ned:
- Vedlikehold → ved mange rapporter om "dårlig vedlikehold"
- Kapasitet → ved tidsbaserte rapporter om kø/fullt

---

## 6. KATEGORIER OG FILTRE

### Aktivitetskategorier (med emoji-ikoner)
```
RACKET & BAT      🎾 Tennis · 🏓 Padel · 🏓 Bordtennis
BALL              🏐 Volleyball · 🏀 Basketball · ⚽ Fotball
VANN              🏊 Bade · 🛶 Kajakkutleie · 🏄 SUP
NATUR & TUR       🌲 Park · 👁️ Utsikt · 🧭 Løperute · 🚵 Sykling
URBAN & EKSTREM   🛹 Skatepark · 🥏 Discgolf · 🧗 Klatring
FITNESS           💪 Tuftepark / Treningspark
VINTER            🛷 Akebakke · ⛷️ Skiløype · ⛸️ Skøytebane
```

### Filterdimensjoner
```
TILGANG:          Gratis | Betalt | Booking nødvendig
AVSTAND:          <1km | 1-3km | 3-7km | 7km+
OMRÅDE:           Oslo | Nordmarka | Asker | Bærum | Marka
TID PÅ DAGEN:     Åpent nå | Lys på kvelden | 24/7
SESONG:           Åpent nå | Sommer | Vinter | Hele året
VENNLIGHET:       Familie | Hund | Rullestol | Nybegynner
FASILITETER:      Toalett | Parkering | Koll.transport | Kiosk
SORTERING:        Rangering | Avstand | Nyest rated | Trendende
```

### Fargekodingsystem (visuelle merker)
```
🟢 GRATIS          — grønn badge
🔵 BETALT          — blå badge  
🟡 BOOKING REQ.    — gul badge
⬛ SESONGSTENGT   — grå badge
🔴 RAPPORTERT FEIL — rød badge
✅ TOPPRANGERT     — gull/stjerne
```

---

## 7. EKSEMPELDATA — 15 STEDER

### 1. Sognsvann
- Aktiviteter: Bade, Løperute, Tur, Hund
- Område: Nordmarka · Oslo
- Gratis · Alltid åpent
- Toalett ✓ · Parkering ✓ · T-bane (Sognsvann st.) ✓ · Kiosk ✓
- Belysning: Nei
- Totalpoeng: 9.1
- Passer best for: Familie, Hund, Morgenbad, Trening, Rolig tur
- Sesong: Hele året (bading sommer)

### 2. Bekkestua Padel (Bærum)
- Aktiviteter: Padel
- Område: Bekkestua · Bærum
- Betalt · Booking nødvendig · Lys ✓
- Totalpoeng: 8.4
- Passer best for: Vennegjeng, Trening

### 3. Frognerparken
- Aktiviteter: Park, Volleyball, Fotball, Løperute
- Område: Frogner · Oslo
- Gratis · Alltid åpent
- Toalett ✓ · Kiosk ✓ · T-bane ✓
- Totalpoeng: 8.9
- Passer best for: Familie, Date, Vennegjeng, Rolig tur, Solnedgang

### 4. Ekebergsletta Skatepark
- Aktiviteter: Skatepark
- Område: Ekeberg · Oslo
- Gratis · Alltid åpent
- Belysning: Ja · Toalett: Nei
- Totalpoeng: 8.2
- Passer best for: Nybegynnere, Vennegjeng, Ungdom

### 5. Slottsparken
- Aktiviteter: Park, Løperute, Utsikt
- Område: Sentrum · Oslo
- Gratis · Alltid åpent
- T-bane ✓
- Totalpoeng: 8.6
- Passer best for: Date, Rolig tur, Solnedgang

### 6. Oslofjordbadet / Hvervenbukta
- Aktiviteter: Bade, SUP, Kajakkutleie
- Område: Søndre Nordstrand · Oslo
- Gratis inngang · Kajakkutleie betalt
- Toalett ✓ · Parkering ✓ · Kiosk ✓
- Totalpoeng: 8.8
- Passer best for: Familie, Morgenbad, Date, Vennegjeng

### 7. Holmenkollen Skiarena
- Aktiviteter: Skiløype, Løperute, Utsikt
- Område: Holmenkollen · Oslo
- Gratis skønnmark · T-bane ✓ · Kiosk ✓
- Belysning: Ja (preparerte løyper)
- Totalpoeng: 9.0
- Sesong: Vinter (ski), Hele året (løping/tur)
- Passer best for: Familie, Trening, Utsikt

### 8. Asker Tennisklubb
- Aktiviteter: Tennis
- Område: Asker sentrum · Asker
- Betalt · Booking nødvendig · Lys ✓
- Garderobe ✓ · Parkering ✓
- Totalpoeng: 8.0
- Passer best for: Trening, Vennegjeng

### 9. Hauktjern (Discgolf)
- Aktiviteter: Discgolf, Tur, Hund
- Område: Nordmarka · Oslo
- Gratis · Alltid åpent
- Toalett: Nei · Parkering: Begrenset
- Totalpoeng: 7.9
- Passer best for: Vennegjeng, Familie, Hund, Nybegynnere

### 10. Frognerbadet
- Aktiviteter: Bade, Badstue
- Område: Frogner · Oslo
- Betalt · Booking anbefalt (badstue) · Sesong: Sommer
- Toalett ✓ · Garderobe ✓ · Kiosk ✓
- Totalpoeng: 9.3
- Passer best for: Familie, Vennegjeng, Date, Morgenbad

### 11. Kolsåstoppen
- Aktiviteter: Utsikt, Tur, Klatring
- Område: Kolsås · Bærum
- Gratis · T-bane (Kolsås) ✓
- Totalpoeng: 9.0
- Passer best for: Date, Familie, Solnedgang, Klatring nybegynnere

### 12. Frogner Stadion (Skøytebane)
- Aktiviteter: Skøytebane
- Område: Frogner · Oslo
- Betalt (leieskøyter tilgjengelig) · Sesong: Vinter
- Toalett ✓ · Garderobe ✓ · T-bane ✓
- Totalpoeng: 8.5
- Passer best for: Familie, Date, Nybegynnere

### 13. Tryvann Vinterpark
- Aktiviteter: Akebakke, Skøytebane, Skiløype
- Område: Tryvann · Oslo
- Betalt · Sesong: Vinter
- Parkering ✓ · Kiosk ✓ · Lys ✓
- Totalpoeng: 8.7
- Passer best for: Familie, Barn, Nybegynnere

### 14. Lysaker Padelklubb
- Aktiviteter: Padel
- Område: Lysaker · Bærum
- Betalt · Booking nødvendig · Lys ✓
- Garderobe ✓ · Parkering ✓
- Totalpoeng: 8.7
- Passer best for: Trening, Vennegjeng

### 15. Grefsenkollen
- Aktiviteter: Utsikt, Tur, Akebakke (vinter), Løperute
- Område: Grefsen · Oslo
- Gratis · Buss ✓ · Kiosk ✓
- Totalpoeng: 8.8
- Sesong: Hele året
- Passer best for: Date, Familie, Solnedgang, Rolig tur

---

## 8. MVP — MINIMUM VIABLE PRODUCT

### Fase 1 — MVP (2-3 måneder)
**Mål:** Bevis konseptet og bygg en liten lojal brukerbase

Inkludert:
- ✅ Listevisning med filtrering (aktivitet, gratis/betalt, område)
- ✅ Stedsside med fullstendig info og bilder
- ✅ Enkel rating og anmeldelser
- ✅ Statisk datasett med 30-50 steder i Oslo/Asker/Bærum
- ✅ Mobiloptimalisert responsivt design
- ✅ Søkefunksjon
- ✅ Favorittliste (lagret lokalt)

IKKE i MVP:
- ❌ Kart (komplisert og kostbart)
- ❌ GPS-basert "nær meg"
- ❌ Brukerinnlogging
- ❌ Bildeoppasting

---

## 9. VIDERE FUNKSJONER (post-MVP)

### Fase 2 — Vekst
- 🗺️ Kartvisning med Mapbox/Google Maps
- 📍 "Nær meg" med GPS
- 👤 Brukerkontoer og innlogging
- 📸 Bildeoppasting av brukere
- 🔔 Push-varsler ("Noen likes anmeldelsen din")
- ⛅ Vær-integrasjon og forslag

### Fase 3 — Community
- 🏆 Poeng og badges for anmeldere
- 📣 Rapportering av stengt/dårlig vedlikehold
- 📅 "Planlegg tur" — del med venner
- 🗓️ Arrangementer på stedene (turneringer etc.)

### Fase 4 — Monetisering
- 💼 Sponsede oppføringer for betalte anlegg (f.eks. padelklubber)
- 🎟️ Booking-integrasjon med provisjon
- 🌍 Ekspansjon til andre byer

---

## 10. TEKNISK IMPLEMENTERINGSPLAN

### Stack — Anbefalt
```
Frontend:     React / Next.js (PWA)
Styling:      Tailwind CSS + shadcn/ui
Kart:         Mapbox GL JS (billigst for hobbyprosjekt)
Backend:      Supabase (DB + Auth + Storage)
Hosting:      Vercel (gratis tier for MVP)
Bilder:       Cloudinary (gratis tier)
Vær-API:      OpenWeatherMap (gratis tier)
```

### Alternativ: Base44 App
Hele appen kan bygges i Base44 App Builder med:
- Entities for steder, ratings, anmeldelser, brukere
- Kart-komponent (Mapbox-integrasjon)
- Filtreringslogikk i frontend
- Brukerinnlogging innebygd

### Database-tabeller
```
places          — Alle steder (se datamodell)
ratings         — En rad per bruker per sted
reviews         — Anmeldelser med tekst og bilder
users           — Brukerprofiler
favorites       — Bruker ↔ sted
issues_reported — Rapporterte problemer
```

### Datatopulasjon (Fase 1)
1. Manuell kurert liste (start med 50 steder)
2. Data fra kommunale databaser (Oslo Idrettsanlegg-register)
3. OpenStreetMap for koordinater og basisinfo
4. Frivillige bidragsytere / redaksjonsgruppe

### Performance-prinsipper
- Server-side rendering for SEO og rask første innlasting
- Lazy load bilder
- Caching av stedsliste (oppdateres daglig)
- Offline-modus med sist besøkte steder (PWA)

### Sikkerhet og moderering
- Anmeldelser godkjennes av moderator (eller AI-filter) før publisering
- Rapporterte feil → admin-dashboard
- Rate limiting på anmeldelser per bruker
```
