from aiogram import Router
from aiogram.types import Message


router = Router()

@router.message()
async def send_echo(msg: Message):
    await msg.answer(text=f'ЭХО, эхо {msg.text}')