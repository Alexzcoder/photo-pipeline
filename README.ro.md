# Pipeline foto covoare — instrucțiuni (Windows)

Îi dai un folder cu poze simple de covoare și primești poze de marketing: covorul întins în studio,
rulat, și pus în living, dormitor, sufragerie, cameră de copii etc., în stilul de mobilă și lumina
pe care le alegi. Modelul este Nano Banana Pro, image-to-image, deci modelul și culorile covorului
rămân exact ca în poza originală. Claude Code face toată treaba prin contul tău de Higgsfield sau
OpenArt. Nu trebuie chei API, nu trebuie server.

## Instalare (o singură dată, cam 15 minute)

Ai nevoie de un abonament Claude Pro sau Max (Claude Code nu merge pe planul gratuit).

1. **Instalează Python.** Descarcă de la https://www.python.org/downloads/ și rulează instalarea.
   Pe primul ecran bifează **„Add python.exe to PATH”**, apoi Install Now.
2. **Instalează Git for Windows.** https://git-scm.com/downloads/win, lasă toate opțiunile implicite.
   Îi dă lui Claude un terminal în care să ruleze scripturile.
3. **Instalează Claude Code.** Deschide PowerShell (Start, scrie „PowerShell”) și lipește:
   ```
   irm https://claude.ai/install.ps1 | iex
   ```
   Închide PowerShell, deschide-l din nou și verifică cu `claude --version`.
4. **Conectează un generator de imagini la contul tău Claude.** În browser intră pe
   https://claude.ai/settings/connectors, adaugă **Higgsfield** (preferat, cel mai ieftin) sau
   **OpenArt** și loghează-te în serviciul respectiv când ți se cere. Pozele se plătesc din
   creditele contului respectiv.
5. **Descarcă pipeline-ul.** În PowerShell:
   ```
   cd $HOME\Desktop
   git clone https://github.com/Alexzcoder/photo-pipeline.git
   cd photo-pipeline
   python -m pip install pillow
   ```
6. **Loghează-te în Claude Code.** Tot din folderul acela rulează `claude`. Se deschide browserul;
   loghează-te cu același cont Claude care are conectorul. Când apare promptul, scrie `/mcp` și
   verifică dacă conectorul apare ca „connected” (poate cere o autorizare o singură dată).

## De fiecare dată când îl folosești

1. Pune pozele cu covoare în orice folder, de exemplu `C:\Users\tu\Desktop\covoare noi`.
   Numește fiecare fișier cu dimensiunea în metri: `1.6x2.3 albastru.jpg`, `200x290 ottoman.jpg`.
   Dacă un nume nu are dimensiune, Claude te va întreba.
2. Deschide PowerShell, intră în folderul pipeline-ului și pornește Claude:
   ```
   cd $HOME\Desktop\photo-pipeline
   claude
   ```
3. Scrie, cu calea folderului tău:
   ```
   /carpet-shots C:\Users\tu\Desktop\covoare noi
   ```
4. Răspunde la întrebări: ce camere, stilul mobilei, lumina, câte poze per cameră, și dacă pozele
   au bannerul cu prețul pe ele. Claude îți spune câte credite ai și cât costă rularea.
5. Claude face primul covor, îți spune cum arată, și te întreabă înainte să continue cu restul.
6. Rezultatele ajung în `<folderul tău>\shots\<covor>\`. La final Claude raportează câte poze a
   făcut și câte credite a consumat. S-a întrerupt? Pornește `claude` din nou și scrie
   „continue the pipeline”.

## Opțiuni
- Camere/scene: studio, rolled, livingroom, bedroom, dining, entryway, office, readingnook, openplan, lounge, kitchen, kidsroom, playroom, nursery
- Stiluri: classic-oriental, modern-minimal, vintage-distressed, art-deco, botanical, scandi-soft, luxe-baroque, bold-contrast, kids
- Lumină: daylight, golden, evening, overcast

## Costuri
Higgsfield: 2 credite per poză. Planul Ultimate dă 1200 de credite pe lună și creditele nefolosite
se pierd la resetarea lunară, adică vreo 600 de poze sau 85 de covoare pe lună care altfel se pierd.
OpenArt: 40 de credite per poză. 7 poze per covor, deci 100 de covoare înseamnă 700 de poze:
1.400 de credite Higgsfield sau 28.000 de credite OpenArt. Claude spune soldul înainte de fiecare
rulare și creditele consumate la final.

## Dacă ceva nu merge
- `claude` nu e recunoscut: închide și redeschide PowerShell.
- `python` nu e recunoscut: reinstalează Python cu „Add python.exe to PATH” bifat.
- Conectorul nu apare la `/mcp`: verifică pe claude.ai/settings/connectors că e adăugat și că te-ai
  logat în Claude Code cu același cont.
