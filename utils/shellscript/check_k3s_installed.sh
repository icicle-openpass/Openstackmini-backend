#!/bin/bash

# Function to check if K3s is installed
check_k3s_installed() {
    if command -v k3s > /dev/null 2>&1; then
        echo "k3s_installed=true"
    else
        echo "k3s_installed=false"
    fi
}

# Execute the function
check_k3s_installed