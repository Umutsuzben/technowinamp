import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, UserNotParticipant
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from Codexun.utils.filters import command

from Codexun.config import BOT_USERNAME 
from Codexun.config import BOT_NAME
from Codexun.config import START_IMG

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{START_IMG}",
        caption=f"""**Hoş geldiniz {message.from_user.mention()}** 👋

Ben **[{BOT_NAME}](https://t.me/{BOT_USERNAME})** Gruplarınızdaki sesli sohbette yüksek kaliteli ve kırılmaz müzik çalmak için kullanılan bir botum.

Sadece beni grubunuza ekleyin ve doğru eylemleri gerçekleştirmek için gerekli yönetici izinlerine sahip bir yönetici olarak yapın, şimdi müziğinizin tadını çıkaralım!

Daha fazla bilgi için verilen düğmeleri kullanın 📍 """,
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Komutlar", callback_data="cbcmnds"),
                    InlineKeyboardButton(
                        "Hakkında", callback_data="cbabout")
                ],
                [
                    InlineKeyboardButton(
                        "Basit Komutlar", callback_data="cbguide")
                ],
                [
                    InlineKeyboardButton(
                        "✚ Beni Grubuna Ekle ✚", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
           ]
        ),
    )
