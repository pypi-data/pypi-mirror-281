import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import queue
from .interface_core import serial_interface
from .connect import port_manager

import logging
from .log_init import log_init

class Application(ctk.CTk):
    """
    A Example tkinter application for serial communication.

    Attributes
    ----------
    interface : serial_interface
        The interface to interact with the serial port.
    left_frame : CTkFrame
        The Left Frame of the application.
    right_frame : CTkFrame
        The Right Frame of the application.
    entry_text : CTkStringVar
        The String variable linked to the data entry.
    data_entry : CTkEntry
        The entry field for the command.
    send_button : CTkButton
        The button to send the command.
    data_text : CTkText
        The textbox to display sent and received messages. Incoming data from the serial interface and the sent commands will be displayed in this field.
    figure : Figure
        The Figure object for the plot in the right frame. This object is what actually contains the graphical representation of the data.
    plot : AxesSubplot
        The subplot in the figure. This is where the data from the serial interface gets plotted.
    canvas : FigureCanvasTkAgg
        The canvas on which the figure is drawn. This is a tkinter-compatible canvas that the Figure object draws onto.
    """

    def __init__(self, interface, plotting : bool = True):
        """Initialize the Application."""
        super().__init__()
        self.interface = interface

        ctk.set_appearance_mode("Dark")

        self.left_frame = ctk.CTkFrame(self)
        self.right_frame = ctk.CTkFrame(self)

        self.left_frame.grid(row=0, column=0, sticky='ns')
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        self.entry_text = ctk.StringVar()
        self.data_entry = ctk.CTkEntry(self.left_frame, textvariable=self.entry_text)
        self.data_entry.pack(side=ctk.TOP, fill=ctk.X)
        self.data_entry.bind('<Return>', lambda event: self.send_command())

        self.send_button = ctk.CTkButton(self.left_frame, text="Send", command=self.send_command)
        self.send_button.pack(side=ctk.TOP, fill=ctk.X)

        self.data_text = ctk.CTkTextbox(self.left_frame, height=10, width=50)
        self.data_text.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        self.plotting = plotting

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.figure, self.right_frame)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)
        self.data_list = []
        self.plot_queue = queue.Queue()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        self.rxd_update()

    def send_command(self):
        """
        Fetch the command, send it via the serial interface and update the textbox.
        Clear the command entry field after sending the command.
        This function is connected to the 'Send' button and the 'Return' key while typing into the data_entry field.
        """
        command = self.entry_text.get()
        if self.interface.format == 'STR':        
            self.data_text.insert(0., "TXD: " + command + "\n")
        elif self.interface.format == 'HEX':
            try:
                _ = bytes.fromhex(command)
            except ValueError:
                print('\'' + command + '\' includes non-hexadecimal number')
                self.data_text.insert(0., 'ERR: non-hex cmd')
                self.entry_text.set("")
                return
            self.data_text.insert(0., "TXD: 0x" + command + "\n")
        self.interface.write_to_port(command)
        self.entry_text.set("")

    def rxd_update(self):
        """
        Update the plot with the data from the interface. 
        This function re-plots the data from the serial interface, then schedules itself to be called again after 100 ms.
        This function is automatically triggered in the initialization of the Application class, implementing a regular update of the plot.
        """
        data_queue_size = self.interface.data_queue.qsize()
        if data_queue_size > 0:
            self.plot.clear()
            self.data_list = []  # Clear data_list in every iteration of update_plot

            for _ in range(data_queue_size):
                data_dict = self.interface.data_queue.get()

                if self.interface.format == 'HEX':
                    self.data_text.insert(0., "RXD: 0x" + data_dict['data'].hex() + "\n")
                elif self.interface.format == 'STR':
                    data_dict['data'] = data_dict['data'].strip()
                    if data_dict['data'].strip().isdigit() and self.plotting:
                        self.plot_queue.put(data_dict) # pass down numbers to plot_queue
                    else:
                        self.data_text.insert(0., data_dict['data'] + "\n")

            plot_queue_size = self.plot_queue.qsize()
            for _ in range(plot_queue_size):
                data_dict = self.plot_queue.get()
                self.data_list.append(float(data_dict['data']))  # Store individual data-points
                self.plot_queue.put(data_dict)
            
            # Outside of the loop, plot the entire data_list
            self.plot.plot(self.data_list)
            self.canvas.draw()

        self.after(100, self.rxd_update)
        

def serial_monitor_gui():
    """
    Start and run the customtkinter application. 
    This is the main entry point of the application that creates an instance of the Application class and executes the main loop.
    """
    logger = log_init()

    port_interface = port_manager.select_port(interactive=True, portname="serial monitor", logger=logger)
    format_input = input("format ('STR', 'HEX') ['STR'] >> ")
    if format_input.strip():
        format = format_input
    else:
        format = 'STR'

    if not port_interface:
        return
    
    target_serial_interface = serial_interface(port_interface, terminal=False, max_queue_size=200, format=format, logger=logger)
    app = Application(target_serial_interface, plotting = (format == 'STR'))
    app.mainloop()