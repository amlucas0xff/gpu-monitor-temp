import subprocess
import re
import toml
import argparse

DEFAULT_CONFIG = {
    "GPU0": {
        "threshold": 80,
        "message": "GPU 0 temperature is {temp}°C"
    },
    "GPU1": {
        "threshold": 80,
        "message": "GPU 1 temperature is {temp}°C"
    }
}
def load_config(file_path):
    if file_path:
        with open(file_path, 'r') as f:
            return toml.load(f)
    return {}

def generate_default_config(file_path='config.toml'):
    with open(file_path, 'w') as f:
        toml.dump(DEFAULT_CONFIG, f)
    print(f"Default configuration file generated at {file_path}")

parser = argparse.ArgumentParser(description="Monitor GPU temperatures and send notifications.")
parser.add_argument('-c', '--config', type=str, help="Path to the TOML configuration file.")
parser.add_argument('-g', '--generate-config', action='store_true', help="Generate a default config.toml file.")
parser.add_argument('-e', '--execute', action='store_true', help="Execute the script to monitor GPU temperatures.")
parser.add_argument('-t', '--test-notification', action='store_true', help="Test the notification system.")

def parse_arguments():
    args = parser.parse_args()
    
    # Check if more than one argument is provided
    if sum([args.config is not None, args.generate_config, args.execute, args.test_notification]) > 1:
        parser.print_help()
        exit(0)
    
    return args
def get_gpu_temperatures():
    result = subprocess.run(['nvidia-settings', '-q', 'gpucoretemp'], capture_output=True, text=True)
    output = result.stdout
    temperatures = re.findall(r"Attribute 'GPUCoreTemp' \(.*\[gpu:(\d+)\]\): (\d+)\.", output)
    return {gpu: int(temp) for gpu, temp in temperatures}
def send_notification(gpu, temp, message):
    subprocess.run(['notify-send', f'GPU {gpu} Temperature Alert', message.format(temp=temp)])

def monitor_temperatures(config):
    temperatures = get_gpu_temperatures()
    for gpu, temp in temperatures.items():
        threshold = config.get(f'GPU{gpu}', {}).get('threshold', 80)  # Default threshold
        message = config.get(f'GPU{gpu}', {}).get('message', 'GPU {gpu} temperature is {temp}°C')
        if temp > threshold:
            send_notification(gpu, temp, message)

import os  # Add this import at the top of the file

if __name__ == "__main__":
    args = parse_arguments()
    if args.generate_config:
        generate_default_config(args.config if args.config else 'config.toml')
    elif args.execute:
        config_path = args.config if args.config else 'config.toml'
        if not args.config and not os.path.exists(config_path):
            print("No configuration file provided and config.toml does not exist in the current directory.")
            exit(1)
        config = load_config(config_path)
        if not any(key.startswith('GPU') for key in config):
            print("The configuration file does not contain any GPU to monitor.")
            exit(1)
        monitor_temperatures(config)
    elif args.test_notification:
        # Test notification with a dummy message
        send_notification(0, 85, "Test notification: GPU 0 temperature is {temp}°C")
    else:
        global parser
        parser.print_help()
        exit(0)
