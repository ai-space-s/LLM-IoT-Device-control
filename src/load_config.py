def load_config(config_path):
    with open(config_path, "r") as f:
        config = f.readlines()
    config = [i.replace(' ', '').replace('\n', '').split('=') for i in config if i[0] != '#']
    parsed_config = {}
    for cfg in config:
        parsed_config[cfg[0]] = cfg[1]
    return parsed_config
    

    