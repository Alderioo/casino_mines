from django.urls import path
from . import views

urlpatterns = [
    path('new_game/', views.game_start, name='game_start'),
    path('game/<int:game_id>/', views.game_view, name='game_view'),
    # Пути для JS (убрали лишний /api/ чтобы не путаться)
    path('start_round/<int:game_id>/', views.start_round),
    path('reveal/<int:game_id>/<int:row>/<int:col>/', views.reveal_cell),
    path('cash_out/<int:game_id>/', views.cash_out),
    path('reset/<int:game_id>/', views.reset_game),
]