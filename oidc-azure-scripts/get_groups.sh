#!/bin/bash

#  "_claim_names": {
#    "groups": "src1"
#  },
#  "_claim_sources": {
#    "src1": {
#      "endpoint": "https://graph.windows.net/<TENANT_ID>/users/<USER_ID>/getMemberObjects"
#    }
#  },

### CONFIGURATION 
USER_ID="" # CHANGE THIS!
OUTPUT_FILE="user_groups_${USER_ID}.txt"

### AUTHENTICATION ###
GRAPH_API_URL="https://graph.microsoft.com/v1.0/users/$USER_ID/getMemberObjects"
USER_INFO_URL="https://graph.microsoft.com/v1.0/users/$USER_ID"

echo "Getting access token using Azure CLI..."
ACCESS_TOKEN=$(az account get-access-token --resource https://graph.microsoft.com --query accessToken -o tsv 2>/dev/null)

# Check if we got a token
if [ -z "$ACCESS_TOKEN" ]; then
    echo "Failed to get an access token. Make sure you are logged in with 'az login'." | tee "$OUTPUT_FILE"
    exit 1
fi

echo "Access Token Retrieved." | tee "$OUTPUT_FILE"

### FETCH GROUPS ###
echo "Fetching groups for user $USER_ID..." | tee -a "$OUTPUT_FILE"
RESPONSE=$(curl -s -X POST "$GRAPH_API_URL" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"securityEnabledOnly": false}')

# Check for API errors
if echo "$RESPONSE" | jq -e .error >/dev/null; then
    echo "Error fetching groups:" | tee -a "$OUTPUT_FILE"
    echo "$RESPONSE" | jq . | tee -a "$OUTPUT_FILE"
    exit 1
fi

### FETCH GROUP DETAILS ###
GROUP_IDS=$(echo "$RESPONSE" | jq -r '.value[]')

echo "Fetching display names for each group..." | tee -a "$OUTPUT_FILE"
for GROUP_ID in $GROUP_IDS; do
    GROUP_RESPONSE=$(curl -s -X GET "https://graph.microsoft.com/v1.0/groups/$GROUP_ID" \
        -H "Authorization: Bearer $ACCESS_TOKEN")

    # Check for errors in group response
    if echo "$GROUP_RESPONSE" | jq -e .error >/dev/null; then
        echo "Error fetching details for group ID $GROUP_ID:" | tee -a "$OUTPUT_FILE"
        echo "$GROUP_RESPONSE" | jq . | tee -a "$OUTPUT_FILE"
        continue
    fi

    # Output the group display name and ID
    GROUP_NAME=$(echo "$GROUP_RESPONSE" | jq -r '.displayName')
    echo "Group ID: $GROUP_ID, Display Name: $GROUP_NAME" | tee -a "$OUTPUT_FILE"
done

### OUTPUT ###
echo "All groups the user belongs to have been saved to $OUTPUT_FILE."
