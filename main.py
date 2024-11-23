import time

from seed import Seed
from loguru import logger

"""
网页主页链接
https://seed.futunn.com/?client=mobile&target_lang=0&futusource=nnq_im
"""


def watering_friends():
    logger.info("开始向朋友浇水.")
    all_friends = seed.all_friends()
    for friend in all_friends:
        if friend.get("seed_state") == 0:
            time.sleep(10)
            uid_key = friend.get("uid_key")
            nick_name = friend.get("nick")
            result = seed.fert(uid_key)
            if result:
                logger.info("向朋友浇水成功 nike_name: {}, uid_key: {}".format(nick_name, uid_key))
            else:
                logger.warning("向朋友浇水失败 nike_name: {}, uid_key: {}".format(nick_name, uid_key))
    logger.info("结束向朋友浇水.")


def watering():
    logger.info("开始浇水.")
    room = seed.culture_room()
    if not room:
        logger.error("未获取到culture room")
        return

    seed_info = room.get("seed")
    if not seed_info:
        logger.error("未获取到seed info")
        return

    seed_id = seed_info.get("seed_id")
    seed_level = seed_info.get("seed_level")

    message = seed.water(seed_id)
    if message.get("status") == 200:
        logger.info("浇水成功: seed_id: {}, seed_level: {}, message: {}".format(seed_id, seed_level, message))
    else:
        logger.warning("浇水失败: seed_id: {}, seed_level: {}, message: {}".format(seed_id, seed_level, message))
    logger.info("结束浇水.")


if __name__ == '__main__':
    # setting log info
    logger.add(sink="seeding.log", level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

    seed = Seed()
    watering()
    watering_friends()
    pass
