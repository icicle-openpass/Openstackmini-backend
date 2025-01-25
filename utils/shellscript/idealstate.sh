#!/bin/bash

# Function to check if a service or characteristic is active or idle.
check_status() {
    if $1; then
        echo "$2=true"
    else
        echo "$2=false"
    fi
}

# 1. Check if the system is running (basic health check)
check_status "ping -c 1 127.0.0.1 > /dev/null 2>&1" "system_heartbeat"

# 2. Check for kernel logs
check_status "dmesg | grep -i 'idle' > /dev/null 2>&1" "kernel_logs_present"

# 3. Check for recent login attempts
lastlog -b 0 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "login_attempts=false"
else
    echo "login_attempts=true"
fi

# 4. Check firewall activity (assuming UFW is installed)
ufw status | grep -qi 'active'
check_status "[ $? -eq 0 ]" "firewall_active"

# 5. Check for scheduled jobs (using cron)
check_status "crontab -l | grep -i 'job' > /dev/null 2>&1" "scheduled_jobs_running"

# 6. Check network activity logs (DHCP lease renewal)
check_status "journalctl -u dhcpd.service | grep 'renew' > /dev/null 2>&1" "network_logs_present"

# 7. Check CPU and memory usage thresholds (idle state < 5%)
CPU_IDLE=$(mpstat | awk '/all/ {print $12}')
if (( $(echo "$CPU_IDLE > 95" | bc -l) )); then
    echo "cpu_usage=true"
else
    echo "cpu_usage=false"
fi

MEM_FREE=$(free -m | awk '/Mem:/ {print $4/$2 * 100.0}')
if (( $(echo "$MEM_FREE > 80" | bc -l) )); then
    echo "memory_usage=true"
else
    echo "memory_usage=false"
fi

# 8. Check if NTP synchronization is working
check_status "timedatectl show | grep -q 'NTPSynchronized=yes'" "time_synchronized"

# 9. Check if any active connections exist (idle should have minimal activity)
ACTIVE_CONNECTIONS=$(netstat -tn | grep ESTABLISHED | wc -l)
if [ "$ACTIVE_CONNECTIONS" -eq 0 ]; then
    echo "active_connections=false"
else
    echo "active_connections=true"
fi

# 10. Check disk I/O (low disk activity when idle)
DISK_USAGE=$(iostat -dx | awk 'NR>6 {sum+=$NF} END {print sum}')
if (( $(echo "$DISK_USAGE < 5" | bc -l) )); then
    echo "disk_usage=true"
else
    echo "disk_usage=false"
fi