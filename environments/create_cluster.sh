
#!/usr/bin/env bash

set -e
CLUSTER_NAME="kubepilot-cluster"

echo "Creating k3d cluster: $CLUSTER_NAME"

# Create the cluster
k3d cluster create "$CLUSTER_NAME" \
    --servers 1 \
    --agents 2 \
    --port "8080:80@loadbalancer" \
    --port "8443:443@loadbalancer" \
    --wait

echo "k3d cluster $CLUSTER_NAME is ready."
echo "You can now use kubectl to connect to the cluster."
