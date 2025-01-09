from LoggingHandler import Logger
from FC500Com import FC500Com
from settings import Settings

class CommandInterpreter:
    def __init__(self, settings:Settings):
        self.settings = settings
        self.fc500Com = FC500Com(settings)
        self.logger = Logger()
        self.commands = {
            "com": self.handle_com,
            "help": self.handle_help,
            "?": self.handle_help,
            "log": self.handle_log
        }
        self.com_devices = ["ESP", "FC500"]

    def receiver(self, command):
        command_parts = command.split()
        if not command_parts:
            self.logger.log_info("Unknown command. Type 'help' or '?' for command list.")
            return

        command_name = command_parts[0].lower()
        if command_name in self.commands:
            self.commands[command_name](command_parts[1:])
        else:
            self.logger.log_info("Unknown command. Type 'help' or '?' for command list.")


    def handle_com(self, args):
        if not args:
            self.logger.log_info("COM command requires arguments. Type 'help' or '?' for command list.")
            return

        if args[0].lower() == "list":
            self.logger.log_info("Available COM devices: " + ", ".join(self.com_devices))
            return

        if len(args) < 2:
            self.logger.log_info("COM command requires a device and a message. Type 'COM list' for available devices.")
            return

        device = args[0].strip().upper()
        if device not in [dev.upper() for dev in self.com_devices]:
            self.logger.log_info("Invalid COM device. Type 'COM list' for available devices.")
            return

        message = " ".join(args[1:])
        self.logger.log_info(f"Sending to {device}: {message}")
        self.logger.log_info(self.fc500Com.cmd_custom(str({message})))


    def handle_help(self, args):
        self.logger.log_info("Available commands:")
        self.logger.log_info("  COM [device] [message]  - Send a message to a COM device")
        self.logger.log_info("  COM list              - List available COM devices")
        self.logger.log_info("  LOG [level] [message]  - Log a message with a specific level")
        self.logger.log_info("  help or ?             - Display this help message")

    def handle_log(self, args):
        log_levels = {
            "USER": self.logger.log_user,
            "DEBUG": self.logger.log_debug,
            "INFO": self.logger.log_info,
            "WARNING": self.logger.log_warning,
            "ERROR": self.logger.log_error,
            "CRITICAL": self.logger.log_critical
        }

        if len(args) < 2:
            self.logger.log_info(f"LOG command requires two arguments: log level ({', '.join(log_levels.keys())}) and message.")
            return
        
        level = args[0].upper()
        message = " ".join(args[1:])
        if level not in log_levels:
            self.logger.log_error(f"Invalid log level: {level}. Allowed levels are: {', '.join(log_levels.keys())}")
            return
        
        log_levels[level](message)
