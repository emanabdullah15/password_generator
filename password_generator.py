
import tkinter as tk
from tkinter import messagebox
import secrets
import string
import math

# ==================== COLORS ====================
BG = "#0b1020"
PANEL = "#141c30"
FIELD = "#0a1224"
TEXT = "#f3f6ff"
MUTED = "#9ba8c7"
ACCENT = "#8b5cf6"
ACCENT_HOVER = "#7c3aed"
GREEN = "#34d399"
YELLOW = "#fbbf24"
RED = "#fb7185"
BORDER = "#293552"

# ==================== MAIN WINDOW ====================
root = tk.Tk()
root.title("CodeByEman | Password Generator")
root.geometry("760x690")
root.minsize(680, 650)
root.configure(bg=BG)


# ==================== HELPER FUNCTIONS ====================
def make_label(parent, text, size=11, color=TEXT, weight="normal"):
    return tk.Label(
        parent,
        text=text,
        bg=parent.cget("bg"),
        fg=color,
        font=("Segoe UI", size, weight)
    )


def selected_character_sets():
    sets = []

    if uppercase_var.get():
        sets.append(string.ascii_uppercase)

    if lowercase_var.get():
        sets.append(string.ascii_lowercase)

    if numbers_var.get():
        sets.append(string.digits)

    if symbols_var.get():
        sets.append("!@#$%^&*()-_=+[]{};:,.?/")

    return sets


def secure_shuffle(items):
    # Securely shuffle characters
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]

    return items


def generate_password():
    char_sets = selected_character_sets()
    length = length_var.get()

    if not char_sets:
        messagebox.showwarning(
            "Choose an option",
            "Please select at least one character type."
        )
        return

    if length < len(char_sets):
        messagebox.showwarning(
            "Password length too short",
            f"Your selected options need at least "
            f"{len(char_sets)} characters."
        )
        return

    # Select at least one character from each selected group
    password_chars = [
        secrets.choice(char_set)
        for char_set in char_sets
    ]

    all_chars = "".join(char_sets)

    # Fill the remaining password positions
    remaining = length - len(password_chars)

    password_chars.extend(
        secrets.choice(all_chars)
        for _ in range(remaining)
    )

    # Shuffle characters securely
    secure_shuffle(password_chars)

    password = "".join(password_chars)

    password_var.set(password)

    password_entry.config(
        show="" if show_password_var.get() else "•"
    )

    update_strength(password)


def copy_password():
    password = password_var.get()

    if not password:
        messagebox.showinfo(
            "No password",
            "Generate a password first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    copy_button.config(text="✓ Copied!")
    root.after(
        1500,
        lambda: copy_button.config(text="Copy Password")
    )


def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="•")


def update_length_label(value=None):
    length_label.config(
        text=f"{length_var.get()} characters"
    )


def estimate_strength(password):
    # A simple educational strength estimate
    if not password:
        return 0, "Not generated yet", MUTED

    pool_size = 0

    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26

    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26

    if any(c in string.digits for c in password):
        pool_size += 10

    symbol_chars = "!@#$%^&*()-_=+[]{};:,.?/"

    if any(c in symbol_chars for c in password):
        pool_size += len(symbol_chars)

    entropy = len(password) * math.log2(max(pool_size, 1))

    if len(password) < 8 or entropy < 35:
        return 1, "Weak", RED

    elif len(password) < 12 or entropy < 60:
        return 2, "Moderate", YELLOW

    return 3, "Strong", GREEN


def update_strength(password):
    score, label, color = estimate_strength(password)

    strength_text.config(
        text=label,
        fg=color
    )

    strength_canvas.delete("all")

    width = strength_canvas.winfo_width()

    if width < 10:
        width = 250

    strength_canvas.create_rectangle(
        0, 0, width, 8,
        fill=BORDER,
        outline=BORDER
    )

    if score:
        strength_canvas.create_rectangle(
            0, 0, width * score / 3, 8,
            fill=color,
            outline=color
        )


def reset_options():
    length_var.set(16)

    uppercase_var.set(True)
    lowercase_var.set(True)
    numbers_var.set(True)
    symbols_var.set(True)

    show_password_var.set(False)
    password_var.set("")

    password_entry.config(show="•")

    strength_text.config(
        text="Not generated yet",
        fg=MUTED
    )

    strength_canvas.delete("all")

    copy_button.config(text="Copy Password")

    update_length_label()


# ==================== HEADER ====================
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=34, pady=(25, 16))

logo = tk.Label(
    header,
    text="🔐",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI Emoji", 27)
)
logo.pack(side="left", padx=(0, 12))

title_area = tk.Frame(header, bg=BG)
title_area.pack(side="left", fill="x", expand=True)

tk.Label(
    title_area,
    text="Password Generator",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 23, "bold")
).pack(anchor="w")

