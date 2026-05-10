# Tic Tac Toe Stockfish


## Hvad er Tic Tac Toe?

Tic tac toe, eller kryds og bolle, er et spil spillet på en 3x3 matrix, hvor hvert felt kan have et kryds eller en bolle sat. Man skal have 3 krydser, eller boller, efterfulgt af hindanden i diagonalen eller lige for at vinde.  

## Hvad skal vores AI kunne?

Vores AI skal kunne vinde i Tic Tac Toe i så mange spil som muligt.

## Hvordan vil vi lave den?
vi træner en AI, med 9 inputs(en til være plads på bordet), ved at få den til at spille tic tac toe mod sig selv og bliver bedre og så skal den hookes op til et spil tic tac toe som man kan spille imod.

##ekstra
Python kører kun et program på en core på cpuen, så hvis man vil lave 50k tests tager det ~8 minutter, hvilket svarer til omkring 100 spil i sekundet. 
Vi kan derimod bruge multiprocessing og køre det samme program på flere kerner af cpuen og bruge OS til at se, hvor mange kerner der er i cpuen. Mads har en intel I7 cpu, hvilket har 20 kerner. Vi kan dermed træne vores AI på 18 cores, hvilket giver 2 cores til andet arbejde. Vi kan altså gå fra 100 spil i sekundet til 1800 spil i sekundet. Vi gemmer alle vores AI som workers i hver deres pickle og laver en turnering, hvor de alle spiller ~10k til 50k spil mod hindanden. Vinderen af turneringen bliver gemt som den AI man kan spille mod. Ved ny træning bliver AIen trænet mod nye workers og kan dermed blive bedere. Ved spil mod menneske vil den også lære af spillet. 

## Hvilke bilioteker mm. vil vi bruge?

- Gymnasium som api til træningen
- Numpy til bearbejdning af lister mm.
- Random til generering af tilfældige værdier. Vi bruger random til at sætte start spilleren tilfældig.
- Pickle til at gemme vores trænede AI
- Time og Math til at give ETA på træningen
- copy til at kopierer AIen så den nogle gange spiller mod sig selv.
