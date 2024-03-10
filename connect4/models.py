# models.py
from django.db import models


class Giocatore(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Partita(models.Model):
    STATI_PARTITA = (
        ('I', 'In corso'),
        ('F', 'Finita'),
    )
    stato = models.CharField(max_length=1, choices=STATI_PARTITA, default='I')
    giocatore1 = models.ForeignKey(Giocatore, related_name='giocatore1', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    giocatore2 = models.ForeignKey(Giocatore, related_name='giocatore2', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    vincitore = models.ForeignKey(Giocatore, related_name='partite_vinte', on_delete=models.SET_NULL, null=True,
                                  blank=True)

    def __str__(self):
        return f"Partita {self.id} - Stato: {self.stato}"


class Mossa(models.Model):
    COLONNE_SCELTE = [(i, i) for i in range(1, 8)]  # Genera scelte da 1 a 7
    partita = models.ForeignKey(Partita, related_name='mosse', on_delete=models.CASCADE)
    colonna = models.IntegerField(choices=COLONNE_SCELTE)
    riga = models.IntegerField(blank=True, null=True)
    giocatore = models.ForeignKey(Giocatore, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mossa di {self.giocatore.nome} in colonna {self.colonna}, riga {self.riga}"
