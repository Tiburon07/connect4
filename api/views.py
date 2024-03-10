from rest_framework import viewsets, generics
from api.serializers import PartitaSerializer, GiocatoreSerializer, MossaSerializer
from connect4.models import Partita, Giocatore, Mossa
from rest_framework.response import Response


class PartitaViewSet(viewsets.ModelViewSet):
    queryset = Partita.objects.all().order_by('-id')
    serializer_class = PartitaSerializer


class GiocatoreViewSet(viewsets.ModelViewSet):
    queryset = Giocatore.objects.all().order_by('-id')
    serializer_class = GiocatoreSerializer


class MossaViewSet(viewsets.ModelViewSet):
    queryset = Mossa.objects.all().order_by('-id')
    serializer_class = MossaSerializer


class PartitaListAPIView(generics.ListAPIView):
    serializer_class = MossaSerializer

    def get_queryset(self):
        """
        Sovrascrive il metodo predefinito per restituire un queryset filtrato per id della partita.
        """
        partita_id = self.kwargs['id_partita']

        return Mossa.objects.filter(partita__id=partita_id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        tabellone = [[' ' for _ in range(7)] for _ in range(6)]  # Crea un tabellone vuoto
        nome_giocatore2 = ""
        nome_giocatore1 = ""
        nome_vincitore = ""
        if queryset.exists():
            partita = Partita.objects.get(id=queryset.first().partita.id)
            nome_giocatore1 = partita.giocatore1.nome
            nome_giocatore2 = partita.giocatore2.nome
            nome_vincitore = partita.vincitore.nome
            for mossa in queryset:
                if mossa.riga is not None and mossa.colonna is not None:
                    tabellone[mossa.riga][mossa.colonna - 1] = 'X' if mossa.giocatore.nome == nome_giocatore1 else 'O'

        # Converti il tabellone in ASCII
        tabellone_ascii = "\n".join(["|" + "|".join(riga) + "|" for riga in tabellone])

        tabellone_json = []
        for riga in tabellone:
            tabellone_json.append(' | '.join(riga))

        response = {
            nome_giocatore1: 'x',
            nome_giocatore2: 'O',
            'vincitore': nome_vincitore,
            'tabellone': tabellone_json
        }

        return Response(response)
        # return Response(tabellone_ascii)

