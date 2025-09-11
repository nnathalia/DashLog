from django.db import models
class Pacote(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    regiao = models.CharField(max_length=20, choices=[
        ("Norte", "Norte"),
        ("Nordeste", "Nordeste"),
        ("Centro-Oeste", "Centro-Oeste"),
        ("Sudeste", "Sudeste"),
        ("Sul", "Sul"),
    ])
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.codigo} ({self.regiao})"


