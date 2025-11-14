from datetime import timezone
import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Pacote
from django.views.decorators.csrf import csrf_exempt

# Página inicial
def index(request):
    return render(request, 'index.html')

# Rota para o Arduino enviar pacotes
@csrf_exempt
def receber_pacote_arduino(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body.decode('utf-8'))

            codigo = dados.get("codigo")
            nome = dados.get("nome")
            regiao = dados.get("regiao")
            
            if not codigo or not nome or not regiao:
                return JsonResponse({"erro": "Campos obrigatórios ausentes."}, status=400)

            regiao = regiao.lower().strip()

            pacote, created = Pacote.objects.get_or_create(
                codigo=codigo,
                defaults={
                    "nome": nome,
                    "regiao": regiao,
                    "criado_em": timezone.now()
                }
            )

            return JsonResponse({
                "mensagem": "Pacote recebido com sucesso.",
                "codigo": pacote.codigo,
                "nome": pacote.nome,
                "regiao": pacote.regiao,
                "criado_em": pacote.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
                "novo": created
            })

        except json.JSONDecodeError:
            return JsonResponse({"erro": "JSON inválido."}, status=400)
        except Exception as e:
            print("Erro ao processar POST do Arduino:", e)
            return JsonResponse({"erro": "Erro interno no servidor."}, status=500)
    else:
        return JsonResponse({"erro": "Método não permitido. Use POST."}, status=405)


# Rota para o frontend buscar pacotes
def listar_pacotes(request):
    if request.method == 'GET':
        try:
            pacotes = Pacote.objects.order_by('-criado_em')[:10]
            dados = [
                {
                    "codigo": p.codigo,
                    "nome": p.nome,
                    "regiao": p.regiao,
                    "criado_em": p.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
                }
                for p in pacotes
            ]
            return JsonResponse({"pacotes": dados})
        except Exception as e:
            print("Erro ao buscar pacotes:", e)
            return JsonResponse({"erro": "Erro ao buscar dados."}, status=500)
    else:
        return JsonResponse({"erro": "Método não permitido. Use GET."}, status=405)
    
def camera_view(request):
    url_camera = request.GET.get('url_camera', '')
    if not url_camera:
        print("URL da câmera não fornecida.")
    return render(request, 'index.html', {'url_camera': url_camera})
