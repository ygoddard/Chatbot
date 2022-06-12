import yaml


class Config:
    database_uri: str
    database_username: str
    database_password: str

    contacts_database_name: str

    debug: bool
    port: int
    host: str

    account_sid: str
    auth_token: str

    session_dead_threshold_in_sec: int

    def __init__(self, config_path: str):
        self.load_configuration(config_path)

    def load_configuration(self, config_path: str):
        with open(config_path) as f:
            yaml_dict = yaml.safe_load(f)

        # loading class data from yaml
        for key, value in yaml_dict.items():
            setattr(self, key, value)
