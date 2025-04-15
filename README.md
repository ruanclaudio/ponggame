# 🏓 Pong Multiplayer — Python Project

A simple **multiplayer Pong game** built using Python, `pygame` and sockets. Challenge your friends in this classic game!

---

## 💻 Requirements

- Python 3.10+ recommended  
- `pygame`  
- `socket` (standard lib)  
- `pickle` (standard lib)

You can install all dependencies using the provided `requirements.txt`.

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/your-pong-project.git
cd your-pong-project
```

### 2️⃣ Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```
### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
### 4️⃣ Start the Server

In one terminal, run:

```bash
python server.py
```
The server will wait until two players connect and send READY. The game will start automatically!

###5️⃣ Start the Clients

In two separate terminals (or machines), run:

```bash
python client.py
```

The program will prompt for the server IP:

Enter the server IP:

Type the server's IP and hit Enter.

When asked, type:

ready

When both players are ready, the game begins!
🎮 Controls

    ↑ Arrow Up — Move paddle up

    ↓ Arrow Down — Move paddle down

⚠️ Notes

    Make sure port 5555 is open on the server.

    Both players must be on the same network or the server must allow external connections.

📦 Saving Dependencies

To save dependencies after adding new ones:

pip freeze > requirements.txt

💡 Contribution

Pull requests are welcome! Feel free to fork and improve this project.
🏆 License

This project is open-source — feel free to modify and share!
MIT License


---
