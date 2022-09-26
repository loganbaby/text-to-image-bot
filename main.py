from image_definer import ImageDefiner
from config import API_TOKEN
from aiogram import Dispatcher, Bot, executor
from aiogram import types

bot = Bot(API_TOKEN)
dispatcher = Dispatcher(bot)

image_def = ImageDefiner()   # global object of definer

lang_choosing_kb = types.ReplyKeyboardMarkup()    # global object of language keyboard
button_rus = types.KeyboardButton('Русский 🇷🇺')
button_eng = types.KeyboardButton('English 🇺🇸')
lang_choosing_kb.resize_keyboard = True

@dispatcher.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('Привет! Я - бот, который умеет конвертировать текст с изображения в текст, который можно скопировать :D\n\nПросто отправь мне любую картинку с текстом')

@dispatcher.message_handler(content_types=['document'])
async def image_define_document(message: types.Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await bot.download_file(file_path, 'img/recently.jpg')
    image_def.path_to_image = 'img/recently.jpg'

    await bot.send_message(chat_id=message.chat.id, text=str(image_def.get_word_by_path()))

@dispatcher.message_handler(content_types=['photo'])
async def image_define_photo(message: types.Message):
    image_def.path_to_image = 'img/recently.jpg'
    photo = message.photo.pop()

    await photo.download(destination_file='img/recently.jpg')
    await bot.send_message(chat_id=message.chat.id, text=str(image_def.get_word_by_path()))

@dispatcher.message_handler(commands=['language'])
async def choosing_language_of_photo(message: types.Message):
    lang_choosing_kb.add(button_rus, button_eng)
    await message.reply(reply_markup=lang_choosing_kb, text='Выберите текст на предложенной клавиатуре!\n\nЭтот текст очень важен при распознавании текста с картинки. Если на картинке нужно расшифровать русский текст, то вам следует указать \'Русский\'. Иначе, любой другой (тактика такая же)')

@dispatcher.message_handler(content_types=types.ContentTypes.TEXT)
async def choosing_language_definer(message: types.Message):
    if message.text == 'Русский 🇷🇺':
        image_def.language = 'rus'
        await message.reply(reply_markup=types.ReplyKeyboardRemove(), text='Русский язык установлен:) 🇷🇺🇷🇺🇷🇺')
    elif message.text == 'English 🇺🇸':
        image_def.language = 'eng'
        await message.reply(reply_markup=types.ReplyKeyboardRemove(), text='Английский язык установлен:) 🇷🇺🇷🇺🇷🇺')

if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher, skip_updates=True)
