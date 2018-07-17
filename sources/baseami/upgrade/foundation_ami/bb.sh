#!/bin/bash


UBUNTU_AMI_ID=$1
FOUNDATION_AMI_ID="ami-1a2b3"

echo "-- Copied Ubuntu AMI '${UBUNTU_AMI_ID}' to INF. The resulting Foundation AMI ID is '${FOUNDATION_AMI_ID}'"

echo "-- Waiting for the new Foundation AMI '${FOUNDATION_AMI_ID}' to become available"

sleep 30

echo "still waiting"

echo "still waiting"

echo "done"
