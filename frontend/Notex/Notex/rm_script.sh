#!/bin/bash

PROJECT_FILE="Notex.xcodeproj/project.pbxproj"

# Function to generate a new UUID
generate_uuid() {
    uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '-'
}

# Find duplicate UUIDs and generate new ones
fix_uuids() {
    grep -o -E '[0-9a-f]{24}' "$PROJECT_FILE" | sort | uniq -d | while read -r uuid; do
        new_uuid=$(generate_uuid)
        echo "Replacing $uuid with $new_uuid"
        sed -i '' "s/$uuid/$new_uuid/g" "$PROJECT_FILE"
    done
}

fix_uuids

echo "Duplicate UUIDs have been fixed."

