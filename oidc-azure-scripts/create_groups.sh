#!/bin/bash

# Set the user's UPN (email) - replace with the actual email
userUPN="test1@danilo.work"

# Get the Object ID of the user
userId=$(az ad user show --id "$userUPN" --query id -o tsv)

# Check if the user exists
if [ -z "$userId" ]; then
  echo "Error: User $userUPN not found in Azure AD."
  exit 1
fi

# Loop to create 200+ groups and add the user
for i in {1..200}
do
  # Define the group name
  groupName="Group-$i"

  # Create the group and capture the Group ID
  groupId=$(az ad group create --display-name "$groupName" --mail-nickname "$groupName" --query id -o tsv)

  if [ -n "$groupId" ]; then
    echo "Group $groupName ($groupId) created."

    # Add the user to the group using the Object ID
    az ad group member add --group "$groupId" --member-id "$userId"
    echo "User $userUPN added to $groupName."
  else
    echo "Failed to create $groupName."
  fi
done

