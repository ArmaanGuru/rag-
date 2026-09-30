import tkinter as tk
from tkinter import ttk
import threading  # 🟢 NEW
from llm import ask_question


# ------------------ FUNCTIONS ------------------

def submit_query():
    query = entry.get()
    
    if not query.strip():
        return
    
    # Disable button while processing
    submit_btn.config(state="disabled")

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Thinking...\n")

    # Run in background thread (prevents UI freeze)
    threading.Thread(target=process_query, args=(query,)).start()


def process_query(query):
    try:
        response = ask_question(query)

        # Update UI safely from main thread
        output_box.after(0, lambda: update_output(response))

    except Exception as e:
        output_box.after(0, lambda: update_output(f"Error: {str(e)}"))


def update_output(text):
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)

    # Re-enable button
    submit_btn.config(state="normal")


# ------------------ WINDOW ------------------

root = tk.Tk()
root.title("Agentic RAG Assistant 🇮🇳")  # 🔴 CHANGED TITLE
root.geometry("800x600")
root.configure(bg="#1e1e2f")


# ------------------ STYLE ------------------

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Arial", 12, "bold"),
    padding=10,
    background="#4CAF50",
    foreground="white"
)

style.map(
    "TButton",
    background=[("active", "#45a049")]
)


# ------------------ TITLE ------------------

title = tk.Label(
    root,
    text="Agentic RAG Assistant 🇮🇳",
    font=("Helvetica", 18, "bold"),
    bg="#1e1e2f",
    fg="white"
)
title.pack(pady=10)


# ------------------ INPUT FRAME ------------------

frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=10)

entry = tk.Entry(
    frame,
    width=60,
    font=("Arial", 14),
    bg="#2b2b3c",
    fg="white",
    insertbackground="white",
    relief="flat"
)
entry.grid(row=0, column=0, padx=10)

# 🟢 NEW: Press Enter to submit
entry.bind("<Return>", lambda event: submit_query())

submit_btn = ttk.Button(
    frame,
    text="Ask",
    command=submit_query
)
submit_btn.grid(row=0, column=1)


# ------------------ OUTPUT BOX ------------------

output_box = tk.Text(
    root,
    height=20,
    width=90,
    font=("Consolas", 12),
    bg="#2b2b3c",
    fg="white",
    insertbackground="white",
    wrap="word",
    relief="flat"
)
output_box.pack(pady=10, padx=10)


# ------------------ RUN ------------------

root.mainloop()