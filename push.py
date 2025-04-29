import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Coloque o token do seu bot aqui
TELEGRAM_TOKEN = '7664162459:AAH4Edm5i9Ju8htfmHgVhxcV2C94J4mNcJg'
EXATO_TOKEN = '268753a9b3a24819ae0f02159dee6724'

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

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('cpf', cpf))

    app.run_polling()
