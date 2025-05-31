# MCQ Generator Telegram Bot
This is a Telegram bot that uses AI to generate multiple-choice questions (MCQs) based on any text you send, such as a sentence, paragraph or topic.
It uses the Google Gemini API to create questions with four answer choices.
After that, you can pick an answer, and the bot will tell you if you got it right or show the correct answer if you didn’t

---

## How it works
1. Start the bot and tap the **"Generate MCQ"** button.  
2. Send it any text, like a sentence, a paragraph, or just a topic.  
3. The bot will ask Google Gemini to create a question based on your text.  
4. You’ll get the question with four answer buttons labeled A, B, C, and D. 
5. Choose one, and the bot will tell you if your answer is correct or show the correct answer if you didn’t.

---

## What you need
- Docker & Docker Compose installed ([Docker install guide](https://docs.docker.com/get-docker/))
- A Google Gemini API key
- A Telegram Bot Token  

---


## Install Docker (for Linux)

If you're using **Ubuntu** or a Debian-based distro:

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
```
---
## Getting Started

### 1. Clone the project
```bash
git clone 
cd mcq-telegram-bot
```

### 2. Add your API keys
Create a `.env` file (or edit the one provided) with your keys:

```env
API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 3. Build and run the bot
```bash
docker-compose up --build -d
```

That’s it! Your bot is now running and ready to use on Telegram.

---

## Stopping the bot
To stop the bot use:

```bash
docker-compose down
```

---

## Project structure
- `main.py` – Telegram bot logic  
- `api.py` – Talks to Google Gemini and creates MCQs  
- `Dockerfile` – Docker image setup  
- `docker-compose.yml` – Easy Docker run config  
- `requirements.txt` – Python libraries used  
- `.env` – Your API keys

---

Made with ❤️ for learning and fun.