tk.Label(
    title_area,
    text="Create a strong, random password in seconds.",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(anchor="w", pady=(3, 0))


# ==================== MAIN PANEL ====================
panel = tk.Frame(
    root,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)

panel.pack(
    fill="both",
    expand=True,
    padx=34,
    pady=(0, 18)
)


# ==================== PASSWORD OUTPUT ====================
make_label(
    panel,
    "YOUR PASSWORD",
    10,
    MUTED,
    "bold"
).pack(anchor="w", padx=24, pady=(23, 9))

output_row = tk.Frame(panel, bg=PANEL)
output_row.pack(fill="x", padx=24)

password_var = tk.StringVar()

password_entry = tk.Entry(
    output_row,
    textvariable=password_var,
    state="readonly",
    readonlybackground=FIELD,
    fg=GREEN,
    insertbackground=TEXT,
    font=("Consolas", 15),
    relief="flat",
    bd=0,
    show="•"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=14,
    padx=(0, 10)
)

copy_button = tk.Button(
    output_row,
    text="Copy Password",
    command=copy_password,
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    font=("Segoe UI", 10, "bold"),
    padx=14,
    pady=10
)

copy_button.pack(side="right")


# ==================== SHOW / HIDE ====================
show_password_var = tk.BooleanVar(value=False)

show_check = tk.Checkbutton(
    panel,
    text="Show password",
    variable=show_password_var,
    command=toggle_password,
    bg=PANEL,
    fg=MUTED,
    selectcolor=FIELD,
    activebackground=PANEL,
    activeforeground=TEXT,
    font=("Segoe UI", 9)
)

show_check.pack(anchor="w", padx=22, pady=(7, 2))


# ==================== PASSWORD STRENGTH ====================
strength_row = tk.Frame(panel, bg=PANEL)
strength_row.pack(fill="x", padx=24, pady=(8, 4))

make_label(
    strength_row,
    "Password strength",
    9,
    MUTED
).pack(side="left")

strength_text = tk.Label(
    strength_row,
    text="Not generated yet",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 9, "bold")
)

strength_text.pack(side="right")

strength_canvas = tk.Canvas(
    panel,
    height=8,
    bg=PANEL,
    highlightthickness=0,
    bd=0
)

strength_canvas.pack(
    fill="x",
    padx=24,
    pady=(4, 17)
)

strength_canvas.bind(
    "<Configure>",
    lambda event: update_strength(password_var.get())
)


# ==================== DIVIDER ====================
tk.Frame(
    panel,
    bg=BORDER,
    height=1
).pack(fill="x", padx=24, pady=(0, 16))


# ==================== PASSWORD LENGTH ====================
settings = tk.Frame(panel, bg=PANEL)
settings.pack(fill="x", padx=24)

length_header = tk.Frame(settings, bg=PANEL)
length_header.pack(fill="x")

make_label(
    length_header,
    "PASSWORD LENGTH",
    10,
    MUTED,
    "bold"
).pack(side="left")

length_var = tk.IntVar(value=16)

length_label = tk.Label(
    length_header,
    text="16 characters",
    bg=PANEL,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
)

length_label.pack(side="right")

length_slider = tk.Scale(
    settings,
    from_=4,
    to=64,
    orient="horizontal",
    variable=length_var,
    command=update_length_label,
    bg=PANEL,
    fg=TEXT,
    troughcolor=FIELD,
    activebackground=ACCENT,
    highlightthickness=0,
    bd=0,
    showvalue=False,
    sliderlength=18
)

length_slider.pack(
    fill="x",
    pady=(3, 12)
)


# ==================== CHARACTER OPTIONS ====================
make_label(
    settings,
    "INCLUDE CHARACTER TYPES",
    10,
    MUTED,
    "bold"
).pack(anchor="w", pady=(0, 8))

options_grid = tk.Frame(settings, bg=PANEL)
options_grid.pack(fill="x")

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)


def option_check(parent, text, variable):
    return tk.Checkbutton(
        parent,
        text=text,
        variable=variable,
        bg=PANEL,
        fg=TEXT,
        selectcolor=FIELD,
        activebackground=PANEL,
        activeforeground=TEXT,
        font=("Segoe UI", 10),
        cursor="hand2"
    )


option_check(
    options_grid,
    "Uppercase (A–Z)",
    uppercase_var
).grid(row=0, column=0, sticky="w", padx=(0, 24), pady=3)

option_check(
    options_grid,
    "Lowercase (a–z)",
    lowercase_var
).grid(row=0, column=1, sticky="w", padx=(0, 24), pady=3)

option_check(
    options_grid,
    "Numbers (0–9)",
    numbers_var
).grid(row=1, column=0, sticky="w", padx=(0, 24), pady=3)

option_check(
    options_grid,
    "Symbols (!@#$)",
    symbols_var
).grid(row=1, column=1, sticky="w", padx=(0, 24), pady=3)


# ==================== ACTION BUTTONS ====================
actions = tk.Frame(panel, bg=PANEL)
actions.pack(fill="x", padx=24, pady=(18, 22))

generate_button = tk.Button(
    actions,
    text="✦  Generate Password",
    command=generate_password,
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    font=("Segoe UI", 11, "bold"),
    pady=12
)

generate_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 8)
)

reset_button = tk.Button(
    actions,
    text="Reset",
    command=reset_options,
    bg=FIELD,
    fg=TEXT,
    activebackground=BORDER,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    font=("Segoe UI", 10, "bold"),
    padx=20,
    pady=12
)

reset_button.pack(side="right")


# ==================== FOOTER ====================
footer = tk.Label(
    root,
    text=(
        "CODEBYEMAN  •  Built with Python & Tkinter  •  "
        "Passwords are generated locally"
    ),
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 9)
)

footer.pack(pady=(0, 15))


# ==================== START APPLICATION ====================
root.after(150, generate_password)
root.mainloop()
