import os
import psutil
import google.generativeai as genai
import random
import json
import time
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

console = Console()

API_KEY = "YOUR_API_KEY"  # replace with your Gemini API key
genai.configure(api_key=API_KEY)

PROFILE_FILE = "profile.json"

# ---------------- Persistent Profile ----------------
def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    return {"xp": 0, "level": 1, "missions": {}, "completed": []}


def save_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=2)


profile = load_profile()
XP_THRESHOLD = 50


# ---------------- Gamification ----------------
def add_xp(points=10):
    """Add XP, handle leveling up & random power-ups."""
    profile["xp"] += points
    leveled_up = False

    # Level up check
    if profile["xp"] >= XP_THRESHOLD * profile["level"]:
        profile["level"] += 1
        leveled_up = True
        ascii_banner = f"""
███████╗██╗   ██╗██╗     ██╗     ███████╗██╗   ██╗██████╗ 
██╔════╝╚██╗ ██╔╝██║     ██║     ██╔════╝██║   ██║██╔══██╗
█████╗   ╚████╔╝ ██║     ██║     █████╗  ██║   ██║██████╔╝
██╔══╝    ╚██╔╝  ██║     ██║     ██╔══╝  ██║   ██║██╔═══╝ 
███████╗   ██║   ███████╗███████╗███████╗╚██████╔╝██║     
╚══════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     
                LEVEL {profile["level"]}
"""
        console.print(Panel(ascii_banner, style="bold green"))

    # Random power-up
    if random.random() < 0.1:
        bonus = random.randint(5, 20)
        profile["xp"] += bonus
        console.print(f"💎 [bold cyan]Lucky Power-Up![/bold cyan] +{bonus} XP")

    save_profile(profile)
    show_xp_bar()
    if leveled_up:
        show_mission()


def show_xp_bar():
    """Display XP progress bar."""
    with Progress(transient=True) as progress:
        task = progress.add_task(
            f"🎮 XP: {profile['xp']}/{XP_THRESHOLD * profile['level']} (Level {profile['level']})",
            total=XP_THRESHOLD * profile["level"],
        )
        progress.update(task, completed=min(profile["xp"], XP_THRESHOLD * profile["level"]))


# ---------------- Missions ----------------
def generate_mission():
    """Generate a daily mission."""
    all_cmds = ["ls", "cpu", "mem", "fortune", "cat"]
    cmd = random.choice(all_cmds)
    count = random.randint(2, 4)
    profile["missions"] = {"command": cmd, "goal": count, "progress": 0}
    save_profile(profile)


def show_mission():
    """Show current mission."""
    if not profile["missions"]:
        generate_mission()
    m = profile["missions"]
    console.print(
        f"🎯 Mission: Use [bold yellow]{m['command']}[/bold yellow] {m['goal']} times "
        f"([green]{m['progress']}[/green]/{m['goal']})"
    )


def update_mission(cmd):
    if profile["missions"] and cmd == profile["missions"]["command"]:
        profile["missions"]["progress"] += 1
        if profile["missions"]["progress"] >= profile["missions"]["goal"]:
            console.print("🏆 [bold green]Mission Complete![/bold green] +30 XP")
            add_xp(30)
            profile["completed"].append(profile["missions"])
            profile["missions"] = {}
        save_profile(profile)


# ---------------- Autocomplete ----------------
COMMANDS = [
    "pwd", "ls", "cd", "mkdir", "rm", "cpu", "mem", "ps",
    "ai", "fortune", "cat", "help", "exit",
    "matrix", "scan", "whoami", "guess"
]
command_completer = WordCompleter(COMMANDS, ignore_case=True)


def get_input(cwd):
    """Prompt input with autocomplete."""
    return prompt(f"[{cwd}] > ", completer=command_completer)


# ---------------- AI Translator ----------------
def translate_to_command(natural_language_query):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt_text = f"""
        Translate into terminal commands (no explanations).
        Allowed: ls, cd, pwd, mkdir, rm, cpu, mem, ps, fortune, cat.
        Query: "{natural_language_query}"
        """
        response = model.generate_content(prompt_text)
        return response.text.strip()
    except Exception as e:
        return f"ERROR: AI model failed - {e}"


# ---------------- Fun Commands ----------------
def matrix_effect():
    chars = "01"
    console.print("[bold green]Press Ctrl+C to stop Matrix[/bold green]")
    try:
        while True:
            console.print("".join(random.choice(chars) for _ in range(60)), style="green")
            time.sleep(0.05)
    except KeyboardInterrupt:
        console.print("[red]Matrix stopped.[/red]")


def fake_scan():
    ports = [22, 80, 443, 3306, 8080]
    console.print("[bold cyan]🔍 Scanning localhost...[/bold cyan]")
    for p in ports:
        time.sleep(0.5)
        status = random.choice(["open", "closed"])
        console.print(f"Port {p}: {status}")


def whoami_fun():
    identities = [
        "Anonymous Coder 👾",
        "Digital Nomad 🌍",
        "Cyber Wizard 🔮",
        "Python Ninja 🐍",
        "Agent 404: Identity Not Found ❌",
    ]
    console.print(f"👤 You are: [bold magenta]{random.choice(identities)}[/bold magenta]")


