"""
UID 隐私保护工具模块

提供 UID 隐私保护相关的核心函数
"""

from gsuid_core.logger import logger

from .database.models import DNAUser


async def check_uid_privacy(uid: str, user_id: str, bot_id: str) -> bool:
    """
    检查用户是否开启了UID隐藏功能

    Args:
        uid: 游戏UID（原始完整UID）
        user_id: 用户ID
        bot_id: 机器人ID

    Returns:
        bool: True表示需要隐藏UID，False表示正常显示
    """
    try:
        dna_user = await DNAUser.select_dna_user(uid, user_id, bot_id)
        if dna_user:
            # 如果有记录，按照用户设置
            return dna_user.hide_uid == 1
        # 如果没有记录，默认隐藏（新用户默认开启隐私保护）
        return True
    except Exception as e:
        logger.error(f"检查UID隐私设置失败: {e}")
        # 出错时默认隐藏，保护隐私
        return True


async def get_display_uid(uid: str, user_id: str, bot_id: str) -> str:
    """
    获取用于显示的UID

    根据用户隐私设置返回相应的UID格式：
    - 隐私保护开启：返回隐藏格式（如 123****789）
    - 隐私保护关闭：返回完整UID

    Args:
        uid: 原始完整UID（用于API调用）
        user_id: 用户ID
        bot_id: 机器人ID

    Returns:
        str: display_uid - 用于显示的UID
            - 隐私保护开启时: "123****789"
            - 隐私保护关闭时: uid (完整)
    """
    hide = await check_uid_privacy(uid, user_id, bot_id)

    if not hide:
        # 隐私保护关闭：display_uid = uid
        return uid

    # 隐私保护开启：display_uid = hide_uid
    if len(uid) >= 6:
        return f"{uid[:3]}****{uid[-3:]}"
    else:
        return "******"
