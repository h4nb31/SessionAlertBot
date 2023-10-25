#This bot for testing some features
import logging
import conf
import datetime
from apscheduler import schedulers
import time
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, JobQueue
from telegram.ext import Job
import pytz

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print (await context.bot.get_chat(chat_id = update.effective_chat.id))
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ифнормация по чату отправлена")
    except Exception as e:
           await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception: {e}")
           print(f"exception: {e}")
    
#async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
#    await context.bot.send_message(chat_id="-569283112", text="Test message evry 30 seconds")

def user_input(u_input: str):
    return u_input

async def Daily_ping(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id="6017481524", text=conf.Message_P + conf.Message1 )

async def Daily_ping_repeat_1(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id="6017481524", text=conf.Message2 )

async def Daily_ping_repeat_2(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id="6017481524", text=conf.Message3 )

async def get_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    job_name = [Job.name for Job in context.job_queue.jobs()]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Все работающие задания: \n\n" + str(job_name)) 
    
async def remove_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        job_name = [Job.name for Job in context.job_queue.jobs()]
        job_id = [Job.id for Job in context.job_queue.jobs()]
        job_len = len(job_name)
        for i in job_name:
            if (job_name[i] == context.args[0]):
                await context.bot.send_message(chat_id=update.effective_chat.id, text=job_name[i])
                context.job_queue.scheduler.remove_job(str(job_id[i]))
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Job: " + str(job_name[i]) +"\nStatus: Deleted")
        ##context.job_queue.scheduler.remove_job()
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception: {e}")
        print(context.job_queue.scheduler.get_jobs())
        print(type(job_name))
    

if __name__ == '__main__':
    application = ApplicationBuilder().token(conf.TOKEN).build()
    job_queue = application.job_queue
    
    local_timezone = pytz.timezone('Europe/Moscow')
    target_time = datetime.time(21, 2, 40, tzinfo=local_timezone)
    target_time1 = datetime.time(18, 42, 00, tzinfo=local_timezone)
    target_time2 = datetime.time(18, 42, 40, tzinfo=local_timezone)
    target_days = 0,1,2,3,4,5,6
    
    #Constant jobs
    job_daily = job_queue.run_daily(Daily_ping, time=target_time, days=target_days)
    job_daily = job_queue.run_daily(Daily_ping_repeat_1, time=target_time1, days=target_days)
    job_daily = job_queue.run_daily(Daily_ping_repeat_2, time=target_time2, days=target_days)
  
    jobs_handler = CommandHandler('jobs', get_jobs)
    info_handler = CommandHandler('send_info', info)
    remove_handler = CommandHandler('remove_job',remove_job)
    application.add_handler(info_handler)
    application.add_handler(jobs_handler)
    application.add_handler(remove_handler)
   
    
    
    application.run_polling()
    


