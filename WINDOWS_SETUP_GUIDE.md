# Claude Code CLI - Windows Installation Guide

This guide walks you through installing Claude Code CLI on Windows, step by step.
No technical experience required!

---

## Before You Start

Make sure you have:

- **Windows 10 or Windows 11** (your computer must have one of these)
  - To check: press the `Windows` key, type `winver`, and press Enter
- **A stable internet connection**
- **A Claude account** (Pro, Max, Teams, or Enterprise plan)
  - Free accounts cannot use Claude Code
  - Sign up at [claude.ai](https://claude.ai) if you need one

---

## Step 1 — Install Git for Windows

Git is a required tool that Claude Code needs to work. You only need to install it once.

1. Open your web browser and go to: **https://git-scm.com/downloads/win**
2. Click the large **Download** button
3. Open the downloaded file (named something like `Git-2.x.x-64-bit.exe`)
4. Click **Next** on every screen — the default settings are fine
5. Click **Finish** when the installer is done

---

## Step 2 — Open PowerShell as Administrator

PowerShell is a built-in Windows program used to run commands.

1. Press the **Windows key** on your keyboard
2. Type `PowerShell`
3. Right-click on **Windows PowerShell** in the results
4. Select **Run as administrator**
5. Click **Yes** if a pop-up asks for permission

A blue window will open. This is PowerShell.

> **Important:** Use PowerShell, not "Command Prompt". They look similar but are different programs.

---

## Step 3 — Install Claude Code

In the PowerShell window, copy and paste the following line exactly as written:

```
irm https://claude.ai/install.ps1 | iex
```

Then press **Enter**.

The installer will run automatically. This may take 1–5 minutes. When it is done, you will see a message saying **Claude Code installed successfully**.

---

## Step 4 — Confirm the Installation Worked

1. Close the PowerShell window (type `exit` and press Enter, or just close it)
2. Open a **new** PowerShell window (repeat Step 2, but you do not need "Run as administrator" this time)
3. Type the following and press Enter:

```
claude --version
```

If you see a version number (for example, `1.2.3`), the installation was successful!

---

## Step 5 — Log In to Your Claude Account

1. In PowerShell, type `claude` and press **Enter**
2. Your web browser will open automatically
3. Sign in with your Claude email address and password
4. Click **Allow** when asked for permissions
5. Return to PowerShell — you are now ready to use Claude Code!

---

## Using Claude Code

Once installed, here is how to start using it:

1. Open **PowerShell**
2. Navigate to your project folder. For example:
   ```
   cd C:\Users\YourName\Documents\MyProject
   ```
   Replace `YourName` and `MyProject` with your actual folder names.
3. Type `claude` and press Enter
4. Start chatting with Claude about your code!

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `claude` is not recognized after install | Close PowerShell and open a fresh window |
| `irm` is not recognized | You are in Command Prompt, not PowerShell. Open PowerShell instead. |
| Installation fails with a network error | Check your internet connection, temporarily disable any VPN, then try again |
| Browser does not open for login | Try typing `claude` again in PowerShell |

---

## Need More Help?

Visit the official Claude Code documentation at: **https://docs.anthropic.com/en/docs/claude-code**
