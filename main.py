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
    # GitHub Actions roda em UTC
    hora_atual = datetime.utcnow()
    hora_brasilia = hora_atual - timedelta(hours=3)

    print(f"Horário atual de Brasília: {hora_brasilia.strftime('%H:%M')}")

    if not os.path.exists("alimentos.json"):
        print("Erro: Arquivo alimentos.json não encontrado.")
        return

    with open("alimentos.json", "r", encoding="utf-8") as f:
        dieta = json.load(f)

    # Procura uma refeição até 5 minutos antes/depois do horário atual
    for horario, refeicao in dieta.items():
        horario_refeicao = datetime.strptime(horario, "%H:%M").replace(
            year=hora_brasilia.year,
            month=hora_brasilia.month,
            day=hora_brasilia.day
        )

        diferenca = abs((hora_brasilia - horario_refeicao).total_seconds())

        if diferenca <= 300:  # 5 minutos
            print(f"Enviando refeição das {horario}")
            enviar_telegram(refeicao)
            return

    print("Nenhuma refeição cadastrada para este horário.")


if __name__ == "__main__":
    executar()
