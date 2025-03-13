curl -LsSf https://astral.sh/uv/install.sh | sh

curl -LsSf -o $HOME/.local/bin/autosetup.py https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/refs/heads/master/autosetup.py

# Define the target directory
TARGET_DIR="$HOME/.local/bin"
TARGET_NAME="qproject"
# Create the target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Remove old version of quantum init
if [ -e "$TARGET_DIR/$TARGET_NAME" ]; then
    echo "Removing old version of: $TARGET_DIR/$TARGET_NAME"
    rm $TARGET_DIR/$TARGET_NAME
fi
# Write the content to a new script file in the target directory
echo "#!/bin/sh" > "$TARGET_DIR/$TARGET_NAME"
echo "uv run --with \"colorama,requests,readchar\" --python 3.12.9 $TARGET_DIR/autosetup.py \"\$@\""  > "$TARGET_DIR/qproject"
# Make the new script executable
chmod +x "$TARGET_DIR/$TARGET_NAME"

echo "Installing to $TARGET_DIR"
echo "  $TARGET_NAME"
echo "To create a new quantum project reopen the terminal and run the command: $TARGET_NAME"
