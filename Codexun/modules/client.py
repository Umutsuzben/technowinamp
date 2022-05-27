import aiofiles
import ffmpeg
import asyncio
import os
import shutil
import psutil
import subprocess
import requests
import aiohttp
import yt_dlp
import aiohttp
import random

from os import path
from typing import Union
from asyncio import QueueEmpty
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from PIL import ImageGrab
from typing import Callable

from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

from youtube_search import YoutubeSearch

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    Voice,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


from Codexun.tgcalls import calls, queues
from Codexun.tgcalls.youtube import download
from Codexun.tgcalls import convert as cconvert
from Codexun.tgcalls.calls import client as ASS_ACC
from Codexun.database.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from Codexun import app
import Codexun.tgcalls
from Codexun.tgcalls import youtube
from Codexun.config import (
    DURATION_LIMIT,
    que,
    SUDO_USERS,
    BOT_ID,
    ASSNAME,
    ASSUSERNAME,
    ASSID,
    START_IMG,
    SUPPORT,
    UPDATE,
    BOT_NAME,
    BOT_USERNAME,
)
from Codexun.utils.filters import command
from Codexun.utils.decorators import errors, sudo_users_only
from Codexun.utils.administrator import adminsOnly
from Codexun.utils.errors import DurationLimitError
from Codexun.utils.gets import get_url, get_file_name
from Codexun.modules.admins import member_permissions


def others_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"resumevc"),
            InlineKeyboardButton(text="II", callback_data=f"pausevc"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"skipvc"),
            InlineKeyboardButton(text="▢", callback_data=f"stopvc"),
        ],[
            InlineKeyboardButton(text="Sistem", callback_data=f"cls"),
        ],
        
    ]
    return buttons


fifth_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200% 🔊", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Geri", callback_data=f"cbmenu"),
        ],
    ]
)

fourth_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150% 🔊", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Geri", callback_data=f"cbmenu"),
        ],
    ]
)

third_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100% 🔊", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Geri", callback_data=f"cbmenu"),
        ],
    ]
)

second_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50% 🔊", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Geri", callback_data=f"cbmenu"),
        ],
    ]
)

first_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20% 🔊", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Geri", callback_data=f"cbmenu"),
        ],
    ]
)
highquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Düşük Kalite", callback_data="low"),],
         [   InlineKeyboardButton("Orta Kalite", callback_data="medium"),
            
        ],[   InlineKeyboardButton("Yüksek Kalite ✅", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Geri", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="Kapat 🗑️", callback_data=f"cls"),
        ],
    ]
)
lowquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Düşük Kalite ✅", callback_data="low"),],
         [   InlineKeyboardButton("Orta Kalite", callback_data="medium"),
            
        ],[   InlineKeyboardButton("Yüksek Kalite", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Geri", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="Kapat 🗑️", callback_data=f"cls"),
        ],
    ]
)
mediumquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Düşük Kalite", callback_data="low"),],
         [   InlineKeyboardButton("Orta Kalite ✅", callback_data="medium"),
            
        ],[   InlineKeyboardButton("Yüksek Kalite", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Geri", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="Kapat 🗑️", callback_data=f"cls"),
        ],
    ]
)

dbclean_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Evet, Devam edin !", callback_data="cleandb"),],
        [    InlineKeyboardButton("Hayır, İptal Et !", callback_data="cbmenu"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Geri", callback_data=f"cbmenu"),
        ],
    ]
)
menu_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▢", callback_data="stopvc"),
            
        ],[
            InlineKeyboardButton(text="Ses", callback_data=f"fifth"),
             InlineKeyboardButton(text="Kalite", callback_data=f"high"),
        ],[
            InlineKeyboardButton(text="Listeyi Sil", callback_data=f"dbconfirm"),
             InlineKeyboardButton(text="Hakkında", callback_data=f"nonabout"),
        ],[
             InlineKeyboardButton(text="🗑️ Menüyü Kapat", callback_data=f"cls"),
        ],
    ]
)




@Client.on_message(command(["menu", "settings"]) & filters.group & ~filters.edited)
async def menu(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{START_IMG}",
        caption=f"""**Merhaba {message.from_user.mention()}** 👋
Ben, Gruplarınızdaki sesli sohbette müzik çalmayı yönetebileceğiniz menü bölümüdür. Yönetmek için verilen düğmeleri kullanın!""",
    reply_markup=menu_keyboard
    )

