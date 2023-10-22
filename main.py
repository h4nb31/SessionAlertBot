#This bot for testing some features
import logging
import conf
import datetime
import time
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import pytz

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #now = time.strftime("%H:%M:%S")
    try:
        print (await context.bot.get_chat(chat_id = update.effective_chat.id))
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Chat Info sended")
    except Exception as e:
           await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception: {e}")
           print(f"exception: {e}")
    
#async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
#    await context.bot.send_message(chat_id="-569283112", text="Test message evry 30 seconds")

async def callback_daily(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id="6017481524", text=conf.Message1 )

async def callback_daily1(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id="6017481524", text=conf.Message2 )

async def callback_daily2(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id="6017481524", text=conf.Message3 )



if __name__ == '__main__':
    application = ApplicationBuilder().token(conf.TOKEN).build()
    job_queue = application.job_queue
    
    local_timezone = pytz.timezone('Europe/Moscow')
    target_time = datetime.time(18, 41, 40, tzinfo=local_timezone)
    target_time1 = datetime.time(18, 42, 00, tzinfo=local_timezone)
    target_time2 = datetime.time(18, 42, 40, tzinfo=local_timezone)
    target_days = 0,1,2,3,4,5,6
    #job_minute = job_queue.run_repeating(callback_minute, interval=30, first=5)
    job_daily = job_queue.run_daily(callback_daily, time=target_time, days=target_days)
    job_daily1 = job_queue.run_daily(callback_daily1, time=target_time1, days=target_days)
    job_daily2 = job_queue.run_daily(callback_daily2, time=target_time2, days=target_days)
  
    
    info_handler = CommandHandler('sent_info', info)
    application.add_handler(info_handler)
   
    
    
    application.run_polling()
    


