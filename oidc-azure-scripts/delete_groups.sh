#!/bin/bash

# Loop to delete 200+ groups
for i in {1..200}
do
  # Define the group name
  groupName="Group-$i"

  # Get the group ID
  groupId=$(az ad group show --group "$groupName" --query id -o tsv 2>/dev/null)

  if [ -n "$groupId" ]; then
    # Delete the group
    az ad group delete --group "$groupId"
    echo "Group $groupName ($groupId) deleted."
  else
    echo "Group $groupName not found, skipping."
  fi
done
