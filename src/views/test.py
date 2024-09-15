import sys
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime

# Create a custom widget for the plot
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super().__init__(fig)
        self.setParent(parent)

    def plot_data(self, data):
        timestamps, y_values = zip(*data)  # Unpack the data into two lists (timestamps, y-values)

        # Convert string timestamps to datetime objects
        x_values = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

        # Clear the previous plot
        self.ax.clear()

        # Plot the data
        self.ax.plot(x_values, y_values, label="Data from DB")

        # Format the x-axis for dates
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())

        # Rotate x-axis labels to avoid overlap
        self.ax.tick_params(axis='x', rotation=45)

        self.ax.set_title('Data Plot')
        self.ax.set_xlabel('Timestamp')
        self.ax.set_ylabel('Values')
        self.ax.legend()

        self.draw()  # Update the plot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Plot Example")
        self.setGeometry(100, 100, 800, 600)

        # Create main layout and central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create and add the plot canvas
        self.plot_canvas = PlotCanvas(self)
        layout.addWidget(self.plot_canvas)

        # Retrieve and plot data
        self.plot_from_database()

    def plot_from_database(self):
        # Connect to the database
        conn = sqlite3.connect('../db/sensors.db')
        cursor = conn.cursor()

        # Query data (assume the table has 'timestamp' and 'value' columns)
        cursor.execute("SELECT timestamp, temperature FROM fishtank_data")
        data = cursor.fetchall()

        # Close the connection
        conn.close()

        # Plot the data
        self.plot_canvas.plot_data(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
