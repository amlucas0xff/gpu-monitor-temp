import subprocess
import re
import toml
import argparse
def load_config(file_path):
    if file_path:
        with open(file_path, 'r') as f:
            return toml.load(f)
    return {}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Monitor GPU temperatures and send notifications.")
    parser.add_argument('-c', '--config', type=str, help="Path to the TOML configuration file.")
    return parser.parse_args()
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

if __name__ == "__main__":
    args = parse_arguments()
    config = load_config(args.config)
    monitor_temperatures(config)
