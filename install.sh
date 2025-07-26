#!/bin/bash
set -e

# Create the agents directory if it doesn't exist
AGENT_DIR="$HOME/.claude/agents"
mkdir -p "$AGENT_DIR"

# Copy ghost-cofounder.md to the agents directory and bake in the script path
cp "$(dirname "$0")/ghost-cofounder.md" "$AGENT_DIR/"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ESCAPED_PATH="${SCRIPT_DIR//\//\\/}"
sed -i.bak "s|SCRIPT_DIR|$ESCAPED_PATH|g" "$AGENT_DIR/ghost-cofounder.md"

# Clean up the temporary backup
rm -f "$AGENT_DIR/ghost-cofounder.md.bak"

echo "ghost-cofounder.md has been copied to $AGENT_DIR with script path baked in."