
from pyrogram import Client, filters
from utils import USERNAME
from config import Config
ADMINS=Config.ADMINS
CACHE={}
from pyrogram.errors import BotInlineDisabled
@Client.on_message(filters.private & ~filters.bot & filters.incoming & ~filters.service & ~filters.me)
async def reply(client, message): 
    try:
        inline = await client.get_inline_bot_results(USERNAME, "ORU_MANDAN_PM_VANNU")
        m=await client.send_inline_bot_result(
            message.chat.id,
            query_id=inline.query_id,
            result_id=inline.results[0].id,
            hide_via=True
            )
        old=CACHE.get(message.chat.id)
        if old:
            await client.delete_messages(message.chat.id, [old["msg"], old["s"]])
        CACHE[message.chat.id]={"msg":m.updates[1].message.id, "s":message.message_id}
    except BotInlineDisabled:
        for admin in ADMINS:
            try:
                await client.send_message(chat_id=admin, text=f"Hey,\nParece que ha desactivado el modo en línea para @{USERNAME}\n\nUn Burro me está enviando spam en PM, habilite el modo en línea para @{USERNAME} de @Botfather to reply him.")
            except Exception as e:
                print(e)
                pass
    except Exception as e:
        print(e)
        pass
