import os
import json
from datetime import datetime, timedelta
import requests

def enviar_telegram(mensagem):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Erro: Variáveis de ambiente do Telegram não configuradas.")
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar: {response.text}")

def executar():
    # O GitHub Actions roda em UTC. Ajustamos para o horário de Brasília (UTC-3)
    hora_atual = datetime.utcnow()
    hora_brasilia = hora_atual - timedelta(hours=3)
    horario_formatado = hora_brasilia.strftime("%H:%M")
    
    print(f"Horário atual de Brasília: {horario_formatado}")
    
    if not os.path.exists("alimentos.json"):
        print("Erro: Arquivo alimentos.json não encontrado.")
        return
        
    with open("alimentos.json", "r", encoding="utf-8") as f:
        dieta = json.load(f)
        
    refeicao = dieta.get(horario_formatado)
    
    if refeicao:
        enviar_telegram(refeicao)
    else:
        print(f"Nenhuma refeição cadastrada para o horário: {horario_formatado}")

if __name__ == "__main__":
    executar()
