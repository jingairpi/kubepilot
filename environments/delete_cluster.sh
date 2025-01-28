#!/usr/bin/env bash

set -e
CLUSTER_NAME="kubepilot-cluster"

echo "Deleting k3d cluster: $CLUSTER_NAME"
k3d cluster delete "$CLUSTER_NAME"
echo "k3d cluster $CLUSTER_NAME has been deleted."
