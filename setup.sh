curl -LsSf https://astral.sh/uv/install.sh | sh

curl -LsSf -o $HOME/.local/bin/autosetup.py https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/refs/heads/master/autosetup.py

# Define the target directory
TARGET_DIR="$HOME/.local/bin"

# Create the target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Define the content of the new script
SCRIPT_CONTENT='#!/bin/sh
uv run --with "requests,colorama" $HOME/.local/bin/autosetup.py'

# Remove old version of quantum init
rm $TARGET_DIR/quantum_init
# Write the content to a new script file in the target directory
echo "#!/bin/sh" > "$TARGET_DIR/quantum_init"
echo "uv run --with \"requests,colorama\" --python 3.12.9 $TARGET_DIR/autosetup.py" > "$TARGET_DIR/quantum_init"
# Make the new script executable
chmod +x "$TARGET_DIR/quantum_init"

echo "Generated executable script: $TARGET_DIR/quantum_init"
