class Connect4():
    """
    Definisce il costruttore della classe con valori predefiniti per colonne (cols), righe (rows)
    """

    def __init__(self, cols=7, rows=6):
        self.cols = cols
        self.rows = rows
        # Creo una griglia di gioco vuota dove '.' rappresenta le celle vuote.
        self.matrice = [['.' for _ in range(rows)] for __ in range(cols)]
        # Usa 1 per il giocatore 1 e 2 per il giocatore 2
        self.turno = 1
        self.game_over = False

    def insert(self, col):
        """
        Inserimento del gettone
        """
        if self.game_over:
            # Controlla se il gioco è finito; in tal caso, non permette ulteriori mosse
            return "Game has finished!"

        if self.matrice[col][0] != '.':
            # Verifica se la colonna scelta è piena.
            return "Column full!"

        for row in reversed(range(self.rows)):
            # Trova la prima cella vuota nella colonna scelta dall'alto verso il basso e inserisce
            # il gettone del giocatore corrente
            if self.matrice[col][row] == '.':
                self.matrice[col][row] = 'R' if self.turno == 1 else 'Y'
                break

        if self.controllo_vincitore(col, row):
            # Dopo l'inserimento, controlla se il giocatore corrente ha vinto.
            # Se sì, termina il gioco e ritorna il messaggio di vittoria.
            self.game_over = True
            return f"Player {self.turno} wins!"

        # Prepara il messaggio di turno per il giocatore corrente,
        turn_message = f"Player {self.turno} has a turn"
        # cambia il turno e poi ritorna il messaggio preparato.
        self.turno = 1 if self.turno == 2 else 2
        return turn_message

    def controllo_vincitore(self, col, row):
        print(col, row)
        self.print_board()
        # Definisci le direzioni in cui controllare i gettoni consecutivi.
        directions = [(0, 1),  # verticale
                      (1, 0),  # orizzontale
                      (1, 1),  # diagonale ascendente
                      (1, -1)]  # diagonale discendente

        # Ottieni il simbolo del giocatore corrente.
        gettone = 'R' if self.turno == 1 else 'Y'

        for dx, dy in directions:
            count = 1  # Conta il gettone appena inserito.

            # Controlla i gettoni consecutivi in entrambe le direzioni lungo la linea.
            for dir in [1, -1]:

                step = 1
                while True:
                    # Calcola le nuove coordinate basandosi sulla direzione e il passo.
                    x, y = col + step * dx * dir, row + step * dy * dir
                    # Verifica se le coordinate sono dentro la griglia.
                    if 0 <= x < self.cols and 0 <= y < self.rows:
                        # Controlla se il gettone nella posizione calcolata corrisponde a quello del giocatore corrente.
                        if self.matrice[x][y] == gettone:
                            count += 1  # Incrementa il conteggio se corrisponde.
                            # Se il conteggio raggiunge 4, il giocatore ha vinto.
                            if count == 4:
                                return True
                        else:
                            break  # Interrompi il ciclo se il gettone non corrisponde.
                    else:
                        break  # Interrompi il ciclo se la posizione è fuori dalla griglia.
                    step += 1  # Passa al prossimo gettone lungo la direzione.

        return False  # Nessun vincitore trovato dopo aver controllato tutte le direzioni.

    def play(self, col):
        if col < 0 or col >= self.cols:
            return "Invalid column"
        return self.insert(col)

    def print_board(self):
        """
        Stampa lo stato attuale della griglia di gioco, riga per riga
        """
        for row in range(self.rows):
            print(' '.join(self.matrice[col][row] for col in range(self.cols)))
        print()


