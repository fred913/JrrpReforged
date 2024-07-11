import os.path
from datetime import datetime

from mcdreforged.api.command import Literal
from mcdreforged.api.types import (CommandSource, PlayerCommandSource,
                                   PluginServerInterface)

from jrrp.helpers import McUuidModule

from .config import JrrpConfig


def get_todays_luck(string: str):
    now = datetime.now()
    num1 = round((abs(
        (hash("asdfgbn" + str(now.timetuple().tm_yday) + str(now.year) + "XYZ")
         / 3.0 + hash("QWERTY" + string + "0*8&6" + str(now.day) + "kjhg") /
         3.0) / 527.0) % 1001.0))
    num2 = round(num1 / 969.0 * 99.0) if num1 < 970 else 100
    return num2


def register_jrrp_command(server: PluginServerInterface):

    mc_uuid: McUuidModule | None = server.get_plugin_instance("mc_uuid")

    if mc_uuid is None:
        raise RuntimeError(
            "mc_uuid plugin is not loaded, jrrp command will not work.")

    config = server.load_config_simple(os.path.join("config", "jrrp.json"),
                                       in_data_folder=False,
                                       target_class=JrrpConfig)

    # target_class set so config is instance of JrrpConfig
    if not isinstance(config, JrrpConfig):
        config = JrrpConfig.deserialize(config)

    def reply_todays_luck(src: CommandSource):
        if not isinstance(src, PlayerCommandSource):
            src.reply("This command can only be used in-game by Players.")
            return

        online_res = mc_uuid.onlineUUID(src.player)
        player_uuid = online_res.hex if config.online_mode and online_res is not None else None
        if player_uuid is None:
            offline_res = mc_uuid.offlineUUID(src.player)
            if offline_res is None:
                raise RuntimeError("Invalid Player Name: {}".format(
                    src.player))
            player_uuid = offline_res.hex

        jrrp = get_todays_luck(player_uuid)
        for msg_obj in config.message:
            if eval(msg_obj["expr"]):
                prefix = msg_obj.get("start") or config.start
                suffix = msg_obj.get("end") or config.end
                title = msg_obj.get("title") or config.title
                msg = prefix + str(jrrp) + suffix
                if title:
                    src.get_server().execute("title {} {}".format(
                        src.player, msg))
                src.reply(msg)

    for command in config.command:
        server.register_command(Literal(command).runs(reply_todays_luck))


def on_load(server: PluginServerInterface, old):
    register_jrrp_command(server)
