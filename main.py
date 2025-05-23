import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# ========== CONFIGURAÇÕES ==========
TOKEN = '7484306900:AAFHjJZJJdfqTp3QW7b6rhkAl8KoHtsKyCU'
CREDENCIAL = 'sae153sae'
PLANILHA = 'PESQUISAS POLICIAIS APP'
ABA = 'VEICULOS SUSPEITOS'

# Caminho para o JSON (no mesmo diretório no Render)
JSON_PATH = 'credenciais.json'

# ========== AUTENTICAÇÃO GOOGLE SHEETS ==========
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_PATH, scope)
client = gspread.authorize(creds)
sheet = client.open(PLANILHA).worksheet(ABA)

# ========== ESTADOS ==========
LOGIN, MENU = range(2)
usuarios_autenticados = set()

def start(update, context):
    update.message.reply_text("Olá! Insira a credencial:")
    return LOGIN

def verificar_credencial(update, context):
    if update.message.text.strip() == CREDENCIAL:
        user_id = update.message.from_user.id
        usuarios_autenticados.add(user_id)
        update.message.reply_text(
            "✅ Acesso autorizado!\n\nEscolha uma opção:\n1 - Cadastrar veículo\n2 - Consultar veículo"
        )
        return MENU
    else:
        update.message.reply_text("❌ Credencial incorreta. Tente novamente:")
        return LOGIN

def menu(update, context):
    user_id = update.message.from_user.id
    if user_id not in usuarios_autenticados:
        update.message.reply_text("Acesso negado. Envie /start para começar novamente.")
        return ConversationHandler.END

    escolha = update.message.text.strip()
    if escolha == '1':
        update.message.reply_text("Função de cadastro em desenvolvimento.")
    elif escolha == '2':
        update.message.reply_text("Função de consulta em desenvolvimento.")
    else:
        update.message.reply_text("Opção inválida. Digite 1 ou 2.")
    return MENU

def cancelar(update, context):
    update.message.reply_text("Sessão encerrada. Envie /start para recomeçar.")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOGIN: [MessageHandler(Filters.text & ~Filters.command, verificar_credencial)],
            MENU: [MessageHandler(Filters.text & ~Filters.command, menu)],
        },
        fallbacks=[CommandHandler('cancelar', cancelar)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
