import os
import sys

APP_NAME = "datengeist"
APP_SCRIPT = "Sample_Dataset.py"
VERSION = "0.0.1"

# Additional Streamlit configurations
RUN_CONFIGS = [
    "--ui.hideTopBar true",
    "--client.toolbarMode minimal",
    "--server.runOnSave true",
    "--theme.base dark",
    "--theme.backgroundColor black",
    "--theme.secondaryBackgroundColor '#333333'",
    # "--client.showErrorDetails false",
    "--server.maxUploadSize=500"
]


def show_help():
    """Display help information about the usage of the application."""
    help_text = f"""
    Usage: {APP_NAME} [command] [options]

    Commands:
        start              Start the Streamlit app.
        help               Print help and exit
        version            Print version and exit

    Examples:
        {APP_NAME} start          # Start at default input page

    For more information, visit the documentation.
    """
    print(help_text)


def start():
    """Start the Streamlit app with the specified data path."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, APP_SCRIPT)

    configs_str = ' '.join(RUN_CONFIGS)

    print(f"Starting Cookie ...")

    # Build the Streamlit command
    os.system(f"streamlit run {app_path} {configs_str}")




def main():
    """Main entry point of the application."""
    if len(sys.argv) == 1:
        show_help()  # Show help if no command is provided
        return
    elif len(sys.argv) > 2:
        print(f"Error: Got unexpected argument ({sys.argv[2]})")
        return

    command = sys.argv[1]
    if command == 'start':
        start()
    elif command == 'help':
        if len(sys.argv) > 2:
            print(f"Error: Got unexpected argument ({sys.argv[2]})")
            return
        show_help()
        return

    elif command == 'version':
        if len(sys.argv) > 2:
            print(f"Error: Got unexpected argument ({sys.argv[2]})")
            return

        print(f"Cookie, version {VERSION}")
        return

    else:
        print(f"Error: No such command '{command}'")
        show_help()

if __name__ == '__main__':
    main()
