# Braille Reader - Setup and Run Instructions

This guide provides complete step-by-step instructions to set up and run Braille Reader on a fresh machine.

### Step 1: Set Up Python Virtual Environment

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

2. **Activate virtual environment:**
   ```bash
   .venv\Scripts\activate
   ```
   - You should see `(.venv)` in your command prompt

### Step 2: Install Python Dependencies

1. **Install required packages:**
   ```bash
   pip install flask==2.3.3
   pip install flask-wtf
   pip install flask-mobility
   pip install werkzeug==2.3.7
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   pip install numpy==1.26.4
   pip install opencv-python
   pip install pillow
   pip install albumentations
   pip install imgaug
   pip install PyMuPDF
   pip install matplotlib
   pip install scipy
   ```

2. **Verify installations:**
   ```bash
   pip list
   ```

### Step 3: Download Neural Network Model

1. **Create weights directory (if not exists):**
   ```bash
   mkdir weights
   ```

2. **Download the model file:**
   ```bash
   cd weights
   curl -L -o model.t7 http://ovdv.ru/files/retina_chars_eced60.clr.008
   cd ..
   ```

   **Alternative (if curl is not available):**
   - Open browser and go to: http://ovdv.ru/files/retina_chars_eced60.clr.008
   - Save the file as `model.t7` in the `weights` folder

## 🚀 Running the Application

### Method 1: Using the Run Script (Recommended)

1. **Make sure virtual environment is activated:**
   ```bash
   .venv\Scripts\activate
   ```

2. **Run the application:**
   ```bash
   python run_web_app.py --debug
   ```

### Method 2: Direct Flask Run

1. **Set environment variables:**
   ```bash
   set FLASK_APP=web_app.angelina_reader_app
   set FLASK_ENV=development
   ```

2. **Run Flask:**
   ```bash
   python -m flask run --host=0.0.0.0 --port=5001
   ```

## 🌐 Access the Application

Once running, open your web browser and go to:

- **Local access:** http://127.0.0.1:5001
- **Network access:** http://[YOUR-IP]:5001

To find your IP address:
```bash
ipconfig
```
Look for "IPv4 Address" under your active network connection.

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: "Python is not recognized"
**Solution:** Reinstall Python and ensure "Add Python to PATH" is checked.

#### Issue: "git is not recognized"
**Solution:** Reinstall Git or add Git to your system PATH manually.

#### Issue: "Module not found" errors
**Solution:** 
1. Ensure virtual environment is activated
2. Reinstall the missing package: `pip install [package-name]`

#### Issue: "Model file not found"
**Solution:** 
1. Check if `weights/model.t7` exists (should be ~144MB)
2. Re-download the model file
3. Ensure the file is in the correct location

#### Issue: "Port already in use"
**Solution:** 
1. Change the port number: `python run_web_app.py --port 5002`
2. Or kill existing Python processes: `taskkill /f /im python.exe`

#### Issue: Virtual environment activation fails
**Solution:**
1. Delete `.venv` folder
2. Recreate: `python -m venv .venv`
3. Reactivate: `.venv\Scripts\activate`

## 📁 Project Structure

After setup, your directory should look like:
```
AngelinaReader/
├── .venv/                  # Virtual environment
├── web_app/               # Web application files
├── weights/               # Neural network model
│   └── model.t7          # Downloaded model file
├── pytorch_retinanet/     # Git submodule
├── louis.py              # Mock library
├── run_web_app.py        # Main run script
└── requirements.txt       # Dependencies list
```

## 🔄 Daily Usage

For subsequent runs on the same machine:

1. **Open Command Prompt/PowerShell**
2. **Navigate to project:**
   ```bash
   cd C:\Projects\BrailleReader
   ```
3. **Activate environment:**
   ```bash
   .venv\Scripts\activate
   ```
4. **Run application:**
   ```bash
   python run_web_app.py --debug
   ```

## 🛑 Stopping the Application

To stop the application:
- Press `Ctrl+C` in the terminal
- Or close the terminal window

## 📝 Notes

- **First run** may take longer as the neural network model loads
- **File uploads** are processed locally - no data is sent to external servers
- **Supported formats:** JPG, PNG, PDF, ZIP files
- **Image requirements:** Minimum 1000x1000 pixels for best results
- **Privacy:** All processing is done locally on your machine

## 🆘 Getting Help

If you encounter issues:

1. **Check the terminal output** for error messages
2. **Verify all installation steps** were completed
3. **Ensure virtual environment is activated** before running
4. **Check network connectivity** for model download

## 🎯 Success Verification

Your setup is successful if:
- ✅ Application starts without errors
- ✅ Web interface loads at http://127.0.0.1:5001
- ✅ You can upload and process Braille images
- ✅ Text-to-speech functionality works
- ✅ Results are displayed correctly

---

**Congratulations!** You now have Braille Reader running on your machine. The application provides fast, accurate Braille text recognition with a modern, user-friendly interface.
