#!/usr/bin/env python

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
compute = discovery.build('compute', 'v1', credentials=credentials)

# Get all instances
instances = compute.instances().aggregatedList(project='veltzer-machines-id').execute()['items']

for zone, instances_data in instances.items():
    if 'instances' in instances_data:
        for instance in instances_data['instances']:
            instance_name = instance['name']
            # Get existing firewall rules
            firewall_body = {
                "name": "allow-all-all",
                "allowed": [
                    {
                        "IPProtocol": "tcp",
                        "ports": [
                            "1-65535"  # Allow all TCP ports
                        ]
                    },
                    {
                        "IPProtocol": "udp",
                        "ports": [
                            "1-65535"  # Allow all UDP ports
                        ]
                    },
                    {
                        "IPProtocol": "icmp"  # Allow ICMP
                    }
                ],
                "sourceRanges": [
                    "0.0.0.0/0"
                ],
                "targetTags": [
                    "allow-all"  # Create a tag for easier management
                ]
            }

            # Create the firewall rule
            try:
                compute.firewalls().insert(project='veltzer-machines-id', body=firewall_body).execute()
                print("Firewall rule created to allow all ports on all instances.")
            except Exception as e:
                if 'alreadyExists' in str(e):
                    print(f"Firewall rule 'allow-all-all' already exists.")
                else:
                    print(f"An error occurred: {e}")

            # Add the tag to the instance
            tags_body = {
                "items": [
                    "allow-all"
                ],
                "fingerprint": instance['tags']['fingerprint']
            }
            compute.instances().setTags(project='veltzer-machines-id', zone=zone.split('/')[-1], instance=instance_name, body=tags_body).execute()
            print(f"Tag 'allow-all' added to instance {instance_name} in zone {zone}")
