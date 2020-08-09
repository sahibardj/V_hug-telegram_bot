import logging
#flask will help us create a webhook / server to run our program infinitely and telegram server will make request
from flask import Flask , request
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters, Dispatcher
from telegram import Bot,Update,ReplyKeyboardMarkup
from addon import get_reply,topics_keyboard
#message handler to recive message and filters to filter out type of message recived
#enable logging
#reference python telegram bot documentation

dict={'Menstrual_Cup':" Women need effective, safe, and affordable menstrual products. The menstrual cup is a less known alternative. It’s a small, flexible funnel-shaped cup made of rubber or silicone that you insert into your vagina to collect period fluid." +
"\n"+ "A menstrual cup can hold blood for about 5-12hours depending on your flow and size of cup u are using.The small, flexible cup is made of silicone or latex rubber. Instead of absorbing your flow, like a tampon or pad, it catches and collects it. They usually are in shape of a bell and a stem, bell creates vacuum and stem is useful for providing grip while removal."+"\n"+
"visit: https://sahibardj.github.io/V-Hug/mec.html" , 
'Biodegradable_pads': "Biodegradable pads are an effort to reduce ever increasing waste generation by human kind.The biggest benefit of anything biodegradable is that we can compost it in our backyard, otherwise, it has to be sent to landfills (involving waste management workers, systems and elaborate processes). Most of these ‘biodegradable’ pads claim to be chemical-free and compostable."+
 "\n"+ 
 "visit: https://sahibardj.github.io/V-Hug/biop.html",
    'Regular_pads':"Regular Pads are widely accepted as they are comfortable to use. Women find ease in managing their menstrual cycle with them. They can be safely used for 6-7 hours. They may have cotton top or plastic porous top, they hold blood by absorbing it. Available in various sizes, we can choose one on the basis of menstrual flow." +
    "\n" + "visit: https://sahibardj.github.io/V-Hug/pdn.html" , 
    'Reusable_pads':"Reusable pads are usually made up of several layers of cotton or hemp. They are the same as regular pads minus the plastic. They are eco and budget friendly replacement for regular pads. One pad can be used several times and can be disposed of easily when worn out. These pads can be safely used for about 5-6 hours depending on flow. After each use they need to be washed clean and should be left with no stain to avoid any form of infection.Most pad come with thin lining preventing them from staining" 
    +"\n" 
    +"visit:https://sahibardj.github.io/V-Hug/rp.html  " ,
    'Tampons': "Tampon is a feminine hygiene product used to absorb menstrual flow, Made of soft cotton. They are cylindrical in shape with a thread attached to flat bottom, they are hemispherical on top for easy insertion. They are similar to pads in terms of functionality a.k.a they to absorb blood.They come in different absorbances and different sizes.Once it has absorbed the blood you can pull it out with the string attached to the product or if the string breaks, you can reach in and pull the tampon out using your fingers."+ 
    "\n"+"visit: https://sahibardj.github.io/V-Hug/tp.html" ,
     'Period_pants':"A period panty is specially designed to provide women with leak-proof, odourless comfort.Period panty is innovation in regular products used during menstrual cycle. It is designed in a manner that no odour is observed and it is made leak proof. Unlike earlier versions the new ones are no longer bulky and uncomfortable ‘grandma underwear’. They are sleek, fit snugly and are not unwieldy in any way."+ 
     "\n"+ "visit: https://sahibardj.github.io/V-Hug/bp.html " ,
     'about': "V-Hug is an initiative dealing with women health and hygine.It creates awareness among women about menstrual health and all options at hand apart from regular sanitary pads. It enlightens on how to use them, their Pros/Cons and how to maintain hygiene with all the listed alternatives. "+
     "\n"+"visit : https://sahibardj.github.io/V-Hug/ "
	
}

logging.basicConfig(format='%(asctime)s - %(name)%s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


TOKEN="1245399665:AAFbc5ySlMhsVjsuPTlvIHIihjwmiPWAhX8"

#creating a flask app object
app= Flask(__name__)


@app.route(f'/{TOKEN}', methods=['GET','POST'])
def webhook():
	#creating an object from json-format request data
	update=Update.de_json(request.get_json(),bot)
	#process update (handing the updates)
	dp.process_update(update)
	return "ok"
	




#start will be the conversation starter
def start(bot,update):
	#to get name of author (the person who is using the bot)
	author=update.message.from_user.first_name
	#generating the reply user will recieve
	reply= "Hey!    {}".format(author) +"\n"+"Type About to know more on Vhug"+"\n"+" Type '\info' command to get more information" +"\n"+"Visit web to know more: https://sahibardj.github.io/V-Hug/"
	#to send text to the user ud need chat id and it will be sent via bot argument
	bot.send_message(chat_id=update.message.chat_id,text=reply)

def help_(bot, update):
	reply= "How may I you?"
	bot.send_message(chat_id=update.message.chat_id,text=reply)
def error(bot, update):
	#log the error using logger
	logger.error("Update'%s' caused error '%s' ",update,update.error)



def echo_sticker(bot, update):
    """callback function for sticker message handler"""
    bot.send_sticker(chat_id=update.message.chat_id,
                     sticker=update.message.sticker.file_id)




def reply_text(bot, update):
    """callback function for text message handler"""
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if update.message.text in dict:
    	bot.send_message(chat_id=update.message.chat_id, text=dict[update.message.text])
    else:
    	bot.send_message(chat_id=update.message.chat_id, text=reply)

    
def info(bot, update):
    """callback function for /news handler"""
    bot.send_message(chat_id=update.message.chat_id, text="Choose a category",
                     reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


#creating a bot object
# recives update from telegram sever
bot =Bot(TOKEN)
try:
    bot.set_webhook("https://vhugg.herokuapp.com/" + TOKEN)
    time.sleep(5)
except Exception as e:
    print(e)

#dispatcher handels responses to what input is provided on updater.
dp=Dispatcher(bot,None)
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",help_))
dp.add_handler(CommandHandler("info",info))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_error_handler(error)
if __name__ == "__main__":
	app.run(port=8443)
	