def guess_game():
    number = random.randint(1, 10)
    console.print("🎲 Guess a number between 1 and 10")
    for _ in range(3):
        try:
            guess = int(prompt("Your guess: "))
            if guess == number:
                console.print("[bold green]Correct![/bold green] +20 XP")
                add_xp(20)
                return
            else:
                console.print("❌ Wrong!")
        except ValueError:
            console.print("[red]Enter a valid number![/red]")
    console.print(f"💡 The number was {number}")


# ---------------- Command Executor ----------------
def execute_command(user_input):
    parts = user_input.split()
    if not parts:
        return

    command = parts[0]
    args = parts[1:]

    # --- AI Command ---
    if command == "ai":
        query = " ".join(args)
        if not query:
            console.print("[red]ai: Please provide a query.[/red]")
            return
        with console.status(f"🤖 Thinking: '{query}'...", spinner="dots"):
            ai_commands = translate_to_command(query)
        if ai_commands.startswith("ERROR:"):
            console.print(f"[red]AI Error:[/red] {ai_commands}")
            return
        console.print(f"🤖 Executing:\n{ai_commands}")
        for cmd in ai_commands.split("\n"):
            if cmd.strip():
                execute_command(cmd.strip())
        return

    # --- Fun Extras ---
    if command == "matrix":
        matrix_effect()
        return
    if command == "scan":
        fake_scan()
        return
    if command == "whoami":
        whoami_fun()
        return
    if command == "guess":
        guess_game()
        return

    # --- Help ---
    if command == "help":
        console.print("""
[bold cyan]Available Commands:[/bold cyan]
📁 ls, cd, pwd, mkdir, rm
🖥️ cpu, mem, ps
🧠 ai "<query>" (natural language → command)
🍀 fortune
📜 cat <file>
🎲 guess        → Play a mini game
👤 whoami       → Random hacker identity
🔍 scan         → Fake port scan
💻 matrix       → Matrix falling code
❓ help         → Show this menu
🚪 exit         → Exit terminal
        """)
        return

    # --- Fortune ---
    if command == "fortune":
        quotes = [
            "Keep pushing, you're closer than you think!",
            "Debugging is twice as hard as writing the code in the first place.",
            "Stay curious, stay foolish. 🚀",
            "Code is like humor. When you have to explain it, it’s bad.",
        ]
        console.print(f"🍀 {random.choice(quotes)}")
        add_xp(5)
        return

    # --- File Commands ---
    if command == "pwd":
        console.print(os.getcwd())
        add_xp()
        update_mission("pwd")
    elif command == "ls":
        path = args[0] if args else "."
        try:
            for entry in os.listdir(path):
                if os.path.isdir(os.path.join(path, entry)):
                    console.print(f"[blue]📁 {entry}/[/blue]")
                else:
                    console.print(f"📄 {entry}")
            add_xp()
            update_mission("ls")
        except FileNotFoundError:
            console.print(f"[red]ls: No such directory: {path}")
    elif command == "cd":
        path = args[0] if args else os.path.expanduser("~")
        try:
            os.chdir(path)
            add_xp()
            update_mission("cd")
        except FileNotFoundError:
            console.print(f"[red]cd: No such directory: {path}")
    elif command == "mkdir":
        if not args:
            console.print("[red]mkdir: missing operand[/red]")
        else:
            try:
                os.makedirs(args[0], exist_ok=True)
                add_xp()
                update_mission("mkdir")
            except Exception as e:
                console.print(f"[red]mkdir: {e}[/red]")
    elif command == "rm":
        if not args:
            console.print("[red]rm: missing operand[/red]")
        else:
            path = args[0]
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    console.print(f"Removed file: {path}")
                elif os.path.isdir(path):
                    os.rmdir(path)
                    console.print(f"Removed dir: {path}")
                else:
                    console.print(f"[red]rm: No such file or dir: {path}")
                add_xp()
                update_mission("rm")
            except OSError as e:
                console.print(f"[red]rm: {e.strerror}[/red]")

    # --- System Commands ---
    elif command == "cpu":
        console.print(f"CPU Usage: [green]{psutil.cpu_percent(interval=1)}%[/green]")
        add_xp()
        update_mission("cpu")
    elif command == "mem":
        memory = psutil.virtual_memory()
        console.print(f"Total: {memory.total / (1024**3):.2f} GB")
        console.print(f"Used: {memory.used / (1024**3):.2f} GB ({memory.percent}%)")
        add_xp()
        update_mission("mem")
    elif command == "ps":
        table = Table(title="Running Processes")
        table.add_column("PID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("CPU %", style="green")
        for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
            try:
                table.add_row(str(proc.info["pid"]), proc.info["name"], f"{proc.info['cpu_percent']:.1f}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        console.print(table)
        add_xp()
        update_mission("ps")

    # --- Cat ---
    elif command == "cat":
        if not args:
            console.print("[red]cat: missing file operand[/red]")
        else:
            try:
                with open(args[0], "r") as f:
                    console.print(f.read())
                add_xp()
                update_mission("cat")
            except Exception as e:
                console.print(f"[red]cat: cannot read file '{args[0]}': {e}[/red]")

    else:
        console.print(f"[red]Error: Unknown command '{command}'[/red]")


# ---------------- Main Loop ----------------
def main():
    console.print("[bold green]Welcome to the Hacker Gamified Terminal![/bold green] 🚀")
    show_mission()
    while True:
        user_input = get_input(os.getcwd())
        if user_input.lower() == "exit":
            console.print("👋 Goodbye, Hacker!")
            save_profile(profile)
            break
        execute_command(user_input)


if __name__ == "__main__":
    main()
