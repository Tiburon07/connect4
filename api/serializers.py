from rest_framework import serializers
from rest_framework.response import Response
from connect4.models import Giocatore, Partita, Mossa


class GiocatoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Giocatore
        exclude = ["id"]


class PartitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partita
        exclude = []
        read_only_fields = ['vincitore', 'stato']


def controllo_vittoria(partita, giocatore):
    # Recupero tutte le mosse della partita in corso
    mosse = list(partita.mosse.all().order_by('riga', 'colonna'))

    # Converto le mosse in una matrice 6x7 per un facile accesso
    griglia = [[None for _ in range(8)] for _ in range(6)]
    for mossa in mosse:
        # Assegna il giocatore corrispondente in base alla mossa nella griglia
        griglia[mossa.riga][mossa.colonna] = mossa.giocatore

    # Controlla ogni direzione per una vittoria
    altezza = len(griglia)
    larghezza = len(griglia[0])

    # Controllo orizzontale -
    for riga in range(altezza):
        for colonna in range(larghezza - 3):
            if (griglia[riga][colonna] == giocatore
                    and griglia[riga][colonna + 1] == giocatore
                    and griglia[riga][colonna + 2] == giocatore
                    and griglia[riga][colonna + 3] == giocatore):
                return True

    # Controllo verticale |
    for riga in range(altezza - 3):
        for colonna in range(larghezza):
            if (griglia[riga][colonna] == giocatore
                    and griglia[riga + 1][colonna] == giocatore
                    and griglia[riga + 2][colonna] == giocatore
                    and griglia[riga + 3][colonna] == giocatore):
                return True

    # Controllo diagonale \
    for riga in range(altezza - 3):
        for colonna in range(larghezza - 3):
            if (griglia[riga][colonna] == giocatore
                    and griglia[riga + 1][colonna + 1] == giocatore
                    and griglia[riga + 2][colonna + 2] == giocatore
                    and griglia[riga + 3][colonna + 3] == giocatore):
                return True

    # Controllo diagonale /
    for riga in range(3, altezza):
        for colonna in range(larghezza - 3):
            if (griglia[riga][colonna] == giocatore
                    and griglia[riga - 1][colonna + 1] == giocatore
                    and griglia[riga - 2][colonna + 2] == giocatore
                    and griglia[riga - 3][colonna + 3] == giocatore):
                return True

    return False


class MossaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mossa
        fields = ['id', 'partita', 'colonna', 'riga', 'giocatore', 'timestamp']
        read_only_fields = ['riga', 'timestamp']

    def create(self, validated_data):
        # Recupera i dati validati dal serializer
        giocatore = validated_data.get('giocatore')
        partita = validated_data.get('partita')
        colonna = validated_data.get('colonna')

        # Controllo se la partita è in corso
        if partita.stato != 'I':
            raise serializers.ValidationError("La partita è conclusa.")

        # Controlla se il giocatore è uno dei giocatori della partita
        if giocatore != partita.giocatore1 and giocatore != partita.giocatore2:
            raise serializers.ValidationError("Il giocatore non fa parte di questa partita.")

        # Controllo il turno del giocatore
        if partita.mosse.exists():
            ultima_mossa = partita.mosse.order_by('-timestamp')[0]
            if ultima_mossa and giocatore == ultima_mossa.giocatore:
                turno_di = partita.giocatore2 if giocatore == partita.giocatore1 else partita.giocatore1
                raise serializers.ValidationError("È il turno del giocatore. " + turno_di.nome)

        # Controllo se la colonna selezionata è piena
        mosse_nella_colonna = Mossa.objects.filter(partita=partita, colonna=colonna)

        if mosse_nella_colonna.count() >= 6:  # Supponendo che il tabellone sia 6x7
            raise serializers.ValidationError("Questa colonna è piena.")

        # Calcola la riga disponibile più bassa
        riga = 5 - mosse_nella_colonna.count()

        # Crea l'oggetto Mossa con i dati personalizzati
        mossa = Mossa.objects.create(riga=riga, colonna=colonna, partita=partita, giocatore=giocatore)
        mossa.save()

        if controllo_vittoria(partita, giocatore):
            partita.vincitore = giocatore
            partita.stato = 'F'  # Aggiorna lo stato della partita a 'Finita'
            partita.save()

        return mossa
