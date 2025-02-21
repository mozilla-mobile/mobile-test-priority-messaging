import sys
import tkinter as tk


def create_alert_window(title, user, message, channel):
    root = tk.Tk()
    root.title(title)

    # Set window size and position
    root.geometry("400x250+500+300")

    # Ensure the window is always on top
    root.attributes("-topmost", True)

    # Add a label for the "High Priority Alert" title inside the window
    title_label = tk.Label(
        root, text="⚠️ High Priority Alert ⚠️", font=("Helvetica", 24, "bold"), fg="red"
    )
    title_label.pack(pady=10)

    # Add a label for the Slack user who triggered the alert
    user_label = tk.Label(root, text=f"User: {user}", font=("Helvetica", 18))
    user_label.pack(pady=5)

    # Add a label for the channel the message came from
    channel_label = tk.Label(root, text=f"Channel: {channel}", font=("Helvetica", 18))
    channel_label.pack(pady=5)

    # Add a label for the message
    message_label = tk.Label(
        root, text=f"Message: {message}", wraplength=350, font=("Helvetica", 16)
    )
    message_label.pack(pady=10)

    # Add an "Acknowledge" button to close the window
    close_button = tk.Button(
        root, text="Acknowledge", command=root.destroy, font=("Helvetica", 14)
    )
    close_button.pack(pady=10)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    # This script will receive the title, user, message, and channel from the Slack bot
    title = sys.argv[1]
    user = sys.argv[2]
    message = sys.argv[3]
    channel = sys.argv[4]
    create_alert_window(title, user, message, channel)
