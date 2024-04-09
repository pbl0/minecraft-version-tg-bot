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
from threading import Timer

import requests

MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
TELEGRAM_CHAT_ID = '{CHAT_ID}'
TELEGRAM_BOT_TOKEN = '{TELEGRAM_TOKEN}'
CHECK_DELAY = 60 * 5

print("Will poll every " + str(CHECK_DELAY) + " seconds for a new version...")

manifest = requests.get(MANIFEST_URL).json()

latestVersionAnnounced = manifest["latest"]["snapshot"]  # assume current latest version was already announced


class PerpetualTimer:
    def __init__(self, delay, executor):
        self.delay = delay
        self.executorFunction = executor
        self.timer = Timer(self.delay, self.executor)

    def executor(self):
        self.executorFunction()
        self.timer = Timer(self.delay, self.executor)
        self.timer.start()

    def start(self):
        self.timer.start()

    def cancel(self):
        self.timer.cancel()


def sendTelegramMessage(message):
    telegramResponse = requests.get("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage?chat_id=" + TELEGRAM_CHAT_ID + "&parse_mode=markdown&text=%s" % (urllib.parse.quote(message))).json()
    if not telegramResponse["ok"]:
        print("Failed to announce message: %s" % telegramResponse["description"])


def checkForVersionChange():
    global latestVersionAnnounced, manifest
    # print("Checking for new version...")
    manifest = requests.get(MANIFEST_URL).json()
    if manifest["latest"]["snapshot"] == latestVersionAnnounced:
        p# rint("No new version found")
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


print("Starting bot...")
timer = PerpetualTimer(CHECK_DELAY, checkForVersionChange)
timer.start()
