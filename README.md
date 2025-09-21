# 🕹️ AI-Powered Gamified Hacker Terminal

An interactive, **gamified terminal** built in Python that combines:
- ⚡ System commands (`ls`, `cpu`, `mem`, etc.)
- 🤖 AI-powered natural language → command translation (Gemini API)
- 🎯 Missions & XP-based leveling system
- 🎲 Fun hacker-style extras (`matrix`, `scan`, `whoami`, `guess`)
- 💾 Persistent profile (`profile.json`) to save progress

---

## ✨ Features
- **Gamification**
  - Earn XP by running commands
  - Level up with ASCII banners 🎉
  - Random power-ups 💎
  - Daily missions (e.g., "Run `ls` 3 times") for bonus XP 🏆
- **AI Translator**
  - Convert natural language to terminal commands with Google Gemini
  - Example:  
    ```
    ai "create a folder called test"
    ```
    👉 Executes: `mkdir test`
- **Hacker Extras**
  - `matrix` → falling green code (like The Matrix)
  - `scan` → fake port scanner
  - `whoami` → random hacker identity
  - `guess` → number guessing game 🎲
- **System Monitoring**
  - `cpu`, `mem`, `ps` for resource stats
- **Persistence**
  - XP, Level, and Missions are saved in `profile.json`

---

## 📦 Installation

### 1. Clone Repo
```bash
git clone https://github.com/your-username/hacker-terminal.git
cd hacker-terminal
2. Install Dependencies
Make sure you have Python 3.9+. Then install:

bash
Copy code
pip install -r requirements.txt
requirements.txt

nginx
Copy code
psutil
google-generativeai
rich
prompt_toolkit
3. Set Your Gemini API Key
Edit the Python file and replace:

python
Copy code
API_KEY = "YOUR_API_KEY"
Get a key from Google AI Studio.

🚀 Usage
Run the terminal:

bash
Copy code
python terminal.py
Sample Commands
bash
Copy code
pwd             # Show current directory
ls              # List files
cpu             # Show CPU usage
fortune         # Get a random motivational/dev quote
ai "list files" # Natural language → command
matrix          # Falling code animation
scan            # Fake port scan
whoami          # Random hacker identity
guess           # Number guessing game
help            # Show all commands
exit            # Save & quit
🎮 Gamification
XP is awarded for every command

Level up when XP crosses a threshold

Missions (quests) give bonus XP

Random power-ups occasionally drop 🎁

🖼️ Screenshots
bash
Copy code
🎯 Mission: Use ls 3 times (1/3)

[~/Projects] > ls
📁 src/
📄 readme.md
🎮 XP: 10/50 (Level 1)

[~/Projects] > fortune
🍀 Code is like humor. When you have to explain it, it’s bad.
🎮 XP: 20/50 (Level 1)

[~/Projects] > ai "make a test folder"
🤖 Executing:
mkdir test
🎮 XP: 30/50 (Level 1)
🛠️ Tech Stack
Python 3.9+

Rich for UI

Prompt Toolkit for autocomplete

psutil for system monitoring

Google Generative AI (Gemini) for natural language → commands

📜 License
MIT License © 2025 [Your Name]

⭐ Contribute
Pull requests are welcome! If you’d like to add new hacker-style commands or fun mini-games, feel free to fork and submit 🚀

yaml
Copy code

---

Do you want me to also **make a `requirements.txt` file** for your repo so people can install dependencies dir
