
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()
API_key = os.getenv("API_KOD5")
#bot_username = os.getenv("BOT_USERNAME")
print(API_key)
bot = telebot.TeleBot(API_key)




bmd = "CAACAgIAAxkBAAIBlmdxZi6sK42VCA3-ogaIn30MXGrmAAJnIAACKVtpSNxijIXcPOrMNgQ"

holatbot = True



import threading








# Keyboards-------------------------




def main_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if is_admin(message.chat.id):
        item_xy = types.KeyboardButton("📃Xabar yuborish")
        item_bh = types.KeyboardButton("🤖Bot holati")
        item_bc = types.KeyboardButton("◀️Orqaga")

        markup.row(item_xy,item_bh)
        markup.row(item_bc)
    return markup




ids_of_admin = [1218750814,6945876603]
def is_admin(user_id):
    global ids_of_admin
    for x in ids_of_admin:
        if user_id == x:
            return True
    return False


# checking Inchannel----------------------------
channel_id = "@telegrabotkrito"

list_channel: list = [["1-kanal", "https://t.me/neon_katanas"]]
def check_user_in_channel(message):
    return True

    # keyboard = InlineKeyboardMarkup()
    # global list_channel
    # bo = len(list_channel)
    # for c in list_channel:
    #     s: str = c[1]
    #     url1: str = f"@{s[13:]}"
    #     member = bot.get_chat_member(chat_id=url1, user_id=message.chat.id)
    #     if member.status not in ['member', 'administrator', 'creator']:
    #         keyboard.add(InlineKeyboardButton(text=c[0], url=c[1]))
    #     else:
    #         bo -= 1
    #
    # if bo > 0:
    #     start_button = InlineKeyboardButton("✅Tekshirish", callback_data="send_start")
    #     keyboard.add(start_button)
    #
    #     # bot.send_message(message.chat.id,
    #     #                  f"Assalomu alaykum \nAgar bizning xizmatlarimizdan foydalanmoqchi bo'lsangiz, Iltimos pastdagi kanallarga obuna bo'ling!",
    #     #                  reply_markup=keyboard)
    #     # bot.send_sticker(message.chat.id, sticker=bmd)
    #     return False
    # else:
    #     return True


# Starts bot--------------------------------------------------------------

list_users = []

def send_welcome(message: types.Message):

    user = message.from_user
    global list_users
    print(user.id , user.username , user.first_name, user.last_name)
    list_users.append((user.id , user.username , user.first_name, user.last_name))

    if check_user_in_channel(message) or is_admin(message.chat.id):

        bot.send_message(message.chat.id, "Assalomu alaykum, bu bot o'yin natijalarini qabul qiladi.",
                         reply_markup=main_keyboard(message))

    else:

        global list_channel
        keyboard = InlineKeyboardMarkup()
        for c in list_channel:
            s: str = c[1]
            url1: str = f"@{s[13:]}"
            member = bot.get_chat_member(chat_id=url1, user_id=message.chat.id)
            if member.status not in ['member', 'administrator', 'creator']:
                keyboard.add(InlineKeyboardButton(text=c[0], url=c[1]))


        start_button = InlineKeyboardButton("✅Tekshirish", callback_data=f"send_start")
        keyboard.add(start_button)


        bot.send_message(message.chat.id,
                         f"Assalomu alaykum \nAgar bizning xizmatlarimizdan foydalanmoqchi bo'lsangiz, Iltimos pastdagi kanallarga obuna bo'ling!",
                         reply_markup=keyboard)
        bot.send_sticker(message.chat.id, sticker=bmd)


