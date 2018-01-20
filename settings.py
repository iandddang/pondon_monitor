import configparser

c = configparser.ConfigParser()
c.read("config.cfg")

class Config:
    # discord
    bot_token = c.get("discord","bot_token")
    channel_id = c.get("discord","channel_id")

    #monitoring
    baseURL = c.get("monitoring","baseURL")

config = Config()
