import sys
import importlib
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


files = os.listdir(os.getcwd() + '/tg_bot/plugin')
for file in files:
    try:
        if file.endswith('.py'):
            filename = file.replace('.py', '')
            importlib.import_module('tg_bot.plugin.' + filename)
            logger.info(f"Bot加载-->{filename}-->完成")
    except Exception as e:
        logger.info(f"Bot加载失败-->{file}-->{str(e)}")
        continue
