import boto3
import json
import pprint

def finditem(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.items():
        print("key: {}  value: {}".format(key, value))

        if isinstance(value, list):
            for item in value:
                finditem(item, field)
                # if isinstance(item, dict):
                    # finditem(item, field)
                    # more_results = finditem(item, field)
                    # for another_result in more_results:
                    #     fields_found.append(another_result)

        elif isinstance(value, dict):
            finditem(value, field)
            # results = finditem(value, field)
            # for result in results:
            #     fields_found.append(result)

        elif key == field:
            fields_found.append(value)

    return fields_found

pp = pprint.PrettyPrinter(indent=4)

ec2 = boto3.client('ec2')
response = ec2.describe_instances(InstanceIds=['i-0bbb0c6c8ed62fe83'])

# state = finditem(response, 'Reservations')
# print(state)
instance_state = response.get('Reservations')[0].get('Instances')[0].get('State').get('Name')
pp.pprint(instance_state)