#!/usr/bin/python3
import boto3

ec2 = boto3.resource('ec2')

instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

for instance in instances:
        instance_name = list(filter(lambda tag: tag['Key'] == 'Name', instance.tags))[0]['Value']

for volume in ec2.volumes.all():
        vol_id = volume.id
        description = 'snapshot-%s.%s' % (instance_name, volume.volume_id)
        ec2.create_snapshot(VolumeId=vol_id, Description=description)
