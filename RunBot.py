from aiogram.utils import executor
import database.db
from InstanceBot import dp
import handlers


async def on_startup(dp):
    database.db.check_db()
    print('Бот запущен')


handlers.hand_user2.add_hand_user(dp)
handlers.hand_admin.add_hand_admin(dp)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)