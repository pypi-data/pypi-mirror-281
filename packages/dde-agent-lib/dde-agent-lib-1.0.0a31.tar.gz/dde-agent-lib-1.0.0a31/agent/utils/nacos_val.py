import os
import yaml
import nacos

from agent.config.app_config import get_app_config
system_config_from_nacos = None
global_client_storage = None


def get_system_config_from_nacos():
    """从全局安全变量config_from_nacos中，线程安全读取nacos系统配置"""
    global system_config_from_nacos
    if (system_config_from_nacos is None):
        system_config_from_nacos = get_the_new_nacos_config()
    return system_config_from_nacos


def get_the_new_nacos_config():
    """
    将启动的实例注册到nacos上，以供portal后端通过nacos调用
    """
    app_configs = get_app_config()
    # 先从环境变量中获取nacos信息，如果为None，则从配置文件yaml中获取nacos信息
    nacos_group = os.environ.get('dde_nacos_group')
    if nacos_group is None:
        nacos_group = app_configs['nacos']['dde_nacos_group']
    nacos_namespace = os.environ.get('dde_nacos_namespace')
    if nacos_namespace is None:
        nacos_namespace = app_configs['nacos']['dde_nacos_namespace']
    nacos_server_address = os.environ.get('dde_nacos_addr_lib')
    global global_client_storage
    if (global_client_storage is None):
        global_client_storage = nacos.NacosClient(nacos_server_address, namespace=nacos_namespace)
    # 定义服务实例参数
    service_name = app_configs['nacos']['dde_instance_name']
    data_id = service_name + '.yaml'
    system_config = global_client_storage.get_config(data_id, nacos_group, 20, None)
    system_config_yaml = yaml.safe_load(system_config)
    return system_config_yaml