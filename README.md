# 🎙️ Discord Voice Management Bot

> 🚧 ⚠️ **Disclaimer**  
> This project is **not currently under active development**.  
> While the features and setup instructions are provided, there may be bugs or outdated information.  
> Contributions and feedback are still welcome, but users should be aware that support may be limited.

A flexible Discord bot to help server moderators manage **voice channels**, **roles**, and **moderation logs**. Ideal for handling "detain" scenarios and tracking mute/unmute actions seamlessly.

---

## ✨ Features

### 🔊 Automatic Voice Channel Management
- Automatically unmutes users upon joining or switching voice channels.
- Logs unmute events to a dedicated channel.
- Notifies users via DM.

### 🛡️ Detain Role Management
- Use `.detain` to assign a restricted role to users.
- Use `.undetain` to remove the restricted role.
- Sends DM notifications and logs both actions.

### 📜 Moderation Logging
- Logs manual mute/unmute actions and moderator info.
- Sends DMs to the affected users.
- All logs are timestamped and posted to configured channels.

### 🧠 Smart Configuration
- Uses `.env` and `config.json` for clean, secure setup.
- Easily adaptable to any Discord server.

---

## 🛠️ Setup Instructions

### ✅ Requirements
- Python 3.8+
- A Discord Bot Token from https://discord.com/developers/applications
- Admin access to your Discord server

### 🧩 Installation Steps

```bash
git clone https://github.com/arturpedrotti/discord-voice-manager.git
cd discord-voice-manager
pip install -r requirements.txt
```

### 🔐 Bot Configuration

#### 1. `.env`
Create a `.env` file to store your secret token:

```bash
touch .env
```

Paste this line into `.env`:

```env
DISCORD_BOT_TOKEN=your-discord-token-here
```

#### 2. `config.json`
Create a `config.json` using the template below:

```json
{
  "MUTE_LOG_CHANNEL_ID": 123456789012345678,
  "DETAIN_ROLE_ID": 123456789012345678,
  "DETAIN_LOG_CHANNEL_ID": 123456789012345678,
  "VOICEMASTER_BOT_ID": 123456789012345678
}
```

> Replace all `123456789012345678` with real Discord channel or role IDs from your server.

You can optionally create `config_template.json` and `.env.example` in the repo to help others.

---

## 🚀 Running the Bot

```bash
python discord_voice_manager.py
```

The bot will log in and respond to voice and role events.

---

## 📋 Commands

| Command             | Description                                                               |
|---------------------|---------------------------------------------------------------------------|
| `.detain @user`     | Assigns the detain role and notifies/logs the action                      |
| `.undetain @user`   | Removes the detain role and notifies/logs the action                      |
| `.credits`          | Displays bot creator and license information                              |

---

## 🧪 Example Scenario

### 🛡️ Detaining a User
1. Moderator types `.detain @JohnDoe`
2. The bot adds the "Detained" role
3. Logs the event to the Detain Log channel
4. Sends a DM to the user notifying them

### 🔊 Auto Unmute
1. A user joins a voice channel muted
2. The bot unmutes them and logs it
3. The user receives a DM with the update

---

## 🧩 File Structure

```bash
discord-voice-manager/
│
├── discord_voice_manager.py    # Main bot logic
├── config.json                 # Your server-specific IDs
├── .env                        # Your secret bot token
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # You are here
```

---

## 🙌 Credits

Built and maintained by **Artur Pedrotti**  
[GitHub](https://github.com/arturpedrotti)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🧠 Tips for Contributors

- Fork and clone the repo
- Add your changes in a new branch
- Keep commits atomic and clean
- Use `.env.example` and `config_template.json` to help others
- Submit a PR 🚀
