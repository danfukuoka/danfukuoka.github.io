#!/bin/bash

### CONFIGURATION 
#  "_claim_names": {
#    "groups": "src1"
#  },
#  "_claim_sources": {
#    "src1": {
#      "endpoint": "https://graph.windows.net/<TENANT_ID>/users/<USER_ID>/getMemberObjects"
#    }
#  },

### CONFIGURATION ###
# User & API details
USER_ID="<USER_ID>"
GRAPH_API_URL="https://graph.microsoft.com/v1.0/users/$USER_ID/getMemberObjects"
USER_INFO_URL="https://graph.microsoft.com/v1.0/users/$USER_ID"

### AUTHENTICATION ###
echo "Getting access token using Azure CLI..."
ACCESS_TOKEN=$(az account get-access-token --resource https://graph.microsoft.com --query accessToken -o tsv 2>/dev/null)

# Check if we got a token
if [ -z "$ACCESS_TOKEN" ]; then
    echo "Failed to get an access token. Make sure you are logged in with 'az login'."
    exit 1
fi

echo "Access Token Retrieved."

### FETCH USER INFO (to get SAMAccountName) ###
echo "Fetching user information..."
USER_RESPONSE=$(curl -s -X GET "$USER_INFO_URL" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json")

# Extract onPremisesSamAccountName if it exists
SAM_ACCOUNT_NAME=$(echo "$USER_RESPONSE" | jq -r '.onPremisesSamAccountName // empty')

if [ -n "$SAM_ACCOUNT_NAME" ]; then
    echo "SAMAccountName: $SAM_ACCOUNT_NAME"
else
    echo "SAMAccountName not found."
fi

### FETCH GROUPS ###
echo "Fetching groups for user $USER_ID..."
RESPONSE=$(curl -s -X POST "$GRAPH_API_URL" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"securityEnabledOnly": false}')

# Check for API errors
if echo "$RESPONSE" | jq -e .error >/dev/null; then
    echo "Error fetching groups:"
    echo "$RESPONSE" | jq .
    exit 1
fi

### FETCH GROUP DETAILS ###
GROUP_IDS=$(echo "$RESPONSE" | jq -r '.value[]')

echo "Fetching display names for each group..."
for GROUP_ID in $GROUP_IDS; do
    GROUP_RESPONSE=$(curl -s -X GET "https://graph.microsoft.com/v1.0/groups/$GROUP_ID" \
        -H "Authorization: Bearer $ACCESS_TOKEN")

    # Check for errors in group response
    if echo "$GROUP_RESPONSE" | jq -e .error >/dev/null; then
        echo "Error fetching details for group ID $GROUP_ID:"
        echo "$GROUP_RESPONSE" | jq .
        continue
    fi

    # Output the group display name and ID
    GROUP_NAME=$(echo "$GROUP_RESPONSE" | jq -r '.displayName')
    echo "Group ID: $GROUP_ID, Display Name: $GROUP_NAME"
done

### OUTPUT ###
echo "All groups the user belongs to have been displayed above."
