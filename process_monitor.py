import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import time
import threading
from queue import Queue

class ProcessMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Process Monitor")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")  # Light gray background
        
        # Queue for thread-safe communication
        self.update_queue = Queue()
        
        # Number of CPU cores
        self.num_cores = psutil.cpu_count()
        
        # Configure grid
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Top Frame (System Info)
        self.top_frame = ttk.Frame(root, padding=10, relief="raised", borderwidth=2)
        self.top_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        # System Info Labels with styling
        self.cpu_label = ttk.Label(self.top_frame, text="CPU: 0%", font=("Helvetica", 12, "bold"), foreground="#2c3e50")
        self.cpu_label.pack(side=tk.LEFT, padx=10)
        
        self.memory_label = ttk.Label(self.top_frame, text="Memory: 0%", font=("Helvetica", 12, "bold"), foreground="#2c3e50")
        self.memory_label.pack(side=tk.LEFT, padx=10)
        
        self.process_count_label = ttk.Label(self.top_frame, text="Processes: 0", font=("Helvetica", 12, "bold"), foreground="#2c3e50")
        self.process_count_label.pack(side=tk.LEFT, padx=10)
        
        # Control Frame (Refresh Rate and Actions)
        self.control_frame = ttk.Frame(root, padding=5)
        self.control_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        ttk.Label(self.control_frame, text="Refresh Rate (s):").pack(side=tk.LEFT, padx=5)
        self.refresh_rate = tk.DoubleVar(value=0.5)
        self.refresh_spinbox = ttk.Spinbox(self.control_frame, from_=0.1, to=5.0, increment=0.1, textvariable=self.refresh_rate, width=5)
        self.refresh_spinbox.pack(side=tk.LEFT, padx=5)
        
        self.terminate_btn = ttk.Button(self.control_frame, text="Terminate Selected", command=self.terminate_process)
        self.terminate_btn.pack(side=tk.RIGHT, padx=5)
        
        # Process Frame
        self.process_frame = ttk.Frame(root, padding=5, relief="sunken", borderwidth=2)
        self.process_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.process_frame.grid_rowconfigure(0, weight=1)
        self.process_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview Style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), foreground="#34495e")
        style.configure("Treeview", background="#ecf0f1", fieldbackground="#ecf0f1", foreground="#2c3e50")
        
        # Process Treeview
        self.tree = ttk.Treeview(self.process_frame, columns=("PID", "Name", "CPU%", "Memory", "Status"), 
                                show="headings", style="Treeview")
        self.tree.heading("PID", text="PID", command=lambda: self.sort_column("PID", False))
        self.tree.heading("Name", text="Process Name", command=lambda: self.sort_column("Name", False))
        self.tree.heading("CPU%", text="CPU %", command=lambda: self.sort_column("CPU%", True))
        self.tree.heading("Memory", text="Memory (MB)", command=lambda: self.sort_column("Memory", True))
        self.tree.heading("Status", text="Status")
        
        # Column widths
        self.tree.column("PID", width=100, anchor="center")
        self.tree.column("Name", width=350, anchor="w")
        self.tree.column("CPU%", width=100, anchor="center")
        self.tree.column("Memory", width=120, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.process_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Thread control
        self.running = True
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
        self.check_updates()
    
    def update_loop(self):
        """Background thread to collect system and process info"""
        while self.running:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status']):
                    try:
                        pinfo = proc.info
                        if pinfo['name'].lower() not in ['system idle process', 'idle']:
                            pinfo['cpu_percent'] = pinfo['cpu_percent'] / self.num_cores
                            processes.append(pinfo)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
                processes = processes[:50]  # Limit to top 50
                
                self.update_queue.put((cpu_percent, memory, processes))
                
                time.sleep(self.refresh_rate.get())
                
            except Exception as e:
                print(f"Error in update thread: {e}")
                time.sleep(1)
    
    def check_updates(self):
        """Main thread to update UI"""
        try:
            while not self.update_queue.empty():
                cpu_percent, memory, processes = self.update_queue.get_nowait()
                
                # Update system info
                self.cpu_label.config(text=f"CPU: {cpu_percent:.1f}% (Cores: {self.num_cores})")
                self.memory_label.config(text=f"Memory: {memory.percent:.1f}% ({memory.used//(1024*1024)} MB / {memory.total//(1024*1024)} MB)")
                self.process_count_label.config(text=f"Processes: {len(processes)}")
                
                # Clear current list
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Populate process list
                for proc in processes:
                    try:
                        memory_mb = proc['memory_info'].rss / (1024 * 1024)
                        self.tree.insert("", "end", values=(
                            proc['pid'],
                            proc['name'],
                            f"{proc['cpu_percent']:.1f}",
                            f"{memory_mb:.1f}",
                            proc['status']
                        ))
                    except (KeyError, AttributeError) as e:
                        print(f"Error processing process data: {e}")
                        continue
                
        except Exception as e:
            print(f"Error updating UI: {e}")
        
        self.root.after(100, self.check_updates)
    
    def sort_column(self, col, reverse):
        """Sort Treeview by column"""
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        # Handle numeric columns
        if col in ("CPU%", "Memory"):
            items.sort(key=lambda x: float(x[0]) if x[0] else 0, reverse=reverse)
        else:
            items.sort(reverse=reverse)
        
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)
        
        # Toggle sort direction on next click
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
    
    def terminate_process(self):
        """Terminate selected process"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a process to terminate.")
            return
        
        pid = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm Termination", f"Are you sure you want to terminate PID {pid}?"):
            try:
                process = psutil.Process(pid)
                process.terminate()
                messagebox.showinfo("Success", f"Process {pid} terminated.")
            except psutil.NoSuchProcess:
                messagebox.showerror("Error", "Process no longer exists.")
            except psutil.AccessDenied:
                messagebox.showerror("Error", "Access denied. Run as Administrator.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to terminate process: {e}")
    
    def __del__(self):
        """Cleanup on window close"""
        self.running = False
        if hasattr(self, 'update_thread'):
            self.update_thread.join(timeout=1)

def main():
    root = tk.Tk()
    app = ProcessMonitor(root)
    root.mainloop()

if __name__ == "__main__":
    main()