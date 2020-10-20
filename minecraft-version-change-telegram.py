"""
* Minecraft Version Change Telegram
* Copyright (C) 2020 Moritz Zwerger
*
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
*
*  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
*
*  You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
*  This software is not affiliated with Mojang AB, the original developer of Minecraft.
"""

from threading import Timer

import requests

MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
TELEGRAM_CHAT_ID = '@<chat id>'
TELEGRAM_BOT_TOKEN = '<token>'

manifest = requests.get(MANIFEST_URL).json()

latestVersionAnnounced = manifest["latest"]["snapshot"]  # assume current latest version was already announced


class perpetualTimer():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


def checkForVersionChange():
    global latestVersionAnnounced
    print("Checking for new version...")
    manifest = requests.get(MANIFEST_URL).json()
    if manifest["latest"]["snapshot"] == latestVersionAnnounced:
        print("No new version found")
        return
    print("New version found: %s" % manifest["latest"]["snapshot"])
    newVersion = {}
    for version in manifest["versions"]:
        if version["id"] == manifest["latest"]["snapshot"]:
            newVersion = version
    # announce in telegram
    telegramResponse = requests.get("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage?chat_id=" + TELEGRAM_CHAT_ID + "&parse_mode=markdown&text=Mojang just released a new minecraft %s: %s" % (newVersion["type"], newVersion["id"])).json()
    if not telegramResponse["ok"]:
        print("Failed to announce message: %s" % telegramResponse["description"])
    latestVersionAnnounced = newVersion["id"]


print("Starting bot...")
timer = perpetualTimer(60 * 60, checkForVersionChange)
timer.start()
