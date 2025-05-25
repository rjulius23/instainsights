# Hiker Instagram Insights

A lightweight, Tkinter-based desktop app that lets you:

* 🔍 **Look up** any public Instagram profile and view  
  **followers · following · media · public email · verified badge**  
* 📄 **Export bulk stats to CSV** by pasting a list of usernames  
* 🛠 Built with SOLID principles, type-hinted code, and unit-tested components

---

## ✨ Features

| Feature | Details |
|---------|---------|
| **Instant lookup** | Enter a single username, click **Fetch**, and see live stats. |
| **Batch export** | Paste a comma- or newline-separated list, choose a save path, hit **Export CSV**. |
| **Responsive UI** | Network calls run in background threads so the window never freezes. |
| **Clean architecture** | Services, exporters, and GUI are separated for easy maintenance. |
| **Test coverage** | Pytest suites mock HikerAPI responses to verify logic. |

---

## 🏗 Project layout

```

instainsights/
├─ **main**.py         # CLI entry (parses --api\_key)
├─ src/
  ├─ presentation/     # Tkinter UI layer
  ├─ infrastructure/              
     ├─ api/           # HikerAPI wrapper
     ├─ export/        # CSV writer
  ├─ domain/           # Typed dataclasses
├─ tests/              # Unit tests
├─ requirements.txt
├─ Makefile            # Scripting entry point (like make tests.. etc)
└─ README.md

````

---

## 🚀 Quick start

### 1. Clone & install

```bash
git clone https://github.com/rjulius23/instainsights.git
cd instainsights
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
````

### 2. Run the app

```bash
python3 main.py --api_key YOUR_HIKERAPI_KEY
```

*`--api_key` (or `-k`) is **required** – get one from your HikerAPI dashboard.*

### 3. Run tests

```bash
python3 -m pytest tests
```

---

## 📝 CSV format

The exported file contains:

```
username,follower_count,following_count,posts_count,public_email,is_verified
messi,431000000,300,1240,,true
...
```

---

## 🤝 Contributing

1. Fork / branch from `main`.
2. Follow existing code style (`ruff` + `black`).
3. Add/adjust unit tests for any change.
4. Open a pull request describing **why** the change helps.

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 🙏 Credits

* [HikerAPI](https://hikerapi.example.com) – unofficial Instagram data
* Python standard library (Tkinter, csv, argparse, etc.)
