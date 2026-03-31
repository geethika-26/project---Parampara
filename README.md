# Project Parampara

AI Based Design Variation and Product Authentication System

---

## Overview

Project Parampara is a Python based application that generates creative design variations from a given image and provides product authentication using a digital fingerprint and QR code.

This project aims to support traditional artisans by combining basic image processing techniques with creative design generation.

---

## Objectives

Generate multiple design variations from a single input image
Enhance creativity using color, brightness, and contrast changes
Create a unique fingerprint for each design
Generate a QR code for product verification

---

## Technologies Used

Python
OpenCV
NumPy
Pillow (PIL)
Matplotlib
QRCode

---

## Features

Design Variation Generator
Applies random color shifts
Adjusts brightness and contrast
Adds smoothing effects

Digital Fingerprint System
Uses ORB feature detection
Generates a unique hash for the image

QR Code Generation
Stores artisan name and product hash
Helps verify product authenticity

---

## Project Structure

project--Parampara/
Project_Parampara_Prototype.py
outputs/
designs/
qr/

---

## How to Run

Step 1 Install dependencies
pip install opencv-python pillow qrcode matplotlib numpy

Step 2 Run the program
python Project_Parampara_Prototype.py

Step 3 Provide input
Enter image file path
Enter artisan name

---

## Output

Generated design variations will be saved in outputs/designs

QR code will be saved in outputs/qr

---

## Future Improvements

Add graphical user interface
Improve design generation using advanced AI
Store product data in a database
Add real time verification system

---

## Author

## Geethika Simma
