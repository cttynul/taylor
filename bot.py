# -*- coding: utf-8 -*-
import logging, json, addons, chatbot, random, philips_hue
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

#################################################
#              basic global var                 #
#################################################
with open("config.json") as f:
    data = json.loads(f.read())
    token = data["token"]
    user = data["user"]
    hue_ip = data["phue"]

hue_bridge = philips_hue.initialize_bridge(hue_ip)
hue_bridge.connect()

##################################################
#                     logging                    #
##################################################
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#logger = logging.getLogger(__name__)
##################################################
#                   end logging                  #
##################################################

##################################################
#                support functions               #
##################################################
with open("config.json") as f:
    data = json.loads(f.read())
    USERID = data["userid"]

def enabled(user_id, admin_ids=USERID):
    if user_id not in admin_ids: return False

def error_message():
    answeres = ["Non sei il mio padrone vai via!", "Non sei il mio creatore sparisci!", "Puoi anche scrivermi non ti risponderò mai con alcuna frase di senso compiuto", "Get out, ti mangio gnam!", "Non sono il tuo bot, perciò ti sto per inviare un virus per il tuo smartphone", "Non sono il tuo bot, come mi hai trovato? Per punizione la tua curiosità verrà salvata per sempre sui miei log e chi sei segnalato al mio sviluppatore"]
    return random.choice(answeres)

##################################################
#              end support functions             #
##################################################

##################################################
#                conversation                    #
##################################################
'''
Define a few command handlers. These usually take the two arguments update and
context. Error handlers also receive the raised TelegramError object in error.
'''
def start(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_video(open("./gif/error.gif", 'rb'))
        return
    response_start = "Ehilà! Sono un bot e mi chiamo Taylor, perché il mio creatore ha un feticcio per Taylor Swift, posso fare un sacco di cose, anche chiacchierare un po', se vuoi sapere cosa altro io sia in grado di fare invia pure il comando /help in chat :)."
    update.message.reply_text(response_start)

def help(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_video(open("./gif/error.gif", 'rb'))
        return
    """Send a message when the command /help is issued."""
    response_help = "Ehi, sono Taylor e so fare un sacco di cose, posso avere una semplice conversazione con te però, perdonami anticipatamente in caso ti dia risposte un po' 'così', sto ancora imparando! Però posso comunque dirti quando passi il prossimo autobus a Bologna utilizzando il comando /bus NUMEROFERMATA (NUMEROLINEA), puoi anche omettere il nome della linea!"
    update.message.reply_text(response_help)

def bus(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return

    """Send a message when the command /bus is issued."""
    user_says = " ".join(context.args)
    fermata = context.args[0]
    try: bus = context.args[1]
    except: bus = 0
    try: query_result = addons.query_hellobus(fermata, bus)
    except: query_result = "Oh oh oh! Hai inserito dei parametri non validi o, molto probabilmente, la linea che cerchi non è servita dal servizio di geolocalizzazione oppure hai inserito dei parametri a cazzo di cane.\nRicorda che il comando corretto è:\n/bus NUMEROFERMATA [NUMEROAUTOBUS]"
    update.message.reply_text(query_result)
    #update.message.reply_text('Help!')

def book(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_video(open("./gif/error.gif", 'rb'))
        update.message.reply_text(error_message())
        return

    user_says = " ".join(context.args)
    author = addons.search_author(user_says)
    if author:
        update.message.reply_text("Trovato " + user_says.title() + "! Dammi qualche minuto, ora arriva tutto ciò che hai richiesto!")
        books = addons.wrapper_retrive_books(author)
        for book in books:
            update.message.reply_document(open(book, "rb"))
        addons.clean_book_cache(books)
        update.message.reply_text('Pretendo almeno un "grazie" ora!')
    else:
        update.message.reply_text("Mi dispiace, non ho la più pallida idea di chi sia " + user_says.title() +"! Sicuro tu lo abbia scritto correttamente?")

def answer(update, context):
    # Block if it's not me
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_video(open("./gif/error.gif", 'rb'))
        update.message.reply_text(error_message())
        return

    user_says = str(update.message.text)
    if "meme" in user_says.lower():
        # Meme feature
        random_meme = addons.get_random_meme()
        update.message.reply_photo(open(random_meme, 'rb'))
    elif "gif" in user_says.lower():
        random_gif = addons.get_random_gif()
        update.message.reply_video(open(random_gif, 'rb'))
    elif user_says.lower() == "cantami una canzone" or user_says.lower() == "mi canti una canzone?" or "cantarmi una canzone" in user_says.lower():
        # Song feature
        random_song = addons.get_random_song()
        update.message.reply_voice(open(random_song, 'rb'))
    elif "un altro film" in user_says.lower() or "consigliami un film" in user_says.lower() or "mi consigli un film" in user_says.lower() or "un film da guardare" in user_says.lower():
        # Movie suggest
        update.message.reply_text(addons.get_random_movie())
    elif "spegni le luci" in user_says.lower():
        # Philips Hue off
        philips_hue.turn_lights(bridge=hue_bridge, mode=False, light=2)
        update.message.reply_text("Ho appena spento tutte le luci caro.")
    elif "accendi le luci" in user_says.lower():
        # Philips Hue on
        philips_hue.turn_lights(bridge=hue_bridge, mode=True, light=2)
        update.message.reply_text("Ho acceso tutte le luci come volevi.")
    else:
        response = chatbot.taylorchatbot.get_response(user_says)
        update.message.reply_text(str(response).capitalize())

##################################################
#                end conversation                #
##################################################


##################################################
#                   bot core                     #
##################################################
def error(update, context):
    '''Log Errors caused by Updates.'''
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def setup():
    with open("config.json") as f:
        data = json.loads(f.read())
        TOKEN = data["token"]
        USER = data["user"]
        HUE = data["phue"]
    return TOKEN, USER, HUE

def train():
    '''
    with open("chat.txt") as f:
        conversation = f.readlines()
        trainer = ListTrainer(chatbot.taylorchatbot)
        trainer.train(conversation)
    '''
    instance = chatbot.taylorchatbot
    trainer = ChatterBotCorpusTrainer(instance)
    trainer.train(
        "./corpus/ai.yml",
        "./corpus/botprofile.yml",
        "./corpus/computers.yml",
        "./corpus/conversations.yml",
        "./corpus/emotion.yml",
        "./corpus/food.yml",
        "./corpus/gossip.yml",
        "./corpus/greetings.yml",
        "./corpus/health.yml",
        "./corpus/history.yml",
        "./corpus/humor.yml",
        "./corpus/literature.yml",
        "./corpus/money.yml",
        "./corpus/politics.yml",
        "./corpus/psychology.yml",
        "./corpus/science.yml",
        "./corpus/sports.yml",
        "./corpus/trivia.yml"
    )
    #trainer.train('chatterbot.corpus.italian')

def main():
    train()
    
    '''Start the bot.
    Create the Updater and pass it your bot's token.
    Make sure to set use_context=True to use the new context based callbacks
    Post version 12 this will no longer be necessary
    '''
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, Filters.user(username="kridyltneg")))
    dp.add_handler(CommandHandler("bus", bus, Filters.user(username="kridyltneg")))
    dp.add_handler(CommandHandler("help", help, Filters.user(username="kridyltneg")))
    dp.add_handler(CommandHandler("book", book, Filters.user(username="kridyltneg")))

    # on noncommand i.e message - answer the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, answer, Filters.user(username="kridyltneg")))

    # log all errors
    #dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

##################################################
#                 end bot core                   #
##################################################


if __name__ == '__main__':
    main()