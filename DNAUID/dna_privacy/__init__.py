from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.sv import SV

from ..utils.database.models import DNABind, DNAUser
from ..utils.msgs.notify import send_dna_notify

sv_dna_privacy = SV("dna隐私设置")


@sv_dna_privacy.on_command(
    (
        "隐藏uid",
        "隐藏UID",
        "显示uid",
        "显示UID",
    ),
    block=True,
)
async def toggle_uid_privacy(bot: Bot, ev: Event):
    """切换UID显示/隐藏设置"""
    uid = await DNABind.get_uid_by_game(ev.user_id, ev.bot_id)
    if not uid:
        await send_dna_notify(bot, ev, "您还未绑定UID，请先绑定")
        return

    # 获取用户信息
    dna_user = await DNAUser.select_dna_user(uid, ev.user_id, ev.bot_id)
    
    if "隐藏" in ev.command:
        # 设置隐藏
        if dna_user:
            await DNAUser.update_data_by_data(
                select_data={"user_id": ev.user_id, "bot_id": ev.bot_id, "uid": uid},
                update_data={"hide_uid": 1},
            )
        else:
            await DNAUser.insert_data(
                user_id=ev.user_id,
                bot_id=ev.bot_id,
                uid=uid,
                hide_uid=1,
            )
        await send_dna_notify(bot, ev, "已开启UID隐藏，后续作图将不会显示您的完整UID信息")
    else:
        # 设置显示
        if dna_user:
            await DNAUser.update_data_by_data(
                select_data={"user_id": ev.user_id, "bot_id": ev.bot_id, "uid": uid},
                update_data={"hide_uid": 0},
            )
            await send_dna_notify(bot, ev, "已关闭UID隐藏，后续作图将正常显示您的完整UID信息")
        else:
            # 没有记录时，创建一个显示的记录
            await DNAUser.insert_data(
                user_id=ev.user_id,
                bot_id=ev.bot_id,
                uid=uid,
                hide_uid=0,
            )
            await send_dna_notify(bot, ev, "已关闭UID隐藏，后续作图将正常显示您的完整UID信息")


@sv_dna_privacy.on_fullmatch(
    (
        "隐私设置",
        "查看隐私设置",
    ),
    block=True,
)
async def check_privacy_settings(bot: Bot, ev: Event):
    """查看当前隐私设置"""
    uid = await DNABind.get_uid_by_game(ev.user_id, ev.bot_id)
    if not uid:
        await send_dna_notify(bot, ev, "您还未绑定UID")
        return

    dna_user = await DNAUser.select_dna_user(uid, ev.user_id, ev.bot_id)
    
    if dna_user:
        status = "已开启" if dna_user.hide_uid == 1 else "已关闭"
    else:
        # 没有记录时，默认是开启状态
        status = "已开启（默认）"
    
    msg = f"当前隐私设置:\nUID隐藏: {status}\n\n使用 'dna隐藏uid' 或 'dna显示uid' 来切换设置"
    await send_dna_notify(bot, ev, msg)
