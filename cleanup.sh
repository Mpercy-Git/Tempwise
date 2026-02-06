#!/bin/bash
# Cleanup script to remove MQTT-only files from the repository

echo "🧹 Cleaning up MQTT-only files..."

# Remove MQTT-only files
git rm --cached config_template.py 2>/dev/null || true
git rm --cached install.sh 2>/dev/null || true
git rm --cached tempwise_ble_mqtt.py 2>/dev/null || true
git rm --cached UPDATE_SUMMARY.md 2>/dev/null || true

# Keep only essential files
echo "📋 Essential files kept:"
echo "  ✅ custom_components/tempwise_ble/ - Main integration"
echo "  ✅ .github/workflows/ - Auto-release pipeline"
echo "  ✅ README.md - Documentation"
echo "  ✅ INSTALLATION.md - Quick start"
echo "  ✅ NATIVE_INTEGRATION_GUIDE.md - Complete guide"
echo "  ✅ hacs.json - HACS metadata"
echo "  ✅ VERSION - Version tracking"

echo ""
echo "✅ Now commit the changes:"
echo "   git commit -m 'Remove MQTT dependencies, pure native integration'"
echo "   git push"
