import asyncio
import os
import sys

from psycopg2.extensions import register_adapter
from psycopg2.extras import Json

register_adapter(dict, Json)

DBNAME = os.environ["DATABASE"]
USER = os.environ["USER"]
PASS = os.environ["PASS"]
HOST = os.environ["HOST"]

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
