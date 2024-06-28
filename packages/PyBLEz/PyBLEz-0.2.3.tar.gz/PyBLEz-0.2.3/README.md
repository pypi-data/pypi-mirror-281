![Total Downloads](https://pepy.tech/badge/pyblez)
[![Downloads](https://static.pepy.tech/badge/pyblez/month)](https://pepy.tech/project/pyblez)
[![Downloads](https://static.pepy.tech/badge/pyblez/week)](https://pepy.tech/project/pyblez)
![PyPI Version](https://img.shields.io/pypi/v/pyblez)
![License](https://img.shields.io/pypi/l/pyblez)
![GitHub issues](https://img.shields.io/github/issues/kgoke/PyBLEz.svg)


# PyBLEz

PyBLEz is a Python library for creating BLE peripherals using BlueZ and D-Bus. This library allows you to easily set up BLE services and characteristics, handle read and write operations, and send notifications to connected devices.

## Usage

### Creating a Simple BLE Peripheral

```Python
#!/user/bin/env python3
from PyBLEz import create_ble_peripheral, enable_logs, disable_logs

# Enable debug logs
enable_logs()

def main():
    # create a BLE peripheral instance
    ble = create_ble_peripheral()
    ble.power_on_adapter()

    # Add a service
    service = ble.add_service("12345678-1234-5678-1234-56789abcdef0")

    # Add a characteristic to the service
    char = service.add_characteristic("12345678-1234-5678-1234-56789abcdef1", ["read", "write", "notify"], bytearray("Hello", "utf-8"))

    # Defind the read_value function
    def read_value(options):
        return char.value
    
    char.Read = read_value

    # Define the write_value function
    def write_value(value, options):
        data = bytes(value).decode("utf-8")
        print(f"Received: {data}")
        processed = data.upper()
        char.value = bytearray(processed, "utf-8")
        print(f"Processed: {processed}")

    char.Write = write_value

    # Register the GATT application
    ble.register_application()

    # Start advertising (10 seconds)
    ble.start_advertising("HelloBLE", [service.uuid], duration=10)

    # Run the main loop
    ble.run()

if __name__ == "__main__":
    main()

```

### Detailed Explanation

#### Read Characteristic:

- Readable `characteristic` is created with the UUID `12345678-1234-5678-1234-56789abcdef1` and is set to return the value "Hello".
- The `read_value` function is assigned to the characteristic's `Read` method.

#### Write Characteristic:

- Writable is created with the UUID `12345678-1234-5678-1234-56789abcdef1` and allows writing data.
- The `write_value` function is assigned to the characteristic's `Write` method.

#### Advertising:

- The peripheral advertises with the local name "HelloBLE" and includes the service UUID.

#### Running the Peripheral:

- The `run` method starts the main loop to keep the application running and responsive to BLE interactions.

## Requirements

- Python 3.6 or later
- BlueZ (5.41 or later)
- D-Bus (python-dbus)
- Pycairo
- GLib

## Installation

```Bash
pip install PyBLEz
```

## Conrtibuting

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License.

## Contact

For any questions or inquiries, please contact `goecke.dev@gmail.com`.
