from agent.utils.nacos_util import get_the_new_nacos_config

system_config_from_nacos = None


def get_system_config_from_nacos():
    """从全局安全变量config_from_nacos中，线程安全读取nacos系统配置"""
    global system_config_from_nacos
    if (system_config_from_nacos is None):
        system_config_from_nacos = get_the_new_nacos_config()
    return system_config_from_nacos
