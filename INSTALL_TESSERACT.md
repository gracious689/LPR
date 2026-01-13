# Tesseract OCR Installation Guide

## Windows Installation

### Option 1: Download Installer (Recommended)
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download the latest Windows installer (64-bit recommended)
3. Run the installer
4. **Important**: During installation, make sure to check "Add Tesseract to your PATH"
5. Note the installation path (usually: `C:\Program Files\Tesseract-OCR`)

### Option 2: Using Chocolatey
If you have Chocolatey installed:
```bash
choco install tesseract
```

### Option 3: Using Winget
```bash
winget install UB-Mannheim.TesseractOCR
```

## Verify Installation

After installation, open a new Command Prompt and run:
```bash
tesseract --version
```

You should see version information if installed correctly.

## Update .env File

Make sure your `.env` file has the correct Tesseract path:
```env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

If you installed to a different location, update the path accordingly.

## Troubleshooting

### "tesseract is not recognized" error:
- Restart your terminal/command prompt after installation
- Make sure Tesseract was added to PATH during installation
- Manually add Tesseract to Windows PATH if needed

### Path Issues:
- Verify the exact path where tesseract.exe is located
- Use forward slashes or escape backslashes in the .env file
- Example: `C:/Program Files/Tesseract-OCR/tesseract.exe`
