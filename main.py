from fastapi import FastAPI
import startDialog
from loadSettings import get_settings
import argparse
import run

# initializes api and reads in the points fom file routes
app = FastAPI()


if __name__ == "__main__":

    # read and parse start arguments
    parser = argparse.ArgumentParser(description="Start FastAPI server with different modes")
    parser.add_argument('--mode', type=str, choices=['backend', 'frontend', 'full'], required=True,
                        help="Mode to run the server in")
    args = parser.parse_args()

    # loaded settings and copy ip and port settings in client and server settings json file
    settings = get_settings
    settings.copy_setting_entry_to_other_file("extensions/dockerSettings.json", 'Docker', 'extensions'
                                              , 'extensions_api')

    if startDialog.start():

        # Starts Client Server or both, depending on the startup
        if args.mode == "backend":
            run.start_backend(app, settings.select('connect', 'server_ip'), settings.select('connect', 'server_port'))
        elif args.mode == "frontend":
            run.start_frontend(app, settings.select('connect', 'client_ip'), settings.select('connect', 'client_port'))
        elif args.mode == "full":
            run.start_full(app, settings.select('connect', 'server_ip'), settings.select('connect', 'client_port'))
