# TiendaIA - Object and Bill Recognition System

![Python](https://img.shields.io/badge/Python-3.12-blue) ![OpenCV](https://img.shields.io/badge/OpenCV-Support-green) ![YOLO](https://img.shields.io/badge/YOLO-Object%20Detection-red)

## 📌 Project Description

**TiendaIA** is an object and Costa Rican bill recognition system using **YOLO**. This project allows for real-time identification of products and bills via a camera, adding up the bill values to facilitate automatic payments.

The bill recognition model was trained with **Roboflow** and **Google Colab**, enabling the detection of bills in **one thousand, two thousand, five thousand, ten thousand, and twenty thousand colones** denominations. Additionally, a pre-existing **YOLOv8** model is used for the detection of common objects.

## ✨ Key Features
✅ **Real-time detection** of objects and bills via a camera.  
✅ **Automated payment system**, adding up the entered bills.  
✅ **Interactive display** with three sections on the screen:
   - 📦 **Main Section**: Detects placed products.
   - 💵 **Bill Section**: Registers the entered bills.
   - 📊 **Summary Section**: Displays detected products and their prices in colones.
✅ **Real-time interface** with automatic updates of objects and available balance.  
✅ **Payment and change management** if the balance exceeds the total purchase amount.

---

## 🔧 Installation and Requirements
### 📌 Prerequisites
Make sure you have **Python 3.12** installed and the following dependencies:


```bash
pip install opencv-python ultralytics torch torchvision torchaudio
```

## 📥 Clone the Repository
```bash
git clone https://github.com/EmersonJPJ/TiendaIA.git
cd TiendaIA
```


## 🚀 Run the Project
```bash
python Tienda.py
```

---

## 🛠️ System Usage
1. Start the camera.
2. Place the products in the main section.
3. Insert bills in the bill section and confirm each one.
4. View products and balance in real-time.
5. Confirm the purchase to complete the transaction.

## 🏗️ Technologies Used
- 🐍 Python for system implementation.
- 🎥 OpenCV for video processing.
- 🤖 YOLOv8 for object detection.
- 📡 Roboflow and Google Colab for training the bill model.
- 🔥 PyTorch as the backend for YOLOv8 detection.

---

## 🤝 Contributing

Contributions are always welcome! If you have suggestions, improvements, or bug fixes, feel free to open an issue or create a pull request.

---


## ✨ Contact  

Feel free to reach out for any questions or suggestions!  

- 📧 **Email**: emerson04vade@gmail.com  
- 💻 **GitHub**: EmersonJPJ
