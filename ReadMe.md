# Minecraft Version Change Telegram

Just a simple bot, that can send you (or a group) a telegram message, when mojang releases a new version of minecraft.

## About This Fork

This repository is a fork of [Minecraft Version Change Telegram Bot](https://gitlab.bixilon.de/bixilon/minecraft-version-change-telegram) by [Moritz Zwerger](https://bixilon.de/en).

- **Date Forked:** 06-09-2024 (dd-mm-yyyy)

### Changes

- It now works as a oneshot instead of constantly running in the background.
- Will store the last checked version in /srv/bot/lastversion.txt so the next time it knows if it needs to announce version changes or not.
- The message format remains the same.

Setup:

1. Create a Telegram channel/group and add your bot to it
2. Set config/chat_id.txt to your channel/group id.
3. Set config/token.txt to your bot token
4. Create and run the Podman (or Docker) container:

```bash
podman build -t minecraft-version-tg-bot .

podman run --name minecraft-version-tg-bot -v=${PWD}/config/:/srv/bot/ minecraft-version-tg-bot
```

5. Use podman generate to create a systemd service. (use [podman quadlets](https://www.redhat.com/sysadmin/quadlet-podman) instead if using Podman 4.4+)

```bash
podman generate systemd --new --name minecraft-version-tg-bot > ~/.config/systemd/user/minecraft-version-tg-bot.service
```

6. Create a minecraft-version-tg-bot.timer file with the desired onCalendar setting. There are examples of systemd service and timer on the [systemd/](systemd) folder.

## Original project demo

See [@MinecraftVersionChanges](https://t.me/MinecraftVersionChanges)
