# Real-Time Process Monitor

A Python-based process monitoring application that provides real-time information about system processes, CPU usage, and memory consumption. Built with Tkinter for the GUI and psutil for system monitoring.

## Features

- **Real-time System Monitoring**
  - Total CPU usage and availability
  - System memory usage with available memory indicator
  - Auto-refreshing display (updates every 0.5 seconds)
  - Visual CPU and memory usage graphs

- **Process Information**
  - Process ID (PID)
  - Process name
  - CPU usage percentage (normalized across all cores)
  - Memory usage 
  - Auto-sorting by any column (PID, Name, CPU%, Memory)
  - Process filtering and search functionality

- **Visualization**
  - Real-time CPU usage graphs
  - Historical CPU trends (last 60 seconds)
  - Top 50 processes CPU usage tracking
  - Color-coded process identification for better clarity

- **User Interface**
  - Clean, modern dark interface
  - Tabbed interface for processes and visualizations
  - Interactive progress bars for CPU and memory usage
  - Sortable columns with click headers
  - Scrollable process list with proper sizing
  - Column separators for better readability
  - Bold headers and proper alignment

## Requirements

- Python 3.6 or higher
- psutil library
- matplotlib library
- numpy library
- tkinter (comes pre-installed with Python)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Real-Time-Process-Monitor.git
   cd Real-Time-Process-Monitor
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the program:
```bash
python process_monitor.py
```

The application will open with the following features:
- **Processes Tab**: View and manage running processes
  - System information at the top (CPU and memory usage with progress bars)
  - Search bar for filtering processes by name or PID
  - Scrollable list of processes with detailed information
  - Sortable columns for PID, Name, CPU%, and Memory
  - Auto-updating process list with real-time data

- **Visualization Tab**: View real-time CPU usage graphs
  - Overall system CPU utilization over time
  - Top 5 processes CPU usage tracking
  - Color-coded process identification for better visualization

## Advanced Features

- **Process Filtering and Sorting**:
  - Search for processes by name or PID
  - Sort processes by any column (PID, Name, CPU%, Memory) with ascending/descending order

- **Real-time Visualization**:
  - Smooth updates for CPU usage and top processes
  - Historical data tracking for the last 60 seconds
  - Interactive and responsive graphs with color-coded lines

- **Performance Optimizations**:
  - Efficient UI updates to reduce overhead
  - Smart data collection to minimize system impact
  - Throttled updates for better responsiveness

## Notes

- The CPU usage shown for each process is normalized across all CPU cores.
- System idle processes are filtered out for clarity.
- Some process information might not be available due to system permissions.
- The application requires appropriate system permissions to access process information.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
