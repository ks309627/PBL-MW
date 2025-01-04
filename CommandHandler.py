import sys
from LoggingHandler import ErrorLogger

class CommandInterpreter:
    def __init__(self):
        self.error_logger = ErrorLogger()
        self.commands = {
            "com": self.handle_com,
            "help": self.handle_help,
            "?": self.handle_help,
            "log": self.handle_log
        }
        self.com_devices = ["ESP", "FC500"]

    def receiver(self, command):

        command_parts = command.lower().split()
        if not command_parts:
            self.error_logger.log_info("Unknown command. Type 'help' or '?' for command list.")
            return

        command_name = command_parts[0]
        if command_name in self.commands:
            self.commands[command_name](command_parts[1:])
        else:
            self.error_logger.log_info("Unknown command. Type 'help' or '?' for command list.")

    def handle_com(self, args):
        if not args:
            self.error_logger.log_info("COM command requires arguments. Type 'help' or '?' for command list.")
            return

        if args[0] == "list":
            self.error_logger.log_info("Available COM devices: " + ", ".join(self.com_devices))
            return

        if len(args) < 2 or args[0] not in self.com_devices:
            self.error_logger.log_info("Invalid COM device. Type 'COM list' for available devices.")
            return

        device = args[0]
        message = " ".join(args[1:])
        self.error_logger.log_info(f"Sending to {device}: {message}")

    def handle_help(self, args):
        self.error_logger.log_info("Available commands:")
        self.error_logger.log_info("  COM [device] [message]  - Send a message to a COM device")
        self.error_logger.log_info("  COM list              - List available COM devices")
        self.error_logger.log_info("  LOG [level] [message]  - Log a message with a specific level")
        self.error_logger.log_info("  help or ?             - Display this help message")

    def handle_log(self, args):
        if len(args) < 2:
            self.error_logger.log_info("LOG command requires level and message arguments. Type 'help' or '?' for command list.")
            return

        level = args[0].upper()
        message = " ".join(args[1:])
        self.error_logger.log_info(f"{level}: {message}")