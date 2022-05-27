from pyrogram import Client
from Codexun.tgcalls import client as USER
from pyrogram import filters
from pyrogram.types import Chat, Message, User
from Codexun.config import (
    BOT_USERNAME,
)

@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
  await USER.send_message(message.chat.id,"Merhaba, bu müzik botunun asistanı, kendi müzik botunuzu yapmak istiyorsanız.\n\n@OrmanCocuklariylaMucadele bizimle iletişime geçin!\n\n@BotDestekGrubu tarafından desteklenmektedir")
  return
