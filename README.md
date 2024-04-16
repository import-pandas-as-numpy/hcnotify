## Description: 
This script will poll the hashcat potfile every 30 seconds for changes, and then post any given changes to a Discord webhook. 
The current configuration is managed through `config.json`. You will be prompted for your username (which will be displayed in the embed sent to the webhook), the full path to your hashcat.potfile, and a valid webhook. 
This first run will generate the `config.json` for you.

It is my recommendation that this be used for competitions, and potfiles be backed up and cleared before the competition starts to ensure that only valid competition entries are posted through the webhook. If the potfile
is not cleared, this will produce a large amount of output through the webhook until the potfile has been serialized as JSON. After this point, only new entries in the potfile will be posted to the webhook.


## Installation: 
Build from source using 
`pip install git+https://github.com/import-pandas-as-numpy/hcnotify.git`

## To Use: 
**Windows**
`py -m hcnotify`

**Unix**
`python3 -m hcnotify`

This script also exposes a poetry entrypoint `poetry run hcnotify`.
