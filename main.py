from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random

@register("dickfighting", "letr", "斗鸡插件", "0.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        from astrbot.core.utils.astrbot_path import get_astrbot_data_path
        from .db import Database
        
        # Ensure plugin_data directory exists
        plugin_data_path = get_astrbot_data_path() / "plugin_data" / self.name
        plugin_data_path.mkdir(parents=True, exist_ok=True)
        
        self.db = Database(str(plugin_data_path / "data.db"))

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    @filter.command("growth")
    async def growth(self, event: AstrMessageEvent):
        """增加用户的 dick 长度"""
        user_name = event.get_sender_name()
        # 尝试获取用户ID，如果获取不到则使用用户名
        user_id = user_name
        if hasattr(event, "get_sender_id"):
            user_id = event.get_sender_id()
            
        current_length = self.db.get_user_length(user_id)
        
        # 随机增加 0.1 到 5.0 cm
        growth_amount = round(random.uniform(0.1, 5.0), 2)
        new_length = round(current_length + growth_amount, 2)
        
        self.db.update_user_length(user_id, user_name, new_length)
        
        logger.info(f"User {user_name} (ID: {user_id}) dick grew by {growth_amount}cm, new length: {new_length}cm")
        
        yield event.plain_result(f"{user_name} 的 dick 长度增加了 {growth_amount} cm，当前长度为 {new_length} cm")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        if hasattr(self, "db"):
            self.db.close()
