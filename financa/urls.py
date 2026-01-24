from django.urls import path
from .views import financas, adicionar_transacao ,detalhes_transacao, editar_transacao, deletar_transacao

urlpatterns = [
    path('', financas, name='financas'),
    path('adicionar/', adicionar_transacao, name='adicionar_transacao'),
    path('detalhes/<int:transacao_id>/', detalhes_transacao, name='detalhes_transacao'),
    path('editar/<int:transacao_id>/', editar_transacao, name='editar_transacao'),
    path('deletar/<int:transacao_id>/', deletar_transacao, name='deletar_transacao'),
]
