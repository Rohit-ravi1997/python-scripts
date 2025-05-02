import re
import subprocess
from datetime import date, timedelta

## Author Rohit R ###

# Open the 'hosts' file for reading
with open('/etc/hosts', 'r') as file:
    for line in file:
        # Check if line contains 'smapp' or 'dia'
        if re.search(r"smapp|dia", line):
            print("===============")
            server = line.split()[0]  # Extract server name from the line
            
            # Construct SSH command
            ssh_command = f"ssh {server}"
            
            # Get the current date and the date for one day ago in the required format
            current_date = date.today().strftime("%Y-%m-%d")
            previous_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
            
            # Define the remote bash script
            remote_commands = f"""
            hostname;
            cd /opt/tpa/logs;
            timestamp=$(date +%Y%m%d%H%M%S);
            a="$(hostname)_$timestamp";  # Use a unique directory name using a timestamp
            mkdir -p $a;
            echo "Created directory $a";
            files=$(find . -type f -newermt {current_date} ! -newermt {previous_date} \\( -name "SPSServer.log" -o -name "SPSServer.*.log.gz" \\) -o \\( -name "HLAPIServer.log" -o -name "TPA_system.log" -o -name "Spotlight.log" \\));
            if [ -n "$files" ]; then
                cp -f $files $a/;
                echo "Files copied to $a";
                scp -r $a root@tbnpc-oame-1:/opt/tpa/users/tpaadmin;
                rm -rf $a;
            else
                echo "No files found or error occurred";
            fi
            echo "Executed"
            """
            
            # Construct the full SSH command
            full_command = f"{ssh_command} '{remote_commands}'"
            
            try:
                # Run the SSH command using subprocess
                result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                # Print the output and errors (if any)
                print("Output:", result.stdout)
                print("Errors:", result.stderr)
            
            except Exception as e:
                print(f"Error occurred while running the SSH command: {e}")
