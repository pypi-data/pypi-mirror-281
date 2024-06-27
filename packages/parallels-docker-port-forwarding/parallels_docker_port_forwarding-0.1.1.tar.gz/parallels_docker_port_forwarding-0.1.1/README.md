
# Parallels Docker Port Forwarding

Parallels Docker Port Forwarding is a service that automatically manages port forwarding for Docker containers running inside a Parallels VM.

## Features

- Automatically detects running Docker containers and their exposed ports.
- Sets up port forwarding rules from the host to the Parallels VM.
- Monitors Docker events and updates port forwarding rules dynamically.

## Requirements

- Python 3.8+
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)
- Parallels Desktop with `prlctl` and `prlsrvctl` command-line tools

## Installation

You can install the package using pip:

```bash
pip install parallels-docker-port-forwarding
```

## Usage

To start the port forwarding service, run:

```bash
parallels-docker-port-forwarding --vm-name "Your VM Name"
```

If the VM name is not provided, the default VM name `'Ubuntu 22.04.2 (x86_64 emulation)'` will be used.

## Development

To set up the development environment:

1. Clone the repository:

```bash
git clone https://github.com/imtpot/parallels-docker-port-forwarding.git
cd parallels-docker-port-forwarding
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Run the service:

```bash
poetry run parallels-docker-port-forwarding --vm-name "Your VM Name"
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
