#!/usr/bin/python3
import boto3

ec2 = boto3.resource('ec2')

print("\n\nSnapshot started")
instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

for instance in instances:
        instance_name = list(filter(lambda tag: tag['Key'] == 'Name', instance.tags))[0]['Value']

        for volume in ec2.volumes.filter(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance.id]}]):
                description = 'snapshot-%s.%s' % (instance_name, volume.volume_id)

        if volume.create_snapshot(VolumeId=volume.volume_id, Description=description):
                print("Snapshot description [%s]" % description)

print("\n\nComplited")
