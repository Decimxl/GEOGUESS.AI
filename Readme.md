# Hvad vil vi lave?

## Hvad er GeoGuessr?

Geoguessr er et browserspil, hvor man bliver præsenteret med en tilfældig koordinat, hvori der eksisterer google streetview. Målet er at gætte tæt på lokationens koordinat.

NMPZ er et filter, der fjerne muligheden for at zoome, køre og kigge rundt: No Move Pan Zoom. Man har altså kun et enkelt billede at gætte ud fra.

## Hvad skal vores AI kunne?

Vores AI tager et screenshot af skærmen for lokationen. Billedet bliver analyseret af vores AI, der er trænet på data fra Plonkit.net. Den giver en procentvis sikkerhed for, hvilket land billedet er i og laver et gæt baseret på det. 

Den vil eventuelt kunne trænes på data fra spil. 

# Hvordan vil vi lave det?
vi vil starte med at lave et program der tager alle billeder fra "plonk it" som er en trænings hjemmeside til geoguesser og bruger billederne i et program der vil finde features fra billederne som fx. farve og metas som kun er i specifike lande. alt det vil blive brugt i en csv fil i et neural network som vil bruge det til at træne. den bliver puttet i en pkl fil og indsat i en browser extention så den kan bruges til geoguesser.

# Hvilke værktøjer, biblioteker, sprog, programmer m.m. I vil benytte
vi vil bruge biblioteket sklearn, pandas, pickle. 
vi vælger at bruge python som kode sporg 
samt vil vi bruge bilderer fra https://www.plonkit.net/guide
til at kode AI,en vil vi bruge VS Code. og så vil vi bruge github til at dele projektet mellem os.