@Client.on_callback_query(filters.regex("skipvc"))
async def skipvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
Sesli sohbet yönetme izniniz olması gerekir.
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    if await is_active_chat(chat_id):
            user_id = CallbackQuery.from_user.id
            await remove_active_chat(chat_id)
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await CallbackQuery.answer()
            await CallbackQuery.message.reply(
                f"""
**{rpk}Tarafından Kullanılan Atla Düğmesi** 
•Kuyrukta daha fazla şarkı yok
`Sesli Sohbetten Ayrılıyorum..`
"""
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
            await CallbackQuery.answer("Sesli Sohbeti Atlatıldı..!", show_alert=True)     

@Client.on_callback_query(filters.regex("pausevc"))
async def pausevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Sesli sohbet yönetme izniniz olması gerekir",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await music_off(chat_id)
            await calls.pytgcalls.pause_stream(chat_id)
            await CallbackQuery.answer("Müzik Başarıyla Duraklatıldı..", show_alert=True)
            
        else:
            await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor!", show_alert=True)
            return
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor!", show_alert=True)


@Client.on_callback_query(filters.regex("resumevc"))
async def resumevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
Sesli sohbet yönetme izniniz olması gerekir.
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await CallbackQuery.answer(
                "Sesli sohbette hiçbir şey duraklatılmadı..",
                show_alert=True,
            )
            return
        else:
            await music_on(chat_id)
            await calls.pytgcalls.resume_stream(chat_id)
            await CallbackQuery.answer("Müzik başarıyla devam etti.", show_alert=True)
            
    else:
        await CallbackQuery.answer(f"Hiçbir şey çalmıyor.", show_alert=True)


@Client.on_callback_query(filters.regex("stopvc"))
async def stopvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Sesli sohbet yönetme izniniz olması gerekir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        
        try:
            await calls.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("Müzik akışı sona erdi.", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.message.reply(f"**Müzik {rpk} tarafından başarıyla durduruldu.**")
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)

@Client.on_callback_query(filters.regex("cleandb"))
async def cleandb(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Sesli sohbet yönetme izniniz olması gerekir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        
        try:
            await calls.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("Db cleaned successfully!", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.edit_message_text(
        f"✅ __Kuyruklar başarıyla silindi__\n│\n╰ Veritabanı {rpk} tarafından temizlendi",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("Kapat 🗑️", callback_data="cls")]])
        
    )
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)


@Client.on_callback_query(filters.regex("cbcmnds"))
async def cbcmnds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**{BOT_NAME} Komutları 💡**

• /play /oynat (Song Name /Şarkı Adı) 
- For playing music
- Müzik çalmak için


• /pause /durdur
- For pausing music
- Müziği duraklatmak için

• /resume /devam
- For resuming music
- Müziğe devam etmek için

• /skip /atla
- For skipping current song
- Geçerli şarkıyı atlamak için

• /search /bul (song name) 
- For searching music
- Müzik aramak için

• /song /indir
- For download music
- Müzik indirmek için

• /menu  /settings
- For open menu settings
- Menü ayarları için

Daha Fazla **@{UPDATE}** !""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton(
                        "Menu", callback_data="cbstgs"),
                    InlineKeyboardButton(
                        "Sahip Komutları", callback_data="cbowncmnds")
                ],
              [InlineKeyboardButton("🔙  Ana Menü", callback_data="cbhome")]]
        ),
    )
@Client.on_callback_query(filters.regex("cbowncmnds"))
async def cbowncmnds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Sahip Komutları 💡**

• /reklam (Mesaj)
- Bilgilendirme Mesajları için

• /sreklam (Mesaj) 
- Pın ile mesaj yayını

• /restart 
- Botu sunucudan yeniden başlat

• /ayrıl
- Tüm sohbetlerden asistanı bırakmak

Daha Fazla **@{UPDATE}** !""",
        reply_markup=InlineKeyboardMarkup(
            [
              
              [InlineKeyboardButton("🔙  Ana Menü", callback_data="cbcmnds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbabout"))
async def cbabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**{BOT_NAME} Hakkında  💡**

**[{BOT_NAME}](https://t.me/{BOT_USERNAME})** Müzik Botu **@OrmanCocuklariylaMucadele** Tarafından gruplarınızın sesli sohbetinde yüksek kaliteli ve kırılmaz bir müzik çalmak için tasarlanmış bottur.

This bot helps you to play music, to search music from youtube and to download music from youtube server and many more features related to telegram voice chat feature.

**Assistant :- @{ASSUSERNAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton("Destek 🚶", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("Kanal 🤖", url=f"https://t.me/{UPDATE}")
                ],
            [InlineKeyboardButton("🔙  Ana Menü", callback_data="cbhome")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbstgs"))
async def cbstgs(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Menü Düğmeleri Hakkında 💡**

Şarkınızı çaldıktan sonra, sesli sohbette çalan müziğinizi yönetmek için bazı menü düğmeleri gelecektir. Bunlar aşağıdaki gibidir :

• ▷ 
- Durdur
• II 
- Devam
• ▢  
- Son
• ‣‣ 
- Atla

Bu menüyü /menu ve /settings komutuyla da açabilirsiniz.

**Bu butonları sadece yöneticiler kullanabilir 📍**""",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("🔙  Ana Menü", callback_data="cbcmnds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Temel Kılavuzu Dikkatlice Okuyun 💡**

* Önce bu botu grubunuza ekleyin

* Bir bot yöneticisi olun

* Gerekli yönetici iznini verin

* Grubunuza /reload yazın 

* Gruplarınızın sesli sohbetini başlatın

* Şimdi şarkını çal ve tadını çıkar !""",
        reply_markup=InlineKeyboardMarkup(
            [[
              InlineKeyboardButton("Ortak Hata", callback_data="cberror")],
              [InlineKeyboardButton("🔙  Ana Menü", callback_data="cbhome")]]
        ),
    )


@Client.on_callback_query(filters.regex("cberror"))
async def cberror(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Çoğunlukla Hatalarla Karşı Karşıya Kaldı  💡**

Çoğunlukla, müzik asistanı ile ilgili ana hata olacaktır. Grubunuzda herhangi bir hatayla karşılaşıyorsanız, o zaman önce grubunuzda @{ASSUSERNAME} öğesinin kullanılabilir olduğundan emin olun. Değilse, manuel olarak ekleyin ve bundan önce de sohbetinizde yasaklanmadığından emin olun.\n\n**Asistan :- @{ASSUSERNAME}**\n\n**Teşekkürler !**""",
        reply_markup=InlineKeyboardMarkup(
            [
            [
                    InlineKeyboardButton("Asistan 🙋🏻‍♂️", url=f"https://t.me/{ASSUSERNAME}")
                ],
              [InlineKeyboardButton("🔙  Ana Menü", callback_data="cbguide")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbtuto"))
async def cbtuto(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Make Your Own Bot Like this💡**

Good news! Now you can allow to make your own music bot like to this one. You will be get repo link below just click on it and follow steps!

If you didn't know how to make your own bot then contact us at @TeamCodexun and get help from us.

**🔗 Repo Link : https://github.com/PavanMagar/CodexunMusicBot**

**Thanks !""",
       reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton("Get Repo 📦", url=f"https://github.com/PavanMagar/CodexunMusicBot")
                ],
              [InlineKeyboardButton("🔙  Ana Menü", callback_data="cbabout")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbhome"))
async def cbhome(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Hoşgeldiniz [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})** 👋

Ben **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) ,** Gruplarınızdaki sesli sohbette yüksek kaliteli ve kırılmaz müzik çalmak için kullanılan bir botum.

Sadece beni grubunuza ekleyin ve doğru eylemleri gerçekleştirmek için gerekli yönetici izinlerine sahip bir yönetici olarak yapın, şimdi müziğinizin tadını çıkaralım!

Daha fazla bilgi için verilen düğmeleri kullanın 📍""",
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

@Client.on_callback_query(filters.regex(pattern=r"^(cls)$"))
async def closed(_, query: CallbackQuery):
    from_user = query.from_user
    permissions = await member_permissions(query.message.chat.id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await query.answer(
            "Bu eylemi gerçekleştirmek için yeterli izniniz yok.",
            show_alert=True,
        )
    await query.message.delete()

@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Sen İsimsiz bir Yöneticisin !\n\n" yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("Sadece yöneticiler bunu kullanır..!", show_alert=True)
    chat_id = query.message.chat.id
    if is_music_playing(chat_id):
          await query.edit_message_text(
              f"**⚙️ {BOT_NAME} Ayarları**\n\n📮 Grup : {query.message.chat.title}.\n📖 Grup ID : {query.message.chat.id}\n\n**Aşağıda Verilen Tuşlara Basarak Gruplarınızın Müzik Sistemini Yönetin 💡**",

              reply_markup=menu_keyboard
         )
    else:
        await query.answer("Şu anda hiçbir şey akış halinde değil", show_alert=True)



@Client.on_callback_query(filters.regex("high"))
async def high(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Bunu yalnızca sesli sohbeti yönet iznine sahip yönetici yapabilir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Şimdi yüksek kalitede akış!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Ses Kalitesini Yönet 🔊**\n\nSes kalitesini yönetmek için aşağıdaki seçenekten seçiminizi yapın.",
        reply_markup=highquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)


@Client.on_callback_query(filters.regex("low"))
async def low(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Bunu yalnızca sesli sohbeti yönet iznine sahip yönetici yapabilir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Şimdi düşük kalitede akış!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Ses Kalitesini Yönet 🔊**\n\nSes kalitesini yönetmek için aşağıdaki seçenekten seçiminizi yapın.",
        reply_markup=lowquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)

@Client.on_callback_query(filters.regex("medium"))
async def medium(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Bunu yalnızca sesli sohbeti yönet iznine sahip yönetici yapabilir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Şimdi orta kalitede akış!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Ses Kalitesini Yönet 🔊**\n\nSes kalitesini yönetmek için aşağıdaki seçenekten seçiminizi yapın.",
        reply_markup=mediumquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)

@Client.on_callback_query(filters.regex("fifth"))
async def fifth(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Bunu yalnızca sesli sohbeti yönet iznine sahip yönetici yapabilir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Şimdi %200 hacimde akış!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Ses Kalitesini Yönet 🔊**\n\nSes seviyesini düğmelerle yönetmek istiyorsanız önce Yönetici yardımcısı olun.",
        reply_markup=fifth_keyboard
    )
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)

@Client.on_callback_query(filters.regex("fourth"))
async def fourth(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Bunu yalnızca sesli sohbeti yönet iznine sahip yönetici yapabilir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Şimdi %150 hacimde akış!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Ses Kalitesini Yönet 🔊**\n\nSes seviyesini düğmelerle yönetmek istiyorsanız önce Yönetici yardımcısı olun.",
        reply_markup=fourth_keyboard
    )
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)

@Client.on_callback_query(filters.regex("third"))
async def third(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Bunu yalnızca sesli sohbeti yönet iznine sahip yönetici yapabilir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Şimdi %100 hacimde akış!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Ses Kalitesini Yönet 🔊**\n\nSes seviyesini düğmelerle yönetmek istiyorsanız önce Yönetici yardımcısı olun.",
        reply_markup=third_keyboard
    )
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)


@Client.on_callback_query(filters.regex("second"))
async def second(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Bunu yalnızca sesli sohbeti yönet iznine sahip yönetici yapabilir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Şimdi %50 hacimde akış!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Ses Kalitesini Yönet 🔊**\n\nSes seviyesini düğmelerle yönetmek istiyorsanız önce Yönetici yardımcısı olun.",
        reply_markup=second_keyboard
    )
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)


@Client.on_callback_query(filters.regex("first"))
async def first(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Bunu yalnızca sesli sohbeti yönet iznine sahip yönetici yapabilir.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("Şimdi %20 hacimde akış!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**Ses Kalitesini Yönet 🔊**\n\nSes seviyesini düğmelerle yönetmek istiyorsanız önce Yönetici yardımcısı olun.",
        reply_markup=first_keyboard
    )
    else:
        await CallbackQuery.answer(f"Sesli sohbette hiçbir şey çalmıyor.", show_alert=True)

@Client.on_callback_query(filters.regex("nonabout"))
async def nonabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Here is the some basic information about to {BOT_NAME},From here you can simply contact us and can join us!**""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton("Destek 🚶", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("Kanal 🤖", url=f"https://t.me/{UPDATE}")
                ],
              [InlineKeyboardButton("🔙  Ana Menü", callback_data="cbmenu")]]
        ),
    )


@Client.on_callback_query(filters.regex("dbconfirm"))
async def dbconfirm(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Sen İsimsiz bir Yöneticisin !\n\n" yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("Sadece yöneticiler bunu kullanır..!", show_alert=True)
    chat_id = query.message.chat.id
    if is_music_playing(chat_id):
          await query.edit_message_text(
              f"**Onay ⚠️**\n\nSorgusunda akışı sonlandırmak istediğinizden emin misiniz? {query.message.chat.title} ve Liste'deki tüm Sıraya alınmış şarkıları temizle ?**",

              reply_markup=dbclean_keyboard
         )
    else:
        await query.answer("şu anda hiçbir şey akış halinde değil", show_alert=True)
