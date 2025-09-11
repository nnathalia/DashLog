import random
from django.http import JsonResponse
from django.shortcuts import render
import requests
from .models import Pacote


def index(request):
    return render(request, 'index.html')


def get_pacote(request):
    try:
        # Chama API com timeout
        resp = requests.get("http://127.0.0.1:8000/fake-api/", timeout=5)
        resp.raise_for_status()  # levanta erro se não for 200 OK
        print(resp)
        dados = resp.json()
        codigo = dados.get("codigo")
        nome = dados.get("nome")
        regiao = dados.get("regiao")

        if codigo and nome and regiao:
            regiao = regiao.lower()  # normaliza

            # Evita duplicados (usa get_or_create)
            pacote, created = Pacote.objects.get_or_create(
                codigo=codigo,
                defaults={
                    "nome": nome,
                    "regiao": regiao
                }
            )

            return JsonResponse({
                "codigo": pacote.codigo,
                "nome": pacote.nome,
                "regiao": pacote.regiao,
                "criado_em": pacote.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
                "novo": created  # True se foi salvo agora, False se já existia
            })

        return JsonResponse({"codigo": None})

    except requests.exceptions.RequestException as e:
        # Erros de rede / HTTP
        print("Erro de requisição API:", e)
        return JsonResponse({"codigo": None})

    except Exception as e:
        # Outros erros
        print("Erro inesperado:", e)
        return JsonResponse({"codigo": None})


def fake_api_externa(request):
    codigos = ["ABC123", "XYZ456", "LMN789"]
    nomes = ["João", "Maria", "Carlos"]
    regioes = ["norte", "sul", "sudeste"]

    pacote = {
        "codigo": random.choice(codigos) + str(random.randint(100, 999)),
        "nome": random.choice(nomes),
        "regiao": random.choice(regioes)
    }

    return JsonResponse(pacote)