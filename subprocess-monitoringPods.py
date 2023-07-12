import subprocess
import re
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def convert_text_table_to_array(text_table):
    lines = text_table.strip().split('\n')
    if (str(lines).find("running")):
        table_data = [line.split() for line in lines]
    return table_data

def display_pod_name_only(array_data):
    podName = [row[0] for row in array_data[0:]]
    return podName

def execute_subprocess(cmd):
    array_data = []
    try:
        result = subprocess.run([cmd], shell=True, capture_output=True, text=True, check=True)
        array_data = convert_text_table_to_array(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error")

    return(array_data)

pod_array = execute_subprocess('kubectl get pods -n default | grep "staging"')

podNames = display_pod_name_only(pod_array)

for podName in podNames:
    ##giving time 2sec between each request
    time.sleep(2)
    print(podName)

    str_kubectl = "kubectl top pod " + podName + " --containers -n default"
    str_kubectl_out = execute_subprocess(str_kubectl)
    print(str_kubectl_out)

    if (str_kubectl_out):
        print(str_kubectl_out[1][3])
        memory_number = re.sub(r"\D", "", str_kubectl_out[1][3])

        ##TODO: check for request memory value kubectl describe pod whatever
        if (int(memory_number) > 200):
            print(bcolors.WARNING + "Warning: potential memory issue with pod: " + podName + " max to " + str_kubectl_out[1][3] + bcolors.ENDC)
            print(bcolors.OKCYAN + "Should try to recover with: kubectl delete -n  " + podName + "  " + bcolors.ENDC)


