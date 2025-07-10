# Password Strength Checker CLI

A beautiful and practical Python command-line tool to check password strength - one by one or in bulk - with visual output powered by
[Rich](https://github.com/Textualize/rich)
Export results to CSV, analyze weaknesses, and use it as your everyday password audit tool.

> Built with ❤️ by [StarCoder](https://github.com/StarCoderSC)

---

## 🛠 Features

- ✅ **Single Password Check** (with confirmation prompt)
- ✅ **Bulk Mode** from '.txt' file
- ✅ **Rich-based CLI interface** with colors and tables
- ✅ **CSV Export** (auto path + timestamped filenames)
- ✅ **Auto-folder creation** for exports
- ✅ **Warning on overwriting existing CSVs**
- ✅ Cross-platform and beginner-friendly

---

## 💻 Usage

### 🔹 Run Single Password Check
```bash
python checker.py

Choose Option 1 and enter your password to check its strength

🔹 Bulk Check from file
```bash
python checker.py --file password.txt

This will anylyse each line in password.txt and output a styled Rich table + CSV report.

🔹 Custom CSV Output Path

```bash
python checker.py --file password.txt --output result/test.csv
