from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import GameState
import random

def game_start(request):
    game = GameState.objects.create()
    return redirect('game_view', game_id=game.id)

def game_view(request, game_id):
    game = get_object_or_404(GameState, id=game_id)
    return render(request, 'game/game.html', {'game': game})

def start_round(request, game_id):
    game = get_object_or_404(GameState, id=game_id)
    try:
        bet = int(request.GET.get('bet', 50))
        if bet < 10 or bet > game.balance:
            return JsonResponse({"status": "error", "message": "Мало денег!"})
        game.bet = bet
    except:
        return JsonResponse({"status": "error", "message": "Ошибка ставки"})

    game.balance -= game.bet
    game.round_active = True
    game.revealed_count = 0
    game.current_multiplier = 1.0
    all_cells = [f"{r},{c}" for r in range(5) for c in range(5)]
    random.shuffle(all_cells)
    game.bomb_positions = ";".join(all_cells[:5])
    game.save()
    return JsonResponse({"status": "success", "balance": game.balance})

def reveal_cell(request, game_id, row, col):
    game = get_object_or_404(GameState, id=game_id)
    if not game.round_active: return JsonResponse({"status": "error"})
    
    bombs = game.bomb_positions.split(';')
    if f"{row},{col}" in bombs:
        game.round_active = False
        res, msg = "bomb", "БАБАХ!"
    else:
        game.revealed_count += 1
        game.current_multiplier += 0.5
        res, msg = "treasure", "Золото!"
    
    game.save()
    return JsonResponse({"status": "success", "result": res, "multiplier": game.current_multiplier, "active": game.round_active, "message": msg})

def cash_out(request, game_id):
    game = get_object_or_404(GameState, id=game_id)
    if not game.round_active: return JsonResponse({"status": "error"})
    win = int(game.bet * game.current_multiplier)
    game.balance += win
    game.round_active = False
    game.save()
    return JsonResponse({"status": "success", "balance": game.balance, "win": win})

def reset_game(request, game_id):
    game = get_object_or_404(GameState, id=game_id)
    game.balance, game.round_active = 2000, False
    game.save()
    return JsonResponse({"status": "success", "balance": 2000})