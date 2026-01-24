from django.db import models

# Create your models here.
class Transacao(models.Model):
    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.descricao} - R${self.valor} na {self.data}"
    
    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ['-data']