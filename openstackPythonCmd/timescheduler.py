from flask import jsonify
import subprocess
import schedule

def check_idea_state():
    result = subprocess.run(['./check_vm_idle_state.sh'], stdout=subprocess.PIPE, text=True)
    status = {}
    for line in result.stdout.strip().split("\n"):
        key, value = line.split("=")
        status[key] = value == "true"
    
    print(status)
    return jsonify(status),200

def check_k3():
    try:
        result = subprocess.run(['./check_k3s_installed.sh'], stdout=subprocess.PIPE, text=True)
        status = result.stdout.strip().split("=")
        if len(status) == 2 and status[0] == "k3s_installed":
            is_installed = status[1] == "true"
            return jsonify({"k3s_installed": is_installed}), 200
        else:
            return jsonify({"error": "Unexpected script output"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def auto_shutdown():
    if check_idea_state and check_k3 == True:
        # delete
        print("System Shutdown")
    else:
        # Occupied
        print("System Occupied")

    return jsonify({}),200

# Auto Schedule Check after every 5 min
schedule.every(5).minutes.do(auto_shutdown)
while True:
    schedule.run_pending()
