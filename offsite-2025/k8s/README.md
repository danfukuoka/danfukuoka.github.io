# Project Pymongo Kubernetes

## Introduction


## Installation Instructions

To build and deploy the application, follow these steps:

### 1. Docker image

```bash
docker build --no-cache --platform linux/amd64 -t danilofukuoka/kubernetes-serviceaccount-callback-k8s-3 .
docker push danilofukuoka/kubernetes-serviceaccount-callback-k8s-3:latest


### 2. Atlas

Issuer URI: https://container.googleapis.com/v1/projects/danilofukuoka/locations/us-central1-c/clusters/cluster-1
Audience: https://container.googleapis.com/v1/projects/danilofukuoka/locations/us-central1-c/clusters/cluster-1

gcloud iam service-accounts add-iam-policy-binding testsa@danilofukuoka.iam.gserviceaccount.com \
  --member="mysa:danilofukuoka.svc.id.goog[namespace/pod-service-account]" \
  --role="roles/iam.workloadIdentityUser"