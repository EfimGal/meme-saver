import requests
from aiogram import Bot, Dispatcher, executor, types
import random
import os
from PIL import Image

print('Hello world')

API_TOKEN = '5861235513:AAE1Y9f7EYywXK-VhVl0rsW13myX94kkQbU'
wojak = 'D:\\envs\\telegram_bot\\images\\wojak.png'
greetings = 'D:\\envs\\telegram_bot\\random_replics\\start\\start.txt'
anecs_folder = 'D:\\envs\\telegram_bot\\random_replics\\anecs'
meme_folder = 'D:\\envs\\telegram_bot\\images\\memes'
temp_img_path = 'D:\\envs\\telegram_bot\\images'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем. 
async def send_welcome(message: types.Message):
    
   with open(greetings, 'r', encoding='utf-8') as f:
       my_lines = f.readlines()
   i = random.randint(0, len(my_lines) - 1)
   rand_message = my_lines[i]

   await message.reply("Привет!\nЯ бот от Тачкина!\n" + rand_message + 
                       "\nЧтобы получить получить юмореску напиши в чат /anec"
                       "\nСмешная картинка /meme") #Так как код работает асинхронно, то обязательно пишем await.
   await bot.send_photo(message.chat.id, types.InputFile(wojak))

@dp.message_handler(commands=['anec']) #Явно указываем в декораторе, на какую команду реагируем. 
async def send_anec(message: types.Message):
   text_files = [f for f in os.listdir(anecs_folder) if f.endswith('.txt')]
   i = random.randint(0, len(text_files) - 1)
   anec_path = anecs_folder + '\\' +text_files[i]
   with open(anec_path, 'r', encoding='utf-8') as f:
       anec = f.read()
   await message.answer(anec)

@dp.message_handler(commands=['meme']) #Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message): #Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
   images_files = [f for f in os.listdir(meme_folder) if f.endswith('.jpg')]
   i = random.randint(0, len(images_files) - 1)
   meme_path = meme_folder + '\\' +images_files[i]
   await bot.send_photo(message.chat.id, types.InputFile(meme_path))

@dp.message_handler()
async def echo(message: types.Message):
   await message.answer('К сожалению с людьми я не разговариваю, могу только показывать мемы (/meme) и рассказывать анеки(/anec)')

@dp.message_handler(content_types=['photo'])
async def photo_id(message):
    photo = max(message.photo, key=lambda x: x.height)
    #print(message)
    #File = await bot.get_file(photo.file_id)
    #print(photo)
    #await bot.download_file(temp_img_path, "temporary")
    #with open('temporary_image','wb') as new_file:
    #    new_file.write(File)
    #await bot.send_photo(message.chat.id, types.InputFile('temporary_image'))
    await message.answer('классная картинка')

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)