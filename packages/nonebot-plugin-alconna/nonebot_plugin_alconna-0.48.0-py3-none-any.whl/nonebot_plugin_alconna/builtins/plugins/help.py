import sys
import random
from pathlib import Path

from tarina import lang
from nonebot.adapters import Bot
from importlib_metadata import PackageNotFoundError, distribution
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from arclet.alconna import Args, Field, Option, Alconna, Arparma, CommandMeta, namespace, store_true, command_manager

from nonebot_plugin_alconna import UniMessage, AlconnaMatcher, referent, on_alconna

__plugin_meta__ = PluginMetadata(
    name="help",
    description="展示所有命令帮助",
    usage="/help",
    type="application",
    homepage="https://github.com/nonebot/plugin-alconna/blob/master/src/nonebot_plugin_alconna/builtins/plugins/help.py",
    config=None,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)


def check_supported_adapters(matcher: type[AlconnaMatcher], bot: Bot):
    if matcher.plugin and matcher.plugin.metadata:
        adapters = matcher.plugin.metadata.supported_adapters
        if adapters is None:
            return True
        if not adapters:
            return False
        adapters = {s.replace("~", "nonebot.adapters") for s in adapters}
        return bot.adapter.__module__.removesuffix(".adapter") in adapters
    return True


def get_info(matcher: type[AlconnaMatcher]):
    if matcher.plugin:
        if matcher.plugin.metadata:
            plugin_name = matcher.plugin.metadata.name
        else:
            plugin_name = matcher.plugin.name
    else:
        plugin_name = matcher.plugin_id or lang.require("nbp-alc/builtin", "help.plugin_name_unknown")
    plugin_id = matcher.plugin_id or lang.require("nbp-alc/builtin", "help.plugin_name_unknown")
    mod = matcher.module or sys.modules["__main__"]
    mod_path = Path(mod.__file__)  # type: ignore
    while mod_path.parent != mod_path:
        try:
            dist = distribution(mod_path.name)
            break
        except PackageNotFoundError:
            mod_path = mod_path.parent
    else:
        return f"""\
{lang.require("nbp-alc/builtin", "help.plugin_name")}: {plugin_name}
{lang.require("nbp-alc/builtin", "help.plugin_id")}: {plugin_id}
{lang.require("nbp-alc/builtin", "help.plugin_path")}: {matcher.module_name}
"""
    return f"""\
{lang.require("nbp-alc/builtin", "help.plugin_name")}: {plugin_name}
{lang.require("nbp-alc/builtin", "help.plugin_id")}: {plugin_id}
{lang.require("nbp-alc/builtin", "help.plugin_module")}: {dist.name}
{lang.require("nbp-alc/builtin", "help.plugin_version")}: {dist.version}
{lang.require("nbp-alc/builtin", "help.plugin_path")}: {matcher.module_name}
"""


with namespace("builtin/help") as ns:
    ns.disable_builtin_options = {"shortcut"}

    help_cmd = Alconna(
        "help",
        Args[
            "query#选择某条命令的id或者名称查看具体帮助;/?",
            str,
            Field(
                "-1",
                completion=lambda: f"试试 {random.randint(0, len(command_manager.get_commands()))}",
                unmatch_tips=lambda x: f"预期输入为某个命令的id或者名称，而不是 {x}\n例如：/帮助 0",
            ),
        ],
        Option(
            "--plugin-info",
            alias=["-P", "插件信息"],
            help_text="查看命令所属插件的信息",
            action=store_true,
            default=False,
        ),
        Option("--hide", alias=["-H", "隐藏"], help_text="是否列出隐藏命令", action=store_true, default=False),
        meta=CommandMeta(
            description="显示所有命令帮助",
            usage="可以使用 --hide 参数来显示隐藏命令，使用 -P 参数来显示命令所属插件名称",
            example="$help 1",
        ),
    )

help_matcher = on_alconna(help_cmd, use_cmd_start=True, auto_send_output=True)
help_matcher.shortcut("帮助", {"prefix": True, "fuzzy": False})
help_matcher.shortcut("命令帮助", {"prefix": True, "fuzzy": False})
help_matcher.shortcut("所有帮助", {"args": ["--hide"], "prefix": True, "fuzzy": False})
help_matcher.shortcut("所有命令帮助", {"args": ["--hide"], "prefix": True, "fuzzy": False})
help_matcher.shortcut(
    "(获取)?插件信息", {"args": ["--plugin-info", "{%0}"], "prefix": True, "fuzzy": True, "humanized": "[获取]插件信息"}
)


@help_matcher.handle()
async def help_cmd_handle(arp: Arparma, bot: Bot, event):
    is_plugin_info = arp.query[bool]("plugin-info.value", False)
    cmds = [i for i in command_manager.get_commands() if not i.meta.hide or arp.query[bool]("hide.value", False)]
    cmds = [i for i in cmds if ((mat := referent(i)) and check_supported_adapters(mat, bot)) or not mat]
    if (query := arp.all_matched_args["query"]) != "-1":
        if query.isdigit():
            slot = cmds[int(query)]
            _matcher = referent(slot)
            if not _matcher:
                msg = slot.get_help()
            else:
                executor = _matcher.executor
                if is_plugin_info:
                    msg = UniMessage.text(get_info(_matcher))
                else:
                    msg = await executor.output_converter("help", slot.get_help())
                    msg = msg or UniMessage(slot.get_help())
                msg = await executor.send_wrapper(bot, event, msg)
            return await help_matcher.finish(msg)
        elif is_plugin_info:
            command_string = "\n".join(
                f" 【{str(index).rjust(len(str(len(cmds))), '0')}】{slot.header_display} : {get_info(mat)}"
                for index, slot in enumerate(cmds)
                if query in slot.header_display and (mat := referent(slot))
            )
            return await help_matcher.finish(command_string)
        command_string = "\n".join(
            f" 【{str(index).rjust(len(str(len(cmds))), '0')}】{slot.header_display} : {slot.meta.description}"
            for index, slot in enumerate(cmds)
            if query in slot.header_display
        )
        if not command_string:
            return await help_matcher.finish("查询失败！")
    else:
        command_string = "\n".join(
            f" 【{str(index).rjust(len(str(len(cmds))), '0')}】{slot.header_display} : {slot.meta.description}"
            for index, slot in enumerate(cmds)
        )
    help_names = set()
    for i in cmds:
        help_names.update(i.namespace_config.builtin_option_name["help"])
    header = lang.require("manager", "help_header")
    footer = lang.require("manager", "help_footer").format(help="|".join(sorted(help_names, key=lambda x: len(x))))
    return await help_matcher.finish(f"{header}\n{command_string}\n{footer}")
