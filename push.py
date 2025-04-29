import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Lendo o token do bot do Telegram a partir de uma variável de ambiente
TELEGRAM_TOKEN = os.getenv("7664162459:AAH4Edm5i9Ju8htfmHgVhxcV2C94J4mNcJg")
EXATO_TOKEN = os.getenv("268753a9b3a24819ae0f02159dee6724")

# Verificando se o token foi lido corretamente
if not TELEGRAM_TOKEN:
    raise ValueError("O token do Telegram não foi configurado corretamente!")

if not EXATO_TOKEN:
    raise ValueError("O token da API Exato não foi configurado corretamente!")

# Imprimindo o token para garantir que ele está sendo lido corretamente (com cuidado, não imprima em produção)
print(f"Token do Telegram lido corretamente: {TELEGRAM_TOKEN[:5]}...")  # Exibindo apenas os primeiros 5 caracteres para segurança

# Função para o comando /cpf
async def cpf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Por favor, envie o CPF. Exemplo: /cpf 18845258653')
        return

    cpf_input = context.args[0]

    # URL da API Exato
    url = f"https://api.exato.digital/br/exato/cadastro/pessoa-fisica?token={EXATO_TOKEN}&cpf={cpf_input}&relacionados=true&get_rf_information_when_contact_not_found=true&format=json"
    
    try:
        # Fazendo a requisição à API usando requests
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Verifica se o status da resposta é 200
        data = response.json()  # Obtém os dados em formato JSON

        # Formata o JSON de forma mais legível
        import json
        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)

        # Envia a resposta de volta no Telegram (limitando a resposta a 4000 caracteres)
        await update.message.reply_text(f"🔎 Resultado para CPF {cpf_input}:\n\n{formatted_data[:4000]}")  # Limita a resposta a 4000 caracteres
    
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"❌ Erro ao buscar CPF: {e}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao buscar CPF: {str(e)}")

# Função para o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bem-vindo ao Bot de Consulta!\n\n"
        "Comandos disponíveis:\n"
        "/cpf <número> - Consultar informações de um CPF.\n"
    )

# Configuração do bot
if __name__ == '__main__':
    # Verificando o token
    print(f"Usando o token: {TELEGRAM_TOKEN[:5]}...")  # Imprimindo os primeiros 5 caracteres do token para debug

    # Criando a aplicação do bot com o token lido das variáveis de ambiente
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Adicionando os handlers para os comandos
    app.add_handler(CommandHandler('start', start))  # Comando /start
    app.add_handler(CommandHandler('cpf', cpf))  # Comando /cpf

    # Inicia o bot para começar a ouvir os comandos
    app.run_polling()  # Inicia o bot com polling
