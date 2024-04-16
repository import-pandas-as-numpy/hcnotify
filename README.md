## Description: 
This script will poll the hashcat potfile every 30 seconds for changes, and then post any given changes to a Discord webhook. 
The current configuration is managed through `config.json`. You will be prompted for your username (which will be displayed in the embed sent to the webhook), the full path to your hashcat.potfile, and a valid webhook. 


## Installation: 
Build from source using... 
`pip install git+https://github.com/import-pandas-as-numpy/hcnotify.git`

## To Use: 
**Windows**
`py -m hcnotify`

**Unix**
`python3 -m hcnotify`

This script also exposes a poetry entrypoint `poetry run hcnotify`.
