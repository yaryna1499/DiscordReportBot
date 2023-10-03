from decouple import config


config = {
    "TOKEN": config("TOKEN"),
    "CHANNEL_ID": int(config("CHANNEL_ID")),
}


if __name__ == "__main__":
    print(repr(config))
