# aitalk_sql_assistant/core/exporter.py

import json
import time
import csv
from tkinter import filedialog, messagebox
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak

def export_history_to_file(history):
    # This function remains the same
    if not history:
        messagebox.showinfo("Export", "No history to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("JSON files", "*.json")], title="Save History As")
    if not file_path: return
    try:
        if file_path.lower().endswith(".json"):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                for item in history:
                    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get("ts", 0)))
                    f.write(f"[{ts}] {item.get('query')}\n")
        messagebox.showinfo("Export", f"History exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))

# --- NEW FUNCTION for CSV Export ---
def export_data_to_csv(tree):
    """Exports the data from a Treeview widget to a CSV file."""
    cols = tree["columns"]
    if not cols or not tree.get_children():
        messagebox.showinfo("Export", "No data to export.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")], title="Save Results as CSV")
    if not file_path: return

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(cols)
            # Write data rows
            for row_id in tree.get_children():
                row = tree.item(row_id)['values']
                writer.writerow(row)
        messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))

# --- UPDATED FUNCTION for better PDF Tables ---
def export_data_to_pdf(tree):
    """Exports the data from a Treeview widget to a PDF with a proper table."""
    cols = tree["columns"]
    if not cols or not tree.get_children():
        messagebox.showinfo("Export", "No data to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Save Results as PDF")
    if not file_path: return
    
    try:
        data = [cols] # Start with the header row
        for row_id in tree.get_children():
            row = tree.item(row_id)['values']
            data.append([str(v) for v in row])

        doc = SimpleDocTemplate(file_path, pagesize=landscape(letter))
        
        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])
        table.setStyle(style)

        doc.build([table])
        messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))
