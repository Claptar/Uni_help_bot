from database_queries import send_timetable

import asyncio


async def main():
    table = await send_timetable(my_group=True, chat_id=199502054)
    print(table[1][0]["Понедельник"])


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())
