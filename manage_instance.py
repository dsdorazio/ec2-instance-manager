import os
import argparse
from ec2_instance_manager.ec2instance import Ec2Instance

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--instance', 
        type=str, 
        dest='instance', 
        default='i-0bbb0c6c8ed62fe83', # TODO dan-rs-1.37 remove
        help='instance id'
    )

    parser.add_argument(
        '-a', '--action', 
        type=str, 
        dest='action', 
        choices={"start", "stop", "describe"}
    )

    args = parser.parse_args()
    action = args.action
    instance_ids = args.instance.split(',')

    chrome_path = ""    
    if os.name == 'nt':
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    else:
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    
    print("Action: {}".format(action))
    print("Instance Id: {}".format(instance_ids))

    ec2 = Ec2Instance(instance_ids=instance_ids, action=action)
    ec2.open_instance_page(chrome_path=chrome_path)