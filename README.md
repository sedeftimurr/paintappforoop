# 🎨 Python OOP Paint Application

A simple yet feature-rich paint application built using **Python's Tkinter GUI framework**, designed to **demonstrate Object-Oriented Programming (OOP) principles** such as **Abstraction**, **Encapsulation**, **Inheritance**, and **Polymorphism**.

Created for educational purposes to showcase good software architecture and clean OOP design in a GUI project.

---

## 🚀 Features

- 🖌️ Multiple drawing tools (Oval, Square, Star, Line, Circle, Eraser)
- 🎨 Color palette & custom color selection
- 📏 Adjustable brush size (with slider & quick buttons)
- ⬅️ Undo / ➡️ Redo drawing history
- 📁 Save drawing as image (.png)
- 🌈 Background color options
- 💾 Canvas reset (New Drawing)
- 🧰 Clean UI design with emoji icons
- 🧠 Fully modular and extensible architecture

---

## 📚 OOP Concepts Demonstrated

| Principle        | Description                                                                                                                                       | File(s)                                                                 |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| **Abstraction**   | Common drawing tool interface defined using an abstract base class (`DrawingTool`)                                                              | [`abstract_classes.py`](abstract_classes.py)                             |
| **Encapsulation** | Drawing settings and history are hidden behind controlled interfaces using `@property` and private variables (`_var`)                          | [`settings.py`](settings.py)                                             |
| **Inheritance**   | Drawing tools and the application class itself inherit from base classes to reuse and extend functionality                                     | [`drawing_tools.py`](drawing_tools.py), [`paint_app.py`](paint_app.py)   |
| **Polymorphism**  | Different tools implement the same `draw()` method differently, allowing flexible and interchangeable use                                       | [`drawing_tools.py`](drawing_tools.py)                                   |

---

## 🗂️ Project Structure

├── paint_app.py # Main application logic & GUI
├── drawing_tools.py # Individual drawing tool classes (brushes, eraser, etc.)
├── abstract_classes.py # Abstract base class for drawing tools
├── settings.py # Drawing settings and canvas history (undo/redo)


---

## 🛠️ Requirements

- Python 3.8+
- `tkinter` (usually included with Python)
- `pillow` (for image saving)

Install dependencies:

```bash
pip install pillow
```
▶️ How to Run
Clone the repository or download the files.

Open terminal in the project directory.

Run the app:

```bash
python paint_app.py
```
Start drawing on the canvas using various tools and options.

💡 Usage Notes
Press 1–6 to switch between tools (Oval, Square, Star, Line, Circle, Eraser).

Use Ctrl + Z and Ctrl + Y to undo/redo actions.

Use Ctrl + S to save your drawing.

Use Ctrl + N to clear the canvas.


## 📬 Contact Me

**Sedef Timur**  
[![Email](https://img.shields.io/badge/Email-sedeftimurrr@gmail.com-red?style=flat&logo=gmail)](mailto:sedeftimurrr@gmail.com)  
[![GitHub](https://img.shields.io/badge/GitHub-sedeftimurr-181717?style=flat&logo=github)](https://github.com/sedeftimurr)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-sedeftimur-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/sedeftimur)

