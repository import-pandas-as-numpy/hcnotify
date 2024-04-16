from .models import Potfile, Webhook, Password

import json
from pathlib import Path
import logging
import time
from datetime import datetime


def get_config(config_path: Path) -> dict:
    if not config_path.exists():
        logging.warning("Config file not found, prompting user for default config")
        return prompt_for_config()
    else:
        logging.info("Config found at location %s", config_path.as_posix())
        with config_path.open("r") as f:
            return json.load(f)


def _set_webhook(config: dict, webhook: Webhook) -> dict:
    config["webhook"] = webhook.to_dict()
    return config


def _set_potfile(config: dict, potfile: Potfile) -> dict:
    config["potfile"] = potfile.to_dict()
    return config


def write_config(config: dict, config_path: Path) -> None:
    with config_path.open("w") as f:
        json.dump(config, f, indent=4)
        logging.info("Config written to %s", config_path.as_posix())


def prompt_for_config() -> dict:
    config = {}
    webhook_url = input("Enter the webhook URL: ")
    potfile_path = input("Enter the path to the potfile: ")
    _set_webhook(config, Webhook(webhook_url))
    _set_potfile(config, Potfile(Path(potfile_path)))
    write_config(config, Path("config.json"))
    return config


def notify(webhook: Webhook, password: Password):

    payload = {
        "content": "Password cracked!",
        "embeds": [
            {
                "color": 5814783,
                "fields": [
                    {"name": "Password Hash", "value": f"`{password.hashed}`"},
                    {"name": "Password Plaintext", "value": f"`{password.plain}`"},
                ],
            }
        ],
        "username": "hcNotify",
        "attachments": [],
        "flags": 4096,
    }
    
    if password.cracked_by:
        payload["embeds"][0]["author"] = {"name": f"{password.cracked_by}"}
    if password.cracked_at:
        payload["embeds"][0]["timestamp"] = f"{datetime.fromtimestamp(password.cracked_at)}"
    print(payload)
    response = webhook.send(payload)
    if response.status_code == 204:
        logging.info("Notification sent successfully")
    else:
        logging.error(
            "Failed to send notification, response code: %s", response.status_code
        )


def load_passwords_from_json(json_path: Path) -> set[Password]:
    if not json_path.exists():
        return set()
    with json_path.open() as f:
        return set([Password(**p) for p in json.load(f)])


def dump_passwords_to_json(passwords: set[Password], json_path: Path) -> None:
    with json_path.open("w") as f:
        json.dump([p.to_dict() for p in passwords], f, indent=4)


def run():
    logging.basicConfig(level=logging.INFO)
    config = get_config(Path("config.json"))
    potfile = Potfile(Path(config["potfile"]["potfile_path"]))
    webhook = Webhook(config["webhook"]["url"])
    passwords = potfile.read().split("\n")
    found_passwords = load_passwords_from_json(Path("passwords.json"))
    for password in passwords:
        logging.debug("Checking password %s", password)
        if password:
            password = Password.from_string(password)
            if password not in found_passwords:
                logging.info("New password found %s", password)
                password.crack("Rem") # Replace with your user name.
                logging.debug("Sending notification for password %s", password.plain)
                notify(webhook, password)
                found_passwords.add(password)
    dump_passwords_to_json(found_passwords, Path("passwords.json"))
    write_config(config, Path("config.json"))


def event_loop(interval: int = 30):
    while True:
        run()
        time.sleep(interval)


if __name__ == "__main__":
    event_loop()
