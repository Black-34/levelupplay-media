# LevelUp Content-Playbook (@levelupplay2026, YouTube @levelupplay2026)

## Ziel
Reichweite aufbauen mit GTA 6 (später weitere Spiele), dann eigene Spiele bewerben.

## Regeln
- Rockstar-Material (Screenshots/Logos in assets/rockstar) nur in eigenen, bearbeiteten Beiträgen. Keine Spoiler (Ende, Zwischensequenzen, Story-Wendungen), keine geleakten Inhalte.
- Keine fremden Songs ins Video schneiden. Musik: audio/levelup_vicecity_synthwave.mp3 (eigener, lizenzfreier Track) oder neue Tracks über vidIQ generate_music.
- Keine fremden YouTube/TikTok-Videos reposten. Keine gekauften Follower, Bots oder Spam.
- Jede Caption: Hook-Frage, Aufruf zum Kommentieren/Speichern/Folgen, Hinweis "Fan-Content, nicht mit Rockstar Games verbunden", 12-15 Hashtags.
- Format: Reels 9:16, 1080x1920, 12-20 s, Text in den ersten 0,5 s; Karussells 1080x1350 JPEG.

## Serien-Ideen (nach Klick-Recherche mit vidIQ)
1. GTA 6 Radio: alle Sender mit Songliste (tools/make_radio.py, Liste in assets/radio_tracklists_community.md)
2. Figuren-Steckbriefe (Jason, Lucia, Cal, Boobie, DreQuan, Real Dimez, Raul, Brian) aus assets/rockstar/shots
3. Die 6 Regionen einzeln
4. Tipps für den Start / Geld verdienen / Cheats (nur mit belegten Fakten)
5. PC-/Konsolen-Fakten

## Wachstumsplan (ab 21.11.2026)
Ziel: in 30 Tagen die ersten 1.000 Follower auf Instagram, dann Reichweite auf YouTube Shorts aufbauen.

### Tagesplan Instagram (4 Durchläufe: 10:47, 14:47, 18:47, 21:47)
- 10:47 Reel aus einer Serie (Radio, Figuren, Regionen)
- 14:47 Karussell zum Speichern (Listen, Tipps, "Alle X in GTA 6") – Karussells werden oft gespeichert und geteilt
- 18:47 Reel mit dem stärksten Thema des Tages (bester Hook)
- 21:47 Reel als Trial Reel (create_video_post mit trial_params graduation_strategy SS_PERFORMANCE): erreicht nur Nicht-Follower, geht bei guten Werten automatisch an Follower
Wenn die Warteschlange nur Reels hat, ist das in Ordnung; Karussells bei Nachschub mit einplanen.

### Jeder Durchlauf zusätzlich
- Eine Story posten (create_story): Standbild aus dem gerade geposteten Beitrag, 1080x1920 JPEG, Text "Neuer Beitrag – jetzt ansehen". Story-Bilder in queue/<ordner>/story.jpg erzeugen, pushen, Raw-URL verwenden.
- Auf alle echten Kommentare antworten, möglichst mit Gegenfrage (bringt mehr Kommentare).

### Jeden Montag (erster Durchlauf der Woche)
- Mit Windsor get_data (instagram) Aufrufe, Reichweite, Saves, Shares und Follower der letzten 7 Tage holen.
- Die 3 besten Beiträge bestimmen; deren Thema/Format für die neue Woche öfter verwenden, die 3 schwächsten Formate seltener.
- Ergebnis kurz in reports/<datum>.md festhalten und dem Nutzer melden.

### Hooks (erste Sekunde)
- Frage oder Zahl: "Diese 10 Songs …", "Das wusstest du nicht über …", "Alle 6 …"
- Großer Text oben, Bewegung ab dem ersten Bild, 12-20 s Länge, Ende mit Frage + "Folgen für Teil X".

### Serien-Plan (je Serie mehrere Teile, nummeriert)
1. GTA 6 Radio – alle Sender (ca. 20 Teile)
2. Figuren-Steckbriefe (8 Teile)
3. Regionen einzeln (6 Teile)
4. "Wusstest du?" Fakten zu GTA 6 (nur belegte Fakten)
5. Tipps für den Start / Geld verdienen (nur belegte Fakten)
6. Umfrage-Karussells ("Welcher Sender ist der beste? 1-7")

### Hashtags
12-15 pro Beitrag: 4 große (#gta6 #gtavi #gaming #gamer), 5 mittlere (#gta6radio #vicecity #gta6music #gamingdeutschland #ps5), 4 spezielle zum Thema.
