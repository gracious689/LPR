# Tesseract OCR Setup - Quick Guide

## You Have Source Code, Need Executable

Your current path: `C:\Users\hp\Downloads\5.5.2 source code\tesseract-ocr-tesseract-9c516f4`
This is the source code, not the compiled program.

## Quick Solution: Download Pre-compiled Executable

### Step 1: Download Installer
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Scroll down to "Tesseract at UB Mannheim"
3. Download: **tesseract-ocr-w64-setup-5.5.2-20240612.exe** (or latest 64-bit version)

### Step 2: Install
1. Run the downloaded installer
2. Choose installation location (default: `C:\Program Files\Tesseract-OCR`)
3. **IMPORTANT**: Check "Add Tesseract to your PATH" during installation

### Step 3: Update .env File
After installation, update your `.env` file with the correct path:

```env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Step 4: Verify Installation
Open Command Prompt and run:
```cmd
tesseract --version
```

You should see: `tesseract 5.5.2`

## Alternative: Use Chocolatey (if installed)
```cmd
choco install tesseract
```

## Alternative: Use Winget (if available)
```cmd
winget install UB-Mannheim.TesseractOCR
```

---

## After Tesseract is Installed:

1. Update `.env` with correct path
2. Run test again: `python test_system.py`
3. Then setup Supabase and complete the system
