# 🧹 Quick Cleanup Guide

## TL;DR - Do This Now

**Windows PowerShell:**
```powershell
cd your-tempwise-repo
git rm --cached tempwise_ble_mqtt.py config_template.py install.sh UPDATE_SUMMARY.md
git commit -m "Remove MQTT dependencies, pure native integration"
git push
```

**Linux/Mac Terminal:**
```bash
cd your-tempwise-repo
bash cleanup.sh
git commit -m "Remove MQTT dependencies, pure native integration"
git push
```

---

## What Happens

✅ These 4 MQTT-only files are removed:
- `tempwise_ble_mqtt.py`
- `config_template.py`
- `install.sh`
- `UPDATE_SUMMARY.md`

✅ Your project becomes 100% pure native integration

✅ GitHub Actions automatically:
- Validates HACS requirements
- Creates release
- Updates HACS listing

---

## Result

🎉 Users can now install with 3 clicks via HACS!

1. Home Assistant → HACS
2. Search "Tempwise"
3. Install ✅

**Done!**

---

## Files That Stay

```
✅ custom_components/tempwise_ble/  ← The integration
✅ .github/workflows/                ← Auto-release
✅ README.md                         ← Docs
✅ All guides and documentation     ← Helpful
```

---

## Next Commands

```bash
# After cleanup, release it:
git tag v1.0.0
git push origin v1.0.0

# Done! GitHub Actions handles the rest 🚀
```

That's it! Your Tempwise integration is now **clean, professional, and production-ready**.
