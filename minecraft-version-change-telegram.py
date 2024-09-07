"""
* Minecraft Version Change Telegram
* Copyright (C) 2020 Moritz Zwerger
*
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
* This software is not affiliated with Mojang AB, the original developer of Minecraft.
"""
import urllib.parse

import requests

MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
TELEGRAM_CHAT_ID = '{CHAT_ID}'
TELEGRAM_BOT_TOKEN = '{TELEGRAM_TOKEN}'

manifest = requests.get(MANIFEST_URL).json()

initial_version = manifest["latest"]["snapshot"]  
latestVersionAnnounced = None


def sendTelegramMessage(message):
    telegramResponse = requests.get("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage?chat_id=" + TELEGRAM_CHAT_ID + "&parse_mode=markdown&text=%s" % (urllib.parse.quote(message))).json()
    if not telegramResponse["ok"]:
        print("Failed to announce message: %s" % telegramResponse["description"])


def checkForVersionChange():
    global latestVersionAnnounced, manifest
    # print("Checking for new version...")
    manifest = requests.get(MANIFEST_URL).json()
    if manifest["latest"]["snapshot"] == latestVersionAnnounced:
        #print("No new version found")
        return
    print("New version found: %s" % manifest["latest"]["snapshot"])
    newVersionData = {}
    for version in manifest["versions"]:
        if version["id"] == manifest["latest"]["snapshot"]:
            newVersionData = version

    versionJson = requests.get(newVersionData["url"]).json()
    # announce in telegram
    sendTelegramMessage("""A new minecraft version is available: `%s`
Type: `%s`
""" % (newVersionData["id"],
       newVersionData["type"]))
    latestVersionAnnounced = newVersionData["id"]
    create_version_file(latestVersionAnnounced)

def create_version_file(version_id, filepath='/srv/bot/lastversion.txt'):
    print('create_version_file')
    # Create the file and write the version_id into it
    with open(filepath, 'w') as file:
        file.write(version_id)

def get_version(filepath='/srv/bot/lastversion.txt'):
    try:
        # Try reading the file if it exists
        with open(filepath, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        # File doesn't exist, return None and call the create function
        return None


if __name__ == '__main__':
    print("Starting bot...")
    version = get_version()

    if version is None:
        create_version_file(initial_version)  # assume current latest version was already announced
    else:
        print("Current version:", version)
        latestVersionAnnounced = version
        checkForVersionChange()