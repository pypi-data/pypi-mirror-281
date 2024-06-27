import docker
import subprocess
import re
import time
import threading
import signal
import sys
import argparse

is_cleaning_up = False
current_rules = set()

def get_vm_ip(vm_name):
    """Gets the IP address of a virtual machine by its name."""
    result = subprocess.run(['prlctl', 'list', '-i', vm_name], capture_output=True, text=True)
    output = result.stdout

    vm_ip_pattern = re.compile(r'IP Addresses:\s+((?:\d+\.\d+\.\d+\.\d+,?\s*)+)')
    match = vm_ip_pattern.search(output)
    
    if match:
        vm_ip = match.group(1).split(',')[0].strip()
        print(f"Found VM IP: {vm_ip}")
        return vm_ip
    else:
        raise RuntimeError(f'VM IP address for {vm_name} not found.')

def get_existing_rules():
    """Gets existing NAT rules."""
    result = subprocess.run(['prlsrvctl', 'net', 'info', 'Shared'], capture_output=True, text=True)
    output = result.stdout

    existing_rules = set()
    rule_pattern = re.compile(r'(\S+)\s+source port=\d+ destination IP/VM id=\S+ destination port=\d+')
    for line in output.splitlines():
        match = rule_pattern.search(line)
        if match:
            rule_name = match.group(1).strip()
            existing_rules.add(rule_name)
    return existing_rules

def get_containers_ports(docker_host):
    """Gets the ports of Docker containers."""
    client = docker.DockerClient(base_url=f'tcp://{docker_host}')
    containers = client.containers.list()
    return {container.name: container.attrs['NetworkSettings']['Ports'] for container in containers}

def delete_rule(rule_name):
    """Deletes a NAT rule."""
    delete_command = ['prlsrvctl', 'net', 'set', 'Shared', '--nat-tcp-del', rule_name]
    delete_result = subprocess.run(delete_command, capture_output=True, text=True)
    if delete_result.returncode == 0:
        print(f'Successfully deleted rule {rule_name}')
    else:
        print(f'Failed to delete rule {rule_name}: {delete_result.stderr}')

def add_rule(rule_name, host_port, vm_name):
    """Adds a NAT rule."""
    add_command = ['prlsrvctl', 'net', 'set', 'Shared', '--nat-tcp-add', f"{rule_name},{host_port},{vm_name},{host_port}"]
    add_result = subprocess.run(add_command, capture_output=True, text=True)
    if add_result.returncode == 0:
        print(f'Successfully forwarded port {host_port} for rule {rule_name}')
    else:
        print(f'Failed to forward port {host_port} for rule {rule_name}: {add_result.stderr}')

def setup_port_forwarding(ports_mapping, vm_name):
    """Sets up port forwarding."""
    global current_rules
    existing_rules = get_existing_rules()
    current_rules = set()
    rules_to_add = {}

    for container, ports in ports_mapping.items():
        for port, bindings in ports.items():
            if bindings:
                for binding in bindings:
                    if binding['HostIp'] == '0.0.0.0':
                        host_port = binding['HostPort']
                        rule_name = f"{container}_{host_port}_to_{host_port}"
                        current_rules.add(rule_name)
                        if rule_name not in existing_rules:
                            rules_to_add[rule_name] = host_port

    for rule in existing_rules - current_rules:
        delete_rule(rule)

    for rule_name, host_port in rules_to_add.items():
        add_rule(rule_name, host_port, vm_name)

def monitor_docker_events(docker_host, vm_name):
    """Monitors Docker events and sets up port forwarding as needed."""
    docker_client = docker.DockerClient(base_url=f'tcp://{docker_host}')
    for event in docker_client.events(decode=True):
        if event['Type'] == 'container' and event['Action'] in ['start', 'stop', 'die', 'destroy']:
            print(f"Detected Docker event: {event['Action']} on container {event['Actor']['Attributes']['name']}")
            ports_mapping = get_containers_ports(docker_host)
            setup_port_forwarding(ports_mapping, vm_name)

def cleanup():
    """Deletes all current rules upon shutdown."""
    global is_cleaning_up
    if not is_cleaning_up:
        is_cleaning_up = True
        print("Cleaning up and deleting rules...")
        for rule_name in current_rules:
            delete_rule(rule_name)
        print("Cleanup complete. Exiting.")

def signal_handler(sig, frame):
    """Handles signals for proper shutdown."""
    print('Signal received, shutting down...')
    cleanup()
    sys.exit(0)

def main():
    """Main function to start the port forwarding service."""
    global is_cleaning_up

    parser = argparse.ArgumentParser(description='Docker container port forwarding service using Parallels VM.')
    parser.add_argument('--vm-name', type=str, default='Ubuntu 22.04.2 (x86_64 emulation)', help='Name of the Parallels VM')
    args = parser.parse_args()

    vm_name = args.vm_name

    print("Starting the port forwarding service")
    vm_ip = get_vm_ip(vm_name)
    docker_host = f"{vm_ip}:2375"

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        ports_mapping = get_containers_ports(docker_host)
        setup_port_forwarding(ports_mapping, vm_name)
        
        event_thread = threading.Thread(target=monitor_docker_events, args=(docker_host, vm_name))
        event_thread.daemon = True
        event_thread.start()

        while True:
            time.sleep(1)
    finally:
        if not is_cleaning_up:
            cleanup()

if __name__ == '__main__':
    main()
