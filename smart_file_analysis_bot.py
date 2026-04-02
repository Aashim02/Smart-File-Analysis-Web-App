import os
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


def summarize_text(text: str, sentence_count: int = 2) -> str:
    """Return a short offline summary using the first few sentences."""
    normalized = " ".join(text.split())
    if not normalized:
        return "No content available"

    sentences = [s.strip() for s in normalized.split(".") if s.strip()]
    if not sentences:
        return normalized[:180]

    summary = ". ".join(sentences[:sentence_count])
    if not summary.endswith("."):
        summary += "."
    return summary


def analyze_folder(folder: Path, log_callback) -> Tuple[List[List[str]], int, int]:
    """Scan folder, summarize .txt files, and return rows plus stats."""
    data: List[List[str]] = []
    txt_count = 0
    other_count = 0

    try:
        files = sorted(folder.iterdir(), key=lambda p: p.name.lower())
    except OSError as exc:
        raise RuntimeError(f"Unable to access folder: {exc}") from exc

    for file_path in files:
        if not file_path.is_file():
            other_count += 1
            log_callback(f"Skipped (not a file): {file_path.name}")
            continue

        if file_path.suffix.lower() != ".txt":
            other_count += 1
            log_callback(f"Skipped: {file_path.name}")
            continue

        txt_count += 1
        try:
            content = file_path.read_text(encoding="utf-8")
            summary = summarize_text(content)
            data.append([file_path.name, str(file_path), summary])
            log_callback(f"Processed: {file_path.name}")
        except UnicodeDecodeError:
            log_callback(f"Error reading (not utf-8): {file_path.name}")
        except OSError as exc:
            log_callback(f"Error reading {file_path.name}: {exc}")

    return data, txt_count, other_count


