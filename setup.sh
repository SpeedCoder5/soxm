#!/usr/bin/env bash
set -e

echo "Determining installed Firefox version..."

if ! command -v firefox &>/dev/null; then
    echo "Firefox is not installed. Please install Firefox first."
    exit 1
fi

# Get the Firefox version (e.g. "Mozilla Firefox 133.0")
FIREFOX_VERSION=$(firefox --version | awk '{print $3}')
echo "Installed Firefox version: $FIREFOX_VERSION"

###############################################
# Download and install the appropriate geckodriver
###############################################

echo "Fetching latest geckodriver release info from GitHub..."
LATEST_JSON=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest)
GECKO_VERSION=$(echo "$LATEST_JSON" | grep -Po '"tag_name": "\K.*?(?=")')
if [ -z "$GECKO_VERSION" ]; then
    echo "Error: Could not determine the latest geckodriver version."
    exit 1
fi
echo "Latest geckodriver version: $GECKO_VERSION"

# Create and enter a downloads directory
echo "Creating downloads directory..."
mkdir -p ./downloads
cd ./downloads

# Determine system architecture to pick the correct tarball
ARCH=$(uname -m)
if [ "$ARCH" == "x86_64" ]; then
    PLATFORM="linux64"
elif [ "$ARCH" == "i686" ] || [ "$ARCH" == "i386" ]; then
    PLATFORM="linux32"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

GECKO_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-${PLATFORM}.tar.gz"

echo "Downloading geckodriver from: $GECKO_URL"
wget -q --show-progress -O geckodriver.tar.gz "$GECKO_URL"

echo "Extracting geckodriver..."
tar -xzf geckodriver.tar.gz
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
rm geckodriver.tar.gz

cd ..

###############################################
# Final Verification
###############################################

echo "Installation complete."
echo "Firefox version: $(firefox --version)"
echo "geckodriver version: $(geckodriver --version)"
