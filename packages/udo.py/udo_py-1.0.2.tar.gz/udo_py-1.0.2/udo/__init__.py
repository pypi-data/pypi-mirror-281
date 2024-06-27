import logging
from ._version import __version__
from .core.udo import udo
from .core.jeju_log import *
from os.path import isfile
import os
import json

Directory = os.path.dirname(os.path.realpath(__file__))

logger: logging.Logger = logging.getLogger(__name__)

if not isfile(f'{Directory}/core/data.json'):
    sdd = {
            "udo": {
                "tag": "udo",
                "value": "**udo project for py-cord**\n```py\npip install -U udo\n```\n```py\nbot.load_extension('udo')\n# or\nawait bot.load_extension('udo')\n```"
            } 
        }
    with open(f"{Directory}/core/data.json", "w",encoding="utf-8-sig") as json_file:
        json.dump(sdd,json_file,ensure_ascii = False, indent=4)
else:
    logger.info("[ udo ] The initial setup was skipped because the file was already created.")

async def setup(bot):
    await bot.add_cog(log(bot))
    await bot.add_cog(udo(bot))