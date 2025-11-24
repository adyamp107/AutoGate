# **AutoGate**

AutoGate is a project that combines Python-based computer vision and 3D processing with a SwiftUI application.
This repository contains two main modules:

* **Python/** — YOLO-based detection, point cloud processing, clustering, and visualization.
* **Swift/** — SwiftUI application (requires Xcode) for UI and visualization tasks.

---

## 🚀 **Getting Started (Python Module)**

### **1. Install Dependencies**

Navigate to the `Python/` directory:

```bash
cd Python
pip install -r requirements.txt
```

Make sure your Python environment (Python 3.9–3.11 recommended) is properly set up before installing.

---

### **2. Download Required Data**

Download all required data from the following Google Drive link:

🔗 **Google Drive (Models + Dataset)**
[https://drive.google.com/drive/folders/1BhKPAO_pgFkuFmesrn-IWdz-zNs0j8vg?usp=sharing](https://drive.google.com/drive/folders/1BhKPAO_pgFkuFmesrn-IWdz-zNs0j8vg?usp=sharing)

After downloading:

* Place the **model/** folder into `Python/model/`
  (contains YOLO models such as `yolov8l.pt`, `yolov8m.pt`, `yolov8n.pt`, `yolov8x.pt`)
* Place the **vehicle_queue/** folder into `Python/vehicle_queue/`
  (contains `vehicle_queue.pcd`, images, and `expected_predictions.csv`)

The Python scripts will automatically read from these directories.

---

### **3. Run the Application**

After installing dependencies and placing the dataset:

```bash
python3 main.py
```

(Or whichever script is the entry point of your project.)

---

## 📱 **Running the Swift Module**

The Swift module is located inside the `Swift/` folder.
To run:

1. Open the project using **Xcode**.
2. Build and run the SwiftUI application.

Xcode 15+ is recommended.

---

## 📂 **Project Structure**

```
AutoGate/
│
├── Python/
│   ├── model/                 # YOLO model files (.pt)
│   ├── vehicle_queue/         # Dataset: PCD files, images, CSV
│   ├── requirements.txt
│   ├── main.py                # Example entry point
│   └── (other scripts)
│
└── Swift/
    ├── (SwiftUI source files)
    └── (Xcode project)
```

---

## 📌 **Notes**

* The `.pt` YOLO model files are **not included** in this repository due to their large size. They must be downloaded from the Google Drive link provided.
* Make sure to ignore `.pt` files in your `.gitignore` to avoid large uploads.
* The Python module uses YOLOv8, Open3D, Matplotlib, Scikit-Learn, and CustomTkinter for the interface.

---

## 🛠️ **Technologies Used**

### **Python**

* YOLOv8 (Ultralytics)
* OpenCV
* Open3D
* NumPy
* Matplotlib
* CustomTkinter (GUI)
* DBSCAN (Scikit-Learn)

### **Swift**

* SwiftUI
* Xcode project structure

---

## 🤝 **Contributing**

Contributions are welcome!
Feel free to open issues or submit pull requests.
