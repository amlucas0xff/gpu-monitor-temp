# GPU Temperature Monitor

This is a simple Python script to monitor GPU temperatures and send notifications if temperatures exceed a specified threshold. The script is designed to work on systems with NVIDIA GPUs, using the `nvidia-settings` command-line utility.

## Features
- **GPU Temperature Monitoring**: Monitor multiple GPUs simultaneously.
- **Configurable Temperature Thresholds**: Use a TOML configuration file to specify individual temperature thresholds for each GPU.
- **Notifications**: Get desktop notifications when GPU temperatures exceed specified thresholds, using the `notifypy` library for multiplatform support.
- **Simple Configuration**: Use a default configuration or generate your own TOML configuration file.

## How It Works
The script fetches GPU temperatures using `nvidia-settings` and compares them to specified thresholds. Notifications are sent if a GPU temperature exceeds its threshold.

### Detailed Workflow
**Temperature Monitoring**:
   - The script first checks if the NVIDIA GPU control utility (`nvidia-settings`) is installed. If not, it exits with an error message.
   - Users can specify a configuration file using a TOML format, or the script will fall back to default values.
   - A sample TOML configuration is provided, allowing customization of the temperature threshold and notification message for each GPU.

**Arguments**:
   - `-c` or `--config`: Specify the path to a TOML configuration file. If not provided, the script uses the default config.
   - `-g` or `--generate-config`: Generate a default `config.toml` configuration file.
   - `-e` or `--execute`: Execute the script to monitor GPU temperatures and send notifications.
   - `-t` or `--test-notification`: Test the notification system.
   - `-v` or `--verbose`: Enable verbose mode for detailed output.

## Prerequisites
- **NVIDIA GPU**: The script uses `nvidia-settings` to get GPU temperatures, so it only works with NVIDIA GPUs.
- **Python 3**: Tested with Python 3.12.6.

## Installation
1. **Clone the repository**:
   ```sh
   git clone https://github.com/amlucas0xff/gpu-temp-monitor.git
   cd gpu-temp-monitor
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Generate a Default Config File
To generate a default TOML configuration file (`config.toml`):
```sh
python3 gpu_temp_monitor.py -g
```

### Test Notifications
To test the notification system:
```sh
python3 gpu_temp_monitor.py -t
```

### Running the script
To monitor GPU temperatures:
```sh
python3 gpu_temp_monitor.py -e
```

### Verbose Mode
For detailed information during execution, add the `-v` flag:
```sh
python3 gpu_temp_monitor.py -e -v
```

## Configuration File Example
The configuration file (`config.toml`) allows you to set thresholds and messages for multiple GPUs:
```toml
[GPU0]
threshold = 50
message = "Warning: Nvidia 3090 temperature has reached {temp}°C!"

[GPU1]
threshold = 80
message = "Alert: Nvidia 3090ti temperature is {temp}°C. Please check the cooling system."
```

## License
This project is licensed under the MIT License
## Author
Developed by amlucas0xff.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests for improvements or bug fixes.

