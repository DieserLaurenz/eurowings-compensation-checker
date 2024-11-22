# Eurowings Compensation Checker

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### **1. Clone the Repository**
Use the following command to clone the repository:

```bash
git clone https://github.com/DieserLaurenz/eurowings-compensation-checker.git
cd eurowings-compensation-checker
```

---

### **2. Create a Virtual Environment**
Create and activate a Python virtual environment:

- **On Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

---

### **3. Install Required Dependencies**
Install the necessary Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### **4. Configure Environment Variables**
1. Open the file `.env.example` and fill in the required values:

   ```env
   FLIGHT_NUMBER=         # Example: 981
   DEPARTURE_DATE=        # Format: YYYY-MM-DD (e.g., 2024-09-06)
   AIRLINE_CODE=          # Example: EW
   NAME=                  # Example: John
   SURNAME=               # Example: Doe
   EMAIL=                 # Example: John.Doe@example.com
   BOOKING_CODE=          # Example: ABCDEF
   ```

2. Rename `.env.example` to `.env`:

   ```bash
   mv .env.example .env
   ```

---

### **5. Run the Script**
Execute the script to check the current compensation status:

```bash
python src/eurowings-compensation-checker.py
```

---

## ⚠️ Disclaimer

- This tool automates web scraping to interact with the Eurowings claim system.
- **Use it responsibly** and in accordance with Eurowings' terms and conditions.
- The author assumes **no liability** for any misuse, errors, or potential issues caused by this script.
- This tool is provided **"as-is"**, without warranty of any kind.

---

## 🛠 Contributing
Feel free to submit issues, fork the repository, or suggest improvements via pull requests.

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

With this README, users can easily set up, configure, and run your tool while being informed about responsibilities and limitations. 🚀
