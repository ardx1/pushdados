import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
EXATO_TOKEN = '268753a9b3a24819ae0f02159dee6724'

# Função para o comando /cpf
async def cpf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Por favor, envie o CPF. Exemplo: /cpf 18845258653')
        return

    cpf_input = context.args[0]
    
    url = f"https://api.exato.digital/br/exato/cadastro/pessoa-fisica?token={EXATO_TOKEN}&cpf={cpf_input}&relacionados=true&get_rf_information_when_contact_not_found=true&format=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Formata o JSON de forma mais bonita
        import json
        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)

        await update.message.reply_text(f"🔎 Resultado para CPF {cpf_input}:\n\n{formatted_data[:4000]}")
    
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"❌ Erro ao buscar CPF: {e}")

# Função para o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bem-vindo ao Bot de Consulta!\n\n"
        "Comandos disponíveis:\n"
        "/cpf <número> - Consultar informações de um CPF.\n"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))   # <-- adicionamos aqui
    app.add_handler(CommandHandler('cpf', cpf))

    app.run_polling()