@bot.callback_query_handler(func=lambda call: call.data.startswith("send_start"))
def a2(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print("In send_start function a2:",e)
        pass
    send_welcome(call.message)


@bot.message_handler(commands=['start'])
def a1(message):
    send_welcome(message)

#bot holat---------------------------------------------------
@bot.callback_query_handler(func= lambda call: call.data == "starts")
def startsbot(call):
    global holatbot
    holatbot = True
    switch(call.message)

def startbot(message):
    mes_key = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton(text= "✅Turn On" , callback_data= "starts")
    mes_key.add(but1)
    bot.send_message(message.chat.id, "⛔️Bot to'xtatildi.", reply_markup= mes_key)


@bot.callback_query_handler(func= lambda call: call.data == "stop")
def stops(call):
    global holatbot
    holatbot = False
    startbot(call.message)
@bot.message_handler(func = lambda message: message.text == "🤖Bot holati" and is_admin(message.chat.id))
def switch(message):
    global holatbot
    if is_admin(message.chat.id):
        keyboard = InlineKeyboardMarkup()
        if holatbot:
            hol = "Ishalamoqda"
        else:
            hol = "To'xtatilgan"
        button2 = InlineKeyboardButton(text="🚷Turn off", callback_data="stop")

        keyboard.add(button2)
        bot.send_message(message.chat.id, f"😇Bot holati: {hol}", reply_markup= keyboard )

# Broadcast tugmasi-----------------------------
broadcast_mode = False
@bot.message_handler(func=lambda message: message.text == "📃Xabar yuborish" and is_admin(message.chat.id))
def start_broadcast(message):
    global broadcast_mode
    if is_admin(message.chat.id):
        broadcast_mode = True
        bot.send_message(message.chat.id, text="❇️Yuboriladigan xabarni yozing...")
    else:
        bot.send_message(message.chat.id, "❌Siz bu tizimdan foyadalanish huquqiga ega emasiz.")
        bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAICk2d2pwlY_Az7yUl1HN1qkEGGlkLmAAI2EwACGJ3wUKir7ygymVAENgQ")



# Anime Izlash-------------------------------------------------------------------------------------------------------
def  find_user(user_id):
    global list_users
    for i in list_users:
        if user_id in i:
            return i
    return None

@bot.message_handler(content_types=["text", "photo", "video", "audio", "document", "sticker"])
def kod_check(message):
    global broadcast_mode, list_users
    if holatbot == False:
        bot.send_message(message.chat.id, "Natija qabul qilinish to'xtatildi.")
        return 0
    if is_admin(message.chat.id) and broadcast_mode:
        peaple = list_users


        for user in peaple:

            try:
                user_id = user[0]
                if int(user_id) == "":
                    print("bo'timiz")
                elif message.content_type == "text":
                    bot.send_message(user_id, message.text)
                    # Broadcast photos
                elif message.content_type == "photo":
                    bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
                    # Broadcast videos
                elif message.content_type == "video":
                    bot.send_video(user_id, message.video.file_id, caption=message.caption)
                    # Broadcast audio
                elif message.content_type == "audio":
                    bot.send_audio(user_id, message.audio.file_id, caption=message.caption)
                    # Broadcast documents
                elif message.content_type == "document":
                    bot.send_document(user_id, message.document.file_id, caption=message.caption)
                elif message.content_type == "sticker":
                    bot.send_sticker(user_id, message.sticker.file_id)
                else:
                    bot.send_message(message.chat.id, "Bu nomalum turdagi xabar")
            except Exception as e:
                print(f"⭕️️Bu userga xabar jo'natilmadi. {user}: {e}")
            finally:
                broadcast_mode = False
        bot.send_message(message.chat.id, "Xabar yuborib tugallandi.")
    elif not is_admin(message.chat.id) != False:
        global ids_of_admin
        for i in ids_of_admin:
            user = message.from_user
            if message.content_type == "text":
                bot.send_message(i, f"#{user.id} @{user.username} \n{message.text}")
            elif message.content_type == "photo":
                bot.send_photo(i, message.photo[-1].file_id, caption=message.caption)
                bot.send_message(i, f"#{user.id} @{user.username}")
            elif message.content_type == "video":
                bot.send_video(i, message.video.file_id, caption=message.caption)
                bot.send_message(i, f"#{user.id} @{user.username}")
            elif message.content_type == "audio":
                bot.send_audio(i, message.audio.file_id, caption=message.caption)
                bot.send_message(i, f"#{user.id} @{user.username}")
            elif message.content_type == "document":
                bot.send_document(i, message.document.file_id, caption=message.caption)
                bot.send_message(i, f"#{user.id} @{user.username}")
            elif message.content_type == "sticker":
                bot.send_sticker(i, message.sticker.file_id)
            else:
                bot.send_message(message.chat.id, "Bu nomalum turdagi xabar. Bu xabar yuborildi desa ham yuborilmagan bo'ladi.")
        bot.send_message(message.chat.id, "Bu xabar adminga yuborildi.")
    else:
        user_id = message.text.split("\n")[0]
        if len(user_id) >= 8 and len(user_id) <= 11:
            a = len(user_id)
            bot.send_message(int(user_id), text= message.text[a:])
        else:
            bot.send_message(message.chat.id, "User ID aniqlanmadi")


print("Your bot is running")
#bot.remove_webhook()
#bot.polling(none_stop=True)
bot.infinity_polling(skip_pending= True)
# bot.polling(none_stop=True, interval=1, timeout=2, long_polling_timeout=10)


# Close the database connection properly when the script exits