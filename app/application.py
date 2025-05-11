# # import redis
# # from langchain.memory import ConversationBufferMemory
# # from langchain.memory.chat_message_histories import RedisChatMessageHistory
from agent.agent import Agent

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from utils import get_config, wait_for_chroma, wait_for_redis
from loguru import logger


config = get_config()
agent = Agent()
# redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
# wait_for_redis("localhost", 6379)


async def start(update, context):
    greeting = '''
    Привет! 

    Я - умный асситент, который может помочь тебе справиться с нападками со стороны сверстников в школе
    Ты можешь задать мне любой вопрос. 
    Я думаю, что смогу помочь тебе справиться с давлением, которые ты переодически испытываешь на себе
    '''
    await update.message.reply_text(greeting)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    response = agent.run(query)

    await update.message.reply_text(response)


# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = str(update.effective_user.id)
#     message = update.message.text

#     # Получаем историю пользователя
#     history = RedisChatMessageHistory(redis_client, session_id=user_id)
#     memory = ConversationBufferMemory(chat_memory=history, return_messages=True)

#     # Извлекаем текст истории
#     chat_context = memory.load_memory_variables({})["history"]

#     # Передаём вместе с вопросом
#     result = agent.graph.invoke({"input": message, "context": chat_context})
#     memory.save_context({"input": message}, {"output": result["response"]})

#     await update.message.reply_text(result["response"])


if __name__ == '__main__':
    # wait_for_chroma("localhost", 8000)
    print('start')
    try:
        app = ApplicationBuilder().token(config['telegram']['api_key']).build()
        logger.info('Application was succesfully started')
    except:
        logger.warning('Cant process passed token')
        raise Exception('Invalid token was passed. Pass correct one instead')
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
