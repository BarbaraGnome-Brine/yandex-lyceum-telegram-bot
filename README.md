# Brine Warrior

---

Brine Warrior is an asynchronous Telegram bot designed for community moderation, statistics collection, and administrator notification. Its primary goal is to automatically monitor chat activity, detect anomalous behaviors (such as spam, flooding, or sudden audience growth), and generate analytical reports. By providing early warnings and automated metric gathering, it significantly reduces the workload on human moderators.

## ✨ Key Features

* **Statistics Collection:** Aggregates data on messages, user joins/leaves, and command usage while automatically detecting the user's language.


* **Active Moderation:** Analyzes real-time data flows to detect spam attacks or bot manipulations, instantly sending alerts to administrators.


* **Automated Digests:** Generates and delivers periodic summaries (text/graphics) of key chat metrics on a schedule.


* **Flexible Settings:** Allows administrators to toggle specific tracking metrics directly through the bot's interface.


* **Actionable Punishments:** Provides inline commands for warning, muting, and banning users, including an automated 7-day ban upon receiving two warnings.



## 🛠️ Technical Stack

* **Language:** Python 3.11+ 


* **Framework:** `python-telegram-bot` (v20+) 


* **Database:** SQLite (operational storage) with JSON for temporary caching 


* **Data Validation:** Pydantic 


* **Infrastructure:** Docker, Docker Compose 


* **CI/CD:** GitHub Actions (linting on PRs) 



## 🚀 Performance & Architecture

The project is built on a modular, asynchronous architecture designed to handle multiple highly active chats simultaneously with a response time of under 2 seconds.

### Component Breakdown

* **`handlers/`**: Listens for commands and messages, managing UI interactions like settings and stats.


* **`services/`**: The "brain" of the bot.
* `collector.py` intercepts and prepares chat events for the database.


* `analyzer.py` compares data flows to baselines to catch anomalies.


* `notification.py` handles triggers and alerts.




* **`models/`**: Strict Pydantic classes for internal data passing between the collector and analyzer.



## 💬 Bot Commands

### User & General Setup

* `/start` — Initial bot setup, private chat authorization, and admin verification.


* `/language` — Select preferred interface language (🇷🇺 Russian, 🇸🇪 Swedish, 🇺🇸 English).
* `/help` — Display available commands.



### Administration & Analytics

* `/stats` — View accumulated personal or chat statistics.


* `/settings` — Open the interface to configure monitoring parameters.


* `/digest` — Request a manual digest or manage automated digest subscriptions.



### Group Moderation (Admins Only)

* `/ban [duration] [reason]` — Ban a user for a specified duration (e.g., `1h`, `365d`).


* `/mute [duration] [reason]` — Restrict a user from sending messages.


* `/warn [reason]` — Issue a warning to a user. Two warnings trigger an automatic 7-day ban.


* `/unban` — Unban a user from the chat.


* `/unmute` — Restore a user's messaging permissions.



## 📂 Project Structure

```text
yandex-lyceum-telegram-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py
│   │   ├── stats.py
│   │   ├── settings.py
│   │   ├── help.py
│   │   └── digest.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── collector.py
│   │   ├── analyzer.py
│   │   ├── digest_builder.py
│   │   └── notification.py
│   └── models/
│       ├── __init__.py
│       └── stat.py
├── logs/
├── data/
│   ├── bot_stats.db
├── tests/
│   ├── __init__.py
│   └── test_collector.py
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── lint.yml
├── Makefile
└── README.md

```

## ⚙️ Deployment & Development

The bot uses containerization for rapid deployment, ensuring the SQLite database is safely stored in a local volume..

1. Clone the repository.
2. Configure your environment variables in `.env`.
3. Use the `Makefile` to quickly manage the development environment (clean DB, run tests, restart services).
4. Run via Docker: `docker-compose up -d`.
