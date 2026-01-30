# 󰆍 Bash Version / Версия на Bash

Original bash implementation of the define dictionary tool.

Оригинальная реализация словаря define на bash.

---

## 󰐕 Features / Возможности

- **2955 lines** of battle-tested bash
- **643 Russian transliterations** built-in
- **177 Russian definitions** embedded
- Works on any system with `bash`, `curl`, `jq`
- Single-file deployment

---

## 󰏗 Installation / Установка

```bash
# Copy to your bin directory
cp define ~/.local/bin/
cp определить словарь слово ~/.local/bin/
chmod +x ~/.local/bin/{define,определить,словарь,слово}

# Add to PATH if needed
export PATH="$HOME/.local/bin:$PATH"
```

### Dependencies / Зависимости

```bash
# Linux (Ubuntu/Debian)
sudo apt install curl jq

# Linux (Arch)
sudo pacman -S curl jq

# macOS
brew install curl jq

# Optional for audio / Для аудио (опционально):
# Linux: mpv, vlc, or ffplay
# macOS: uses built-in afplay
```

---

## 󰙨 Usage / Использование

```bash
define serendipity          # English word
define привет               # Russian (Cyrillic)
define privet               # Russian (transliteration)
define -f love              # Full info
define -p hello             # Play pronunciation
define --save word          # Save to vocabulary
define --quiz               # Quiz mode
```

---

## 󰗊 vs Python Version

| Feature | Bash | Python |
|---------|------|--------|
| Dependencies | curl, jq | None (stdlib) |
| Grammar (cases, conjugation) | ❌ | ✅ |
| Idioms database | ❌ | ✅ |
| Code structure | Single file | Modular |
| Extensibility | Limited | Plugin architecture |

**Recommendation:** Use Python version for new features. Bash version is maintained for compatibility.

---

## 󱗗 Credits

Based on the original [define script](https://github.com/BreadOnPenguins/scripts/blob/master/shortcuts-menus/define) by [BreadOnPenguins](https://github.com/BreadOnPenguins)
