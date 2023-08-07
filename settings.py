import os
import yaml


def load_config(config_file_path):
    """
    Функция для загрузки переменных конфигурации из yaml файла.
    """
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


config = load_config('config.yaml')


class Config(object):
    SQLALCHEMY_DATABASE_URI = config['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config['SECRET_KEY']
