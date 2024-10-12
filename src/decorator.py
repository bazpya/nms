from ncclient import manager as NetConfConnection


def with_connection(target_func):
    def wrapper(target_instance, *args, **kwargs):
        with NetConfConnection.connect(
            host=target_instance._url,
            port=target_instance._port,
            username=target_instance._username,
            password=target_instance._password,
            hostkey_verify=False,
            device_params={"name": "default"},
            allow_agent=False,
            look_for_keys=False,
        ) as connection:
            return target_func(target_instance, connection, *args, **kwargs)

    return wrapper
