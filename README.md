# 🎙️ Discord Voice Management Bot

A flexible Discord bot designed to assist server moderators with **voice channel management**, **user role management**, and **action logging**. This bot is especially useful for managing a "detain" role and logging mute/unmute events for seamless moderation.

---

## ✨ Features

🚧 **Notice: This project is currently under construction.**  
Some features may not be fully functional or implemented yet. Contributions and feedback are welcome as development continues!  


### 🔊 Automatic Voice Channel Management
- Automatically unmutes users when they join or switch voice channels.
- Logs auto-unmute actions to a specified "Mute Log" channel.
- Notifies the user via DM about their auto-unmute.

### 🛡️ Detain Role Management
- **Assign the Detain Role**:
  - Use the `.detain` command to give a user the "Detain Role."
  - Logs the action in a specified "Detain Log" channel.
  - Notifies the user via DM that they have been detained.
- **Remove the Detain Role**:
  - Use the `.undetain` command to remove the "Detain Role."
  - Logs the action in the same "Detain Log" channel.
  - Notifies the user via DM that they have been undetained.

### 📜 Logging
- **Mute/Unmute Logging**:
  - Tracks and logs manual mute/unmute actions performed by moderators.
  - Logs include the affected user, the moderator, and timestamps.
  - Sends a DM to the affected user.
- **Detain/Undetain Logging**:
  - Tracks and logs when the "Detain Role" is added or removed manually or via commands.

### 📌 Dynamic Permissions
- (Optional) Grants dynamic mute permissions in new voice channels for selected users if configured.

### 🙌 Credit Command
- Displays bot credits via the `.credits` command in a subtle and professional manner.

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- A Discord bot token (you can create one at https://discord.com/developers/applications)
- Basic knowledge of Discord server roles and permissions.

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourgithubprofile/discord-voice-management-bot.git
   cd discord-voice-management-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - **Create a `.env` File**:  
     Copy the example `.env` file and add your bot token:
     ```bash
     cp .env.example .env
     ```
     Add your Discord bot token to the `.env` file:
     ```env
     DISCORD_BOT_TOKEN=your-bot-token-here
     ```

   - **Create a `config.json` File**:  
     Copy the example configuration file and update it with your server-specific details:
     ```bash
     cp config_template.json config.json
     ```
     Populate the `config.json` file with the following:
     ```json
     {
       "MUTE_LOG_CHANNEL_ID": 123456789012345678,
       "DETAIN_ROLE_ID": 123456789012345678,
       "DETAIN_LOG_CHANNEL_ID": 123456789012345678,
       "VOICEMASTER_BOT_ID": 123456789012345678
     }
     ```
     Replace the placeholder IDs with the actual IDs for your server:
     - **MUTE_LOG_CHANNEL_ID**: Channel ID for mute/unmute logs.
     - **DETAIN_ROLE_ID**: Role ID for the detain role.
     - **DETAIN_LOG_CHANNEL_ID**: Channel ID for detain/undetain logs.
     - **VOICEMASTER_BOT_ID**: (Optional) Bot ID of the VoiceMaster bot for dynamic permissions.

4. Run the bot:
   ```bash
   python discord_voice_manager.py
   ```

---

## 📋 Commands

| Command          | Description                                                                                          | Example                    |
|-------------------|------------------------------------------------------------------------------------------------------|----------------------------|
| `.detain @member` | Assigns the "Detain Role" to a user, logs the action, and sends a DM to the user.                    | `.detain @JohnDoe`         |
| `.undetain @member` | Removes the "Detain Role" from a user, logs the action, and sends a DM to the user.                | `.undetain @JohnDoe`       |
| `.credits`        | Displays bot credits in a professional and subtle manner.                                           | `.credits`                 |

---

## 🗂️ Logs and Notifications

### 🔊 Mute/Unmute Logs
- **Logged to**: Mute Log Channel (`MUTE_LOG_CHANNEL_ID`).
- **Details**:
  - User affected.
  - Moderator who performed the action.
  - Timestamp.
- **User Notification**:
  - Sends a DM to the affected user about the mute/unmute action.

### 🛡️ Detain Logs
- **Logged to**: Detain Log Channel (`DETAIN_LOG_CHANNEL_ID`).
- **Details**:
  - User detained or undetained.
  - Timestamp.
- **User Notification**:
  - Sends a DM to the user about the detain/undetain action.

---

## 🛡️ Configuration

### `.env`
Store sensitive data, like the bot token, in this file:
```env
DISCORD_BOT_TOKEN=your-bot-token-here
```

### `config.json`
Customize server-specific settings:
- **MUTE_LOG_CHANNEL_ID**: Channel ID for mute/unmute logs.
- **DETAIN_ROLE_ID**: Role ID for the detain role.
- **DETAIN_LOG_CHANNEL_ID**: Channel ID for detain logs.
- **VOICEMASTER_BOT_ID**: VoiceMaster bot ID (optional).

---

## 🖼️ Example Usage Scenarios

### 🎤 User Joins Voice Channel Muted
1. A user joins a voice channel while muted.
2. The bot detects this and unmutes the user automatically.
3. Logs the action in the "Mute Log" channel.
4. Sends a DM to the user notifying them of the unmute.

### 🛡️ Detaining a User
Note: You need to create a role called “Detained” in your Discord server. This role should have restricted permissions, such as no access to most channels except a specific “detention” channel (if desired). The bot assigns this role to users when they are detained.
1. A moderator uses `.detain @user` in any text channel.
2. The bot assigns the "Detain Role" to the user.
3. Logs the action in the "Detain Log" channel.
4. Sends a direct message to the user notifying them of the detain.

---

## 🙌 Credits

Developed and maintained by **Artur Pedrotti**.  
*For inquiries or contributions, feel free to reach out!*  
[GitHub Profile](https://github.com/arturpedrotti)

---

## 📜 License

This project is open-source and licensed under the [MIT License](LICENSE).
