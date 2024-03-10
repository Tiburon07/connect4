
## Istruzioni per l'esecuzione:
1. Clona il repository: <br> 
 git clone https://github.com/tuoutro/repository.git

#####
2. Crea un ambiente virtuale: <br>
   python -m venv myenv
   ##### attivta per Linux/Mac
   source myenv/bin/activate  
   ##### attivta per Windows
   myenv\Scripts\activate <br>

#####
3. Installa le dipendenze del progetto: <br>
   pip install -r requirements.txt

## Creazione del Database con Django
1. Assicurati di trovarti nella directory del progetto Django dove si trova il file manage.py.

2. Per creare le tabelle nel database, esegui il seguente comando:
   python manage.py migrate

#####
4.  Avvia il server locale: <br>
   python manage.py runserver

5. Vai al browser e accedi all'documentazione all'indirizzo:
   http://127.0.0.1:8000/


### Rotte Disponibili

1. **Partite**
    - **Descrizione**: Questa route gestisce le operazioni relative alle partite.
    - **Metodi consentiti**: GET per elencare le partite esistenti, POST per creare una nuova partita.
    - **Endpoint**: /partite/

2. **Mosse**
    - **Descrizione**: Questa route gestisce l'aggiunta di nuove mosse.
    - **Metodi consentiti**: POST per creare una nuova mossa.
    - **Endpoint**: /mosse/

3. **Giocatori**
    - **Descrizione**: Questa route gestisce le operazioni relative ai giocatori.
    - **Metodi consentiti**: GET per elencare i giocatori esistenti, POST per creare un nuovo giocatore.
    - **Endpoint**: /giocatori/

4. **Tabellone**
    - **Descrizione**: Questo endpoint restituisce il tabellone di una specifica partita.
    - **Metodi consentiti**: GET per visualizzare il tabellone della partita.
    - **Parametri**: id_partita (identificativo della partita).
    - **Endpoint**: /tabellone/<id_partita>/
