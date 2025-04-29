import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("7664162459:AAH4Edm5i9Ju8htfmHgVhxcV2C94J4mNcJg")

async def cpf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Por favor, envie o CPF. Exemplo: /cpf 18845258653')
        return

    cpf_input = context.args[0]
    
    # Comando CURL em bash
    url = "https://api.exato.digital/br/exato/cadastro/pessoa-fisica?lightweight=true"
    data = f"cpf={cpf_input}&relacionados=true&get_rf_information_when_contact_not_found=true"
    
    # Executando o comando curl via subprocess
    try:
        result = subprocess.run(
            ['curl', '-X', 'POST', url, 
             '-H', 'accept: application/json',
             '-H', 'Content-Type: application/x-www-form-urlencoded',
             '-d', data], 
            capture_output=True, text=True
        )

        if result.returncode != 0:
            raise Exception(f"Erro ao executar curl: {result.stderr}")

        # A resposta será em formato JSON, então podemos formatá-la
        response_data = result.stdout
        formatted_data = response_data[:4000]  # Limitando a resposta a 4000 caracteres

        await update.message.reply_text(f"🔎 Resultado para CPF {cpf_input}:\n\n{formatted_data}")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao buscar CPF: {str(e)}")

# Função para o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bem-vindo ao Bot de Consulta!\n\n"
        "Comandos disponíveis:\n"
        "/cpf <número> - Consultar informações de um CPF.\n"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('cpf', cpf))

    app.run_polling()