class SmartFileAnalysisBot:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Smart File Analysis Bot")
        self.root.geometry("920x650")
        self.root.configure(bg="#0E1117")

        self.folder_path = tk.StringVar()
        self._build_ui()

    def _build_ui(self) -> None:
        title = tk.Label(
            self.root,
            text="Smart File Analysis Dashboard",
            font=("Segoe UI", 20, "bold"),
            fg="#E6EDF3",
            bg="#0E1117",
        )
        title.pack(pady=(16, 8))

        subtitle = tk.Label(
            self.root,
            text="Analyze .txt files, summarize content, export Excel, and view stats",
            font=("Segoe UI", 10),
            fg="#8B949E",
            bg="#0E1117",
        )
        subtitle.pack(pady=(0, 14))

        controls = tk.Frame(self.root, bg="#0E1117")
        controls.pack(pady=6)

        self.path_entry = tk.Entry(
            controls,
            textvariable=self.folder_path,
            width=72,
            bg="#161B22",
            fg="#E6EDF3",
            insertbackground="#E6EDF3",
            relief=tk.FLAT,
            font=("Consolas", 10),
        )
        self.path_entry.grid(row=0, column=0, padx=(0, 10), ipady=7)

        browse_btn = tk.Button(
            controls,
            text="Browse",
            command=self.select_folder,
            bg="#1F6FEB",
            fg="#FFFFFF",
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=6,
            activebackground="#388BFD",
            activeforeground="#FFFFFF",
        )
        browse_btn.grid(row=0, column=1)

        action_row = tk.Frame(self.root, bg="#0E1117")
        action_row.pack(pady=12)

        run_btn = tk.Button(
            action_row,
            text="Analyze Files",
            command=self.process_files,
            bg="#238636",
            fg="#FFFFFF",
            relief=tk.FLAT,
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=8,
            activebackground="#2EA043",
            activeforeground="#FFFFFF",
        )
        run_btn.grid(row=0, column=0, padx=6)

        clear_btn = tk.Button(
            action_row,
            text="Clear Logs",
            command=self.clear_logs,
            bg="#30363D",
            fg="#E6EDF3",
            relief=tk.FLAT,
            font=("Segoe UI", 11),
            padx=16,
            pady=8,
            activebackground="#484F58",
            activeforeground="#FFFFFF",
        )
        clear_btn.grid(row=0, column=1, padx=6)

        self.output_box = scrolledtext.ScrolledText(
            self.root,
            width=112,
            height=28,
            bg="#010409",
            fg="#7EE787",
            insertbackground="#E6EDF3",
            font=("Consolas", 10),
            relief=tk.FLAT,
            padx=10,
            pady=8,
        )
        self.output_box.pack(padx=18, pady=(8, 14), fill=tk.BOTH, expand=True)

    def log(self, message: str) -> None:
        self.output_box.insert(tk.END, message + "\n")
        self.output_box.see(tk.END)
        self.root.update_idletasks()

    def clear_logs(self) -> None:
        self.output_box.delete("1.0", tk.END)

    def select_folder(self) -> None:
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.log(f"Selected Folder: {folder}")

    def process_files(self) -> None:
        folder_text = self.folder_path.get().strip().strip('"').strip("'")
        if not folder_text:
            messagebox.showerror("Missing Folder", "Please select a folder first.")
            return

        folder = Path(folder_text)
        if not folder.is_dir():
            messagebox.showerror("Invalid Folder", "Selected path is not a folder.")
            return

        self.log("\nProcessing started...\n")

        try:
            data, txt_count, other_count = analyze_folder(folder, self.log)
        except RuntimeError as exc:
            messagebox.showerror("Folder Error", str(exc))
            self.log(str(exc))
            return

        if data:
            df = pd.DataFrame(data, columns=["File Name", "File Path", "Summary"])
            output_file = folder / "output.xlsx"
            try:
                df.to_excel(output_file, index=False)
                self.log("\nExcel created successfully")
                self.log(f"Output: {output_file}")
                self.show_output_options(output_file)
            except Exception as exc:  # noqa: BLE001
                messagebox.showerror("Export Error", f"Failed to write Excel: {exc}")
                self.log(f"Export failed: {exc}")
                return
        else:
            self.log("No .txt files were summarized.")

        self.log(f"\nSummary: txt={txt_count}, other={other_count}")
        self.show_graph(txt_count, other_count)

    def show_output_options(self, output_file: Path) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Excel Output Ready")
        dialog.configure(bg="#0E1117")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        msg = tk.Label(
            dialog,
            text=f"Excel file created:\n{output_file}",
            bg="#0E1117",
            fg="#E6EDF3",
            justify=tk.LEFT,
            font=("Segoe UI", 10),
            padx=18,
            pady=14,
        )
        msg.pack()

        btn_row = tk.Frame(dialog, bg="#0E1117")
        btn_row.pack(pady=(0, 14))

        save_btn = tk.Button(
            btn_row,
            text="Save As",
            command=lambda: self.save_output_as(output_file, dialog),
            bg="#1F6FEB",
            fg="#FFFFFF",
            relief=tk.FLAT,
            padx=12,
            pady=6,
        )
        save_btn.grid(row=0, column=0, padx=6)

        open_btn = tk.Button(
            btn_row,
            text="Open",
            command=lambda: self.open_output_file(output_file, dialog),
            bg="#238636",
            fg="#FFFFFF",
            relief=tk.FLAT,
            padx=12,
            pady=6,
        )
        open_btn.grid(row=0, column=1, padx=6)

        close_btn = tk.Button(
            btn_row,
            text="Close",
            command=dialog.destroy,
            bg="#30363D",
            fg="#E6EDF3",
            relief=tk.FLAT,
            padx=12,
            pady=6,
        )
        close_btn.grid(row=0, column=2, padx=6)

    def save_output_as(self, output_file: Path, dialog: tk.Toplevel) -> None:
        save_path = filedialog.asksaveasfilename(
            title="Save Excel File As",
            defaultextension=".xlsx",
            initialfile=output_file.name,
            filetypes=[("Excel files", "*.xlsx")],
        )
        if not save_path:
            return

        try:
            source_bytes = output_file.read_bytes()
            Path(save_path).write_bytes(source_bytes)
            self.log(f"Saved copy: {save_path}")
            messagebox.showinfo("Saved", f"File saved as:\n{save_path}")
            dialog.destroy()
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Save Error", f"Could not save file: {exc}")

    def open_output_file(self, output_file: Path, dialog: tk.Toplevel) -> None:
        try:
            os.startfile(str(output_file))
            self.log(f"Opened file: {output_file}")
            dialog.destroy()
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Open Error", f"Could not open file: {exc}")

    def show_graph(self, txt_count: int, other_count: int) -> None:
        labels = ["TXT Files", "Other Files"]
        values = [txt_count, other_count]
        colors = ["#2EA043", "#8B949E"]

        plt.figure(figsize=(7, 4.5), facecolor="#0E1117")
        axis = plt.gca()
        axis.set_facecolor("#0E1117")
        bars = plt.bar(labels, values, color=colors)

        plt.title("File Analysis", color="#E6EDF3", fontsize=14, weight="bold")
        plt.xlabel("File Type", color="#C9D1D9")
        plt.ylabel("Count", color="#C9D1D9")
        plt.xticks(color="#C9D1D9")
        plt.yticks(color="#C9D1D9")

        for bar, value in zip(bars, values):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                str(value),
                ha="center",
                va="bottom",
                color="#E6EDF3",
                fontsize=10,
            )

        plt.tight_layout()
        plt.show()


def main() -> None:
    root = tk.Tk()
    app = SmartFileAnalysisBot(root)

    default_data_folder = Path(__file__).resolve().parent / "data"
    if default_data_folder.is_dir():
        app.folder_path.set(str(default_data_folder))
        app.log(f"Default folder loaded: {default_data_folder}")

    root.mainloop()


if __name__ == "__main__":
    main()
