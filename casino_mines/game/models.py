from django.db import models

class GameState(models.Model):
    balance = models.IntegerField(default=2000)
    bet = models.IntegerField(default=50)
    round_active = models.BooleanField(default=False)
    revealed_count = models.IntegerField(default=0)
    current_multiplier = models.FloatField(default=1.0)
    # Позиции бомб храним как "0,1;2,3"
    bomb_positions = models.TextField(default="")
    last_result_msg = models.CharField(max_length=100, default="Welcome!")

    def __str__(self):
        return f"ID: {self.id} | Balance: {self.balance}"