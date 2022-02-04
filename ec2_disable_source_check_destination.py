#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3

ec2 = boto3.client('ec2')
response = ec2.describe_instances()
instances = response["Reservations"]
for instance in instances:
    tags = instance["Instances"][0]["Tags"]
    instance_id = instance["Instances"][0]["InstanceId"]
    for tag in tags:
        if tag["Key"] == "Name" and "juju-k8s-machine" in tag["Value"]:
            print(
                f'Disabling Source Check Destination on Instance : {tag["Value"]}')
            ec2.modify_instance_attribute(
                InstanceId=instance_id, SourceDestCheck={'Value': False})
