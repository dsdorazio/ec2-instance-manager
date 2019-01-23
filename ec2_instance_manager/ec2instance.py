import boto3
import time
import webbrowser

class Ec2Instance:
    """ 
    Represents collection of attributes and methods associated with a specific
    EC2 Instance, such that it can be started, stopped, described, etc.
    """
    def __init__(self, instance_ids: list(), action: str):
        self.instance_ids = self.set_instance_ids(instance_ids)
        self.action = action

        self.client = boto3.client('ec2')
        self.resource = boto3.resource('ec2')
        self.description = self.describe()
        self.state = self.get_state()
        self.public_dns = self.get_public_dns()

        self.perform_action(action=self.action)

    def set_instance_ids(self, instance_ids: list()):
        
        if len(instance_ids) > 1:
            raise TooManyInstancesException
        else:
            return instance_ids

    def get_state(self) -> str:
        return self.description.get('Reservations')[0].get('Instances')[0].get('State').get('Name')

    def get_public_dns(self) -> str:
        return self.description.get('Reservations')[0].get('Instances')[0].get('PublicDnsName')

    def describe(self) -> dict():
        return self.client.describe_instances(InstanceIds=self.instance_ids)

    def start_instance(self):
        if self.state == 'stopped':
            response = self.resource.instances.filter(InstanceIds=self.instance_ids).start()
            print(response)
            
            retries = 1
            for i in range(0,retries):
                self.refresh_after_state_change()
                
                if self.public_dns:
                    break

        else:
            print("Instance isn't stopped. Current status is {}".format(self.state))

    def stop_instance(self):
        if self.state == 'running':
            response = self.resource.instances.filter(InstanceIds=self.instance_ids).stop()
            print(response)
        else:
            print("Instance isn't running. Current status is: {}".format(self.state))
        
    def refresh_after_state_change(self, wait_time_in_seconds: int=45):
        """
        Method to fetch new description after something about the instance has changed.
        :param wait_time_in_seconds - Used to help ensure that the state change has completed.
        """
        print("Waiting {} seconds for instance to start..".format(wait_time_in_seconds))
        time.sleep(wait_time_in_seconds)

        self.description = self.describe()
        self.public_dns = self.get_public_dns()
        self.state = self.get_state()

    def perform_action(self, action: str):
        """
        Method used to decide what action the caller is attempting to make.
        :param action - controls the underlying operation on the instance.
        """
        if self.action == 'stop' and self.state == 'running':
            self.stop_instance()
        elif self.action == 'start' and self.state == 'stopped':
            self.start_instance()
        elif self.action == 'describe':
            print("Current State: {}".format(self.state))
            print("Current Address: {}".format(self.public_dns))
            print(self.description)
        else:
            print("Current status is {}. Action: '{}' cannot be performed.".format(self.state, self.action))

    def open_instance_page(self, chrome_path: str):
        if self.public_dns:
            print("Opening {} in Chrome now...".format(self.public_dns))
            webbrowser.get(chrome_path).open(self.public_dns)

class TooManyInstancesException(Exception):
    """ Raised when multiple instance ids are provided. """
    pass

