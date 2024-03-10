from django.contrib import admin

from .models import Giocatore, Partita, Mossa


class PartitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'stato', 'giocatore1', 'giocatore2', 'vincitore')
    list_filter = ('stato',)
    search_fields = ('giocatore1__nome', 'giocatore2__nome', 'vincitore__nome')
    exclude = ('vincitore',)


class MossaAdmin(admin.ModelAdmin):
    list_display = ('partita', 'colonna', 'riga', 'giocatore', 'timestamp')
    list_filter = ('partita', 'giocatore')
    search_fields = ('partita__id', 'giocatore__nome')
    exclude = ('riga',)


admin.site.register(Giocatore)
admin.site.register(Partita, PartitaAdmin)
admin.site.register(Mossa, MossaAdmin)
