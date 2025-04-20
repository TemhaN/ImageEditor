# 🖼️ ImageEditor

**ImageEditor** — мощный и удобный редактор изображений для цветокоррекции и применения эффектов.  
С его помощью можно легко загружать изображения, настраивать цвета, применять фильтры и сохранять результаты.  
Интерфейс построен на [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), что делает его стильным и интуитивно понятным.

---

## ✨ Возможности

- 🎨 **Цветокоррекция**: регулировка яркости, контрастности, насыщенности и баланса цветов.
- 🧪 **Эффекты**: фильтры, такие как размытие, резкость, сепия, чёрно-белый и другие.
- 🖼️ **Поддержка форматов**: работа с JPEG, PNG и другими популярными форматами.
- 🖱️ **Интуитивный интерфейс**: простое управление через графический интерфейс.
- 💾 **Сохранение**: экспорт изображений в нужном формате.

---

## 📋 Требования

- Python **3.8+**

### Установка зависимостей

```bash
pip install customtkinter Pillow numpy opencv-python CTkMessagebox color-matcher pyinstaller
```

---

## 🧩 Зависимости

| Библиотека      | Назначение                              |
| --------------- | --------------------------------------- |
| `customtkinter` | Современный графический интерфейс       |
| `Pillow`        | Обработка изображений                   |
| `numpy`         | Работа с массивами данных               |
| `opencv-python` | Продвинутая обработка изображений       |
| `CTkMessagebox` | Всплывающие уведомления                 |
| `color-matcher` | Точная цветокоррекция                   |
| `pyinstaller`   | Сборка исполняемых файлов (опционально) |

---

## 🚀 Установка и запуск

1. **Клонируй репозиторий:**

```bash
git clone https://github.com/TemhaN/ImageEditor.git
cd ImageEditor
```

2. **Запусти приложение:**

```bash
python main.py
```

---

## 🖱️ Использование

1. Запусти `main.py`
2. Загрузи изображение через кнопку "Открыть"
3. Используй панель инструментов для цветокоррекции и фильтров
4. Сохрани полученное изображение через кнопку "Сохранить"

---

## 📦 Сборка .exe (или другой платформы)

Если хочешь собрать автономное приложение:

1. Установи `pyinstaller`, если ещё не:

```bash
pip install pyinstaller
```

2. Собери .exe:

```bash
pyinstaller --onefile main.py
```

3. Готовый исполняемый файл появится в папке `dist/`.

---

## 📸 Скриншоты

<img src="https://github.com/TemhaN/ImageEditor/blob/main/screenshots/1.png" alt="ImageEditor">
<img src="https://github.com/TemhaN/ImageEditor/blob/main/screenshots/2.png" alt="ImageEditor">
<img src="https://github.com/TemhaN/ImageEditor/blob/main/screenshots/3.png" alt="ImageEditor">
<img src="https://github.com/TemhaN/ImageEditor/blob/main/screenshots/4.png" alt="ImageEditor">
<img src="https://github.com/TemhaN/ImageEditor/blob/main/screenshots/5.png" alt="ImageEditor">

---

## 🧠 Автор

**TemhaN**  
🔗 [GitHub профайл](https://github.com/TemhaN)

---

## 🧾 Лицензия

Проект распространяется под лицензией **MIT**.  
Делай с ним, что хочешь — только не продавай бабушке 😄

---

## 📬 Обратная связь

Если нашёл баг или хочешь предложить улучшения — **welcome в issues** или **pull request**.
