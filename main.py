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
    send_state = seed_info.get('send_state')
    seed_level = seed_info.get("seed_level")
    comm_affect_type = seed_info.get("comm_affect_type")
    comm_affect_value = seed_info.get("comm_affect_value")
    is_mature = seed_info.get("is_mature")
    # 种子成熟
    if is_mature == 1:
        logger.info("种子成熟: seed_id: {}.".format(seed_id))
        # 免佣种子
        if comm_affect_type == 1:
            pass
        # 现金种子
        if comm_affect_type == 3:
            result = seed.use(seed_id)
            if result:
                logger.info("现金种子使用成功: seed_id: {}, seed_level: {}，comm_affect_type: {}, comm_affect_value: {}.".format(seed_id, seed_level, comm_affect_type, comm_affect_value))
            else:
                logger.warning("现金种子使用失败: seed_id: {}, seed_level: {}，comm_affect_type: {}, comm_affect_value: {}.".format(seed_id, seed_level, comm_affect_type, comm_affect_value))
        # 积分种子
        if comm_affect_type == 4:
            result = seed.use(seed_id)
            if result:
                logger.info("积分种子使用成功: seed_id: {}, seed_level: {}，comm_affect_type: {}, comm_affect_value: {}.".format(seed_id, seed_level, comm_affect_type, comm_affect_value))
            else:
                logger.warning("积分种子使用失败: seed_id: {}, seed_level: {}，comm_affect_type: {}, comm_affect_value: {}.".format(seed_id, seed_level, comm_affect_type, comm_affect_value))
    else:
        logger.info("种子未成熟: seed_id: {}.".format(seed_id))
        water_limit_num = seed_info.get("water_limit_num")
        water_done_num = seed_info.get("water_done_num")
        if (water_limit_num - water_done_num) > 0:
            message = seed.water(seed_id)
            if message.get("code") == 0:
                logger.info("浇水成功: seed_id: {}, seed_level: {}, water_limit_num: {}, water_done_num: {}, message: {}".format(seed_id, seed_level, water_limit_num, water_done_num, message))
            else:
                logger.warning("浇水失败: seed_id: {}, seed_level: {}, water_limit_num: {}, water_done_num: {}, message: {}".format(seed_id, seed_level, water_limit_num, water_done_num, message))
        else:
            logger.info("浇水次数上限: seed_id: {}, seed_level: {}, water_limit_num: {}, water_done_num: {}".format(seed_id, seed_level, water_limit_num, water_done_num))
    logger.info("结束浇水.")


if __name__ == '__main__':
    # setting log info
    logger.add(sink="seeding.log", level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

    seed = Seed()
    watering()
    watering_friends()
