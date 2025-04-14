
#!/bin/bash

set -e

SERVICE_ACCOUNT_NAME="workshop-user"
NAMESPACE="default"
SECRET_NAME="${SERVICE_ACCOUNT_NAME}-token"
KUBECONFIG_FILE="kubeconfig-workshop.yaml"

echo "🔧 Creating ServiceAccount..."
kubectl create serviceaccount "$SERVICE_ACCOUNT_NAME" --namespace "$NAMESPACE" || true

echo "🔐 Creating ClusterRoleBinding with 'cluster-admin' role..."
kubectl create clusterrolebinding "${SERVICE_ACCOUNT_NAME}-cluster-admin-binding" \
  --clusterrole=cluster-admin \
  --serviceaccount="${NAMESPACE}:${SERVICE_ACCOUNT_NAME}" || true

echo "🧪 Creating long-lived token secret..."
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: $SECRET_NAME
  namespace: $NAMESPACE
  annotations:
    kubernetes.io/service-account.name: $SERVICE_ACCOUNT_NAME
type: kubernetes.io/service-account-token
EOF

echo "⏳ Waiting for token to populate..."
sleep 5

echo "📥 Fetching data for kubeconfig..."
TOKEN=$(kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" -o jsonpath='{.data.token}' | base64 --decode)
CA_CRT=$(kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" -o jsonpath='{.data.ca\.crt}')
CLUSTER_NAME=$(kubectl config view --minify -o jsonpath='{.clusters[0].name}')
CLUSTER_ENDPOINT=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')

echo "🧾 Writing kubeconfig to $KUBECONFIG_FILE..."
cat <<EOF > $KUBECONFIG_FILE
apiVersion: v1
kind: Config
clusters:
- name: $CLUSTER_NAME
  cluster:
    certificate-authority-data: $CA_CRT
    server: $CLUSTER_ENDPOINT
contexts:
- name: workshop-context
  context:
    cluster: $CLUSTER_NAME
    user: $SERVICE_ACCOUNT_NAME
current-context: workshop-context
users:
- name: $SERVICE_ACCOUNT_NAME
  user:
    token: $TOKEN
EOF

echo "✅ Done! Kubeconfig saved to $KUBECONFIG_FILE"
