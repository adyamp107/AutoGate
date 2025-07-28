import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

from ultralytics import YOLO
import cv2
from PIL import Image, ImageTk
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import DBSCAN

import csv

import os
import threading
import queue
import re
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nusantara Infrastructure Dashboard")
        self.geometry("1510x850")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=400)
        self.grid_columnconfigure(2, weight=0, minsize=600)
        self.grid_rowconfigure(0, weight=0, minsize=30)
        self.grid_rowconfigure(1, weight=0, minsize=30)
        self.grid_rowconfigure(2, weight=1)

        self.video_cap = None
        self.video_running = False

        self.label = ctk.CTkLabel(self, text="PoC AutoGate - Vehicle Queue Simulation", font=("Arial", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="nsew")

        self.input_vehicle_queue = ctk.CTkFrame(self, corner_radius=10)
        self.input_vehicle_queue.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nsew")

        self.browse_button = ctk.CTkButton(self.input_vehicle_queue, text="Input Folder", command=self.browse_folder)
        self.browse_button.pack(side='left', padx=(0, 5))
        # .grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nsw")

        self.start_button = ctk.CTkButton(self.input_vehicle_queue, text="Start Simulation", command=self.play_simulation)
        self.start_button.pack(side='left', padx=5)
        # .grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nsw")

        self.show_3d_popup = ctk.CTkButton(self.input_vehicle_queue, text="Show 3D Simulation", command=self.show_3d_popup)
        self.show_3d_popup.pack(side='left', padx=5)
        # .grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nsw")

        self.selected_path = ctk.CTkLabel(self, text="No folder selected yet!", anchor="w")
        self.selected_path.grid(row=1, column=1, columnspan=2, padx=(5, 10), pady=5, sticky="nsw")

        # =================== LEFT PANEL: LiDAR ===================

        self.lidar = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.lidar.grid(row=2, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")

        self.title_lidar = ctk.CTkLabel(self.lidar, text="LiDAR", font=("Arial", 16))
        self.title_lidar.pack(padx=10, pady=5)

        self.fig_queue_lidar = plt.Figure(figsize=(5, 3), dpi=100)
        self.ax_queue_lidar = self.fig_queue_lidar.add_subplot(111)
        self.ax_queue_lidar.set_title("\nVehicle Queue")
        self.ax_queue_lidar.scatter([], [])
        self.line_vehicle_lidar = self.ax_queue_lidar.axvline(x=0, color='red', linestyle='--', linewidth=1)
        self.ax_queue_lidar.axis("off")
        self.fig_queue_lidar.tight_layout(pad=0)
        self.canvas_queue_lidar = FigureCanvasTkAgg(self.fig_queue_lidar, master=self.lidar)
        self.canvas_queue_lidar.draw()
        self.canvas_queue_lidar.get_tk_widget().pack(padx=10, pady=5)

        self.fig_vehicle_lidar = plt.Figure(figsize=(5, 3), dpi=100)
        self.ax_vehicle_lidar = self.fig_vehicle_lidar.add_subplot(111)
        self.ax_vehicle_lidar.set_title("\nGet Vehicle")
        self.ax_vehicle_lidar.scatter([], [])
        self.line_axles_lidar = self.ax_vehicle_lidar.axhline(y=0, color='red', linestyle='--', linewidth=1)
        self.ax_vehicle_lidar.axis("off")
        self.fig_vehicle_lidar.tight_layout(pad=0)
        self.canvas_vehicle_lidar = FigureCanvasTkAgg(self.fig_vehicle_lidar, master=self.lidar)
        self.canvas_vehicle_lidar.draw()
        self.canvas_vehicle_lidar.get_tk_widget().pack(padx=10, pady=5)

        self.info_lidar1 = ctk.CTkLabel(self.lidar, text="DBSCAN (Density-Based Spatial Clustering of Applications with Noise)")
        self.info_lidar1.pack(padx=10, pady=5)

        self.info_lidar2 = ctk.CTkLabel(self.lidar, text="Max Z axis")
        self.info_lidar2.pack(padx=10, pady=5)

        # =================== MIDDLE PANEL: CCTV ===================

        self.cctv = ctk.CTkFrame(self, corner_radius=10)
        self.cctv.grid(row=2, column=1, padx=5, pady=(5, 10), sticky="nsew")

        self.title_cctv = ctk.CTkLabel(self.cctv, text="CCTV", font=("Arial", 16))
        self.title_cctv.pack(padx=10, pady=(10, 5))

        self.model_yolo_selected = YOLO("model/yolov8x.pt")  # default awal

        self.image_label_cctv = ctk.CTkLabel(self.cctv, text="The image will appear here!")
        self.image_label_cctv.pack(padx=10, pady=5)

        self.yolo_model_var = ctk.StringVar(value="yolov8x")
        self.yolo_dropdown = ctk.CTkOptionMenu(
            self.cctv,
            values=["yolov8n", "yolov8s", "yolov8m", "yolov8l", "yolov8x"],
            variable=self.yolo_model_var,
            command=self.change_model
        )
        self.yolo_dropdown.pack(padx=10, pady=5)

        self.info_cctv = ctk.CTkLabel(self.cctv, text="YOLOv8x (You Only Look Once)")
        self.info_cctv.pack(padx=10, pady=5)

        self.textbox_yolo_info = ctk.CTkTextbox(self.cctv, width=380, height=150)
        self.textbox_yolo_info.pack(padx=0, pady=(10, 5))
        self.textbox_yolo_info.configure(font=("Courier New", 11))
        self.textbox_yolo_info.insert("0.0", 
            "YOLOv8 Model Info\n"
            "=======================================================\n"
            "| Model   | Kelebihan           | Kekurangan          |\n"
            "|---------|---------------------|---------------------|\n"
            "| yolov8n | Cepat, ringan       | Akurasi rendah      |\n"
            "| yolov8s | Real-time ringan    | Kurang akurat       |\n"
            "| yolov8m | Performa seimbang   | Agak berat          |\n"
            "| yolov8l | Akurasi tinggi      | Butuh GPU besar     |\n"
            "| yolov8x | Akurasi terbaik     | Sangat berat/lambat |\n"
        )

        # =================== RIGHT PANEL: CLASS ===================

        self.vehicles = ctk.CTkFrame(self, corner_radius=10)
        self.vehicles.grid(row=2, column=2, padx=(5, 10), pady=(5, 10), sticky="nsew")

        # self.info_vehicles_data = ctk.CTkLabel(self.vehicles, text="Vehicles Data")
        # self.info_vehicles_data.pack(padx=10, pady=5)

        self.textbox_vehicles_data = ctk.CTkTextbox(self.vehicles, width=570, height=300)
        self.textbox_vehicles_data.pack(padx=0, pady=(10, 5))
        self.textbox_vehicles_data.configure(font=("Courier New", 12))
        self.textbox_vehicles_data.insert("0.0", "Vehicles data will appear here...\n")

        # self.info_expected_predictions = ctk.CTkLabel(self.vehicles, text="Expected Predictions")
        # self.info_expected_predictions.pack(padx=10, pady=5)

        self.textbox_expected_predictions = ctk.CTkTextbox(self.vehicles, width=570, height=410)
        self.textbox_expected_predictions.pack(padx=0, pady=5)
        self.textbox_expected_predictions.configure(font=("Courier New", 12))
        self.textbox_expected_predictions.insert("0.0", "Expected predictions will appear here...\n")

        # =================== STATE ===================

        self.loaded_pcd = None
        self.loaded_points = []
        self.count_vehicles = -1

        self.vehicles_data = []
        self.image_files = []
        self.expected_predictions = []

        # ============================================

        # Sliding window parameters
        self.window_start = 0.0
        self.window_width = 8.0
        self.slide_step = 0.25

        # ============================================

        self.vehicle_grid_size = 0.05
        self.threshold_point_count = 10
        self.threshold_detect_vehicle = self.window_width - 0.1
        self.threshold_detect_axles = 0.15
        self.timer_milisecond = 50

        # ============================================

        self.image_task_queue = queue.Queue()
        self.image_worker_thread = threading.Thread(target=self.image_worker, daemon=True)
        self.image_worker_thread.start()

        self.check_vehicle_queue = queue.Queue()
        self.check_vehicle_thread = threading.Thread(target=self.check_vehicle_worker, daemon=True)
        self.check_vehicle_thread.start()

    def natural_key(self, s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        self.selected_path.configure(text=folder_path)

        # Cari .pcd
        pcd_path = os.path.join(folder_path, "vehicle_queue.pcd")
        if not os.path.isfile(pcd_path):
            self.selected_path.configure(text="vehicle_queue.pcd not found!")
            return

        # Cari semua gambar di images/
        images_folder = os.path.join(folder_path, "images")
        if not os.path.isdir(images_folder):
            self.selected_path.configure(text="Folder 'images/' not found!")
            return

        image_files = sorted([
            os.path.join(images_folder, f)
            for f in os.listdir(images_folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ], key=lambda x: self.natural_key(os.path.basename(x)))

        if len(image_files) == 0:
            self.selected_path.configure(text="There are no images in the 'images/' folder!")
            return

        self.image_files = image_files
        self.vehicle_images = []
        for path in image_files:
            try:
                img = cv2.imread(path)
                if img is not None:
                    self.vehicle_images.append(img)
                else:
                    print(f"❌ Failed to read image: {path}")
            except Exception as e:
                print(f"Failed to open image: {path}\n{e}")

        # Load expected_predictions.csv
        expected_csv_path = os.path.join(folder_path, "expected_predictions.csv")
        if os.path.isfile(expected_csv_path):
            try:
                with open(expected_csv_path, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Optional: bersihkan tanda kutip di field Type kalau perlu
                        row['Type'] = row['Type'].strip("'\"")
                        self.expected_predictions.append(row)
                self.update_expected_predictions_textbox()
                print(f"Loaded expected predictions from {expected_csv_path}")
            except Exception as e:
                print(f"Failed to read expected_predictions.csv: {e}")
        else:
            print("expected_predictions.csv not found in folder.")

        self.load_point_cloud_data(pcd_path)

    def play_simulation(self):
        if self.loaded_points is None or len(self.loaded_points) == 0:
            return

        # Reset state
        self.window_start = 0.0
        self.count_vehicles = -1
        self.vehicles_data = []
        self.vehicle_active = False
        self.vehicle_start_pos = None

        # Clear gambar YOLO
        self.image_label_cctv.configure(image="", text="The image will appear here!")
        self.image_label_cctv.image = None

        # Clear textbox klasifikasi
        self.textbox_vehicles_data.configure(state="normal")
        self.textbox_vehicles_data.delete("1.0", tk.END)
        self.textbox_vehicles_data.insert("0.0", "Vehicle data will appear here...\n")

        # Clear grafik LiDAR Queue
        self.ax_queue_lidar.clear()
        self.ax_queue_lidar.set_title("\nVehicle Queue")
        self.ax_queue_lidar.axis("off")
        self.canvas_queue_lidar.draw()

        # Clear grafik Vehicle LiDAR
        self.ax_vehicle_lidar.clear()
        self.ax_vehicle_lidar.set_title("\nGet Vehicle")
        self.ax_vehicle_lidar.axis("off")
        self.canvas_vehicle_lidar.draw()

        # Kosongkan queue pekerjaan jika ada tersisa
        with self.image_task_queue.mutex:
            self.image_task_queue.queue.clear()
        with self.check_vehicle_queue.mutex:
            self.check_vehicle_queue.queue.clear()

        # Mulai ulang animasi sliding window
        self.animate_sliding_window()

    def show_3d_popup(self):
        if self.loaded_pcd is not None:
            vis = o3d.visualization.Visualizer()
            vis.create_window(window_name='Point Cloud Viewer', width=1300, height=800)
            vis.add_geometry(self.loaded_pcd)

            vis.poll_events()
            vis.update_renderer()

            # Atur kamera
            ctr = vis.get_view_control()
            ctr.set_zoom(0.05)
            ctr.set_front([1, 0, 0])
            ctr.set_lookat([0, 0, 0])
            ctr.set_up([0, 0, 1])

            vis.run()
            vis.destroy_window()
        else:
            self.selected_path.configure(text="No folder selected yet!")

    def change_model(self, choice):
        try:
            model_path = f"model/{choice}.pt"
            self.model_yolo_selected = YOLO(model_path)
            self.info_cctv.configure(text=f"YOLOv8{choice[-1].lower()} (You Only Look Once)")
            print(f"Model switched to: {model_path}")
        except Exception as e:
            print(f"Failed to load model {choice}: {e}")
            self.model_yolo_selected = None

    def update_expected_predictions_textbox(self):
        self.textbox_expected_predictions.configure(font=("Courier New", 12))

        header = (
            f"| {'ID':<3} | {'Axles':<5} | {'Target':<6} | {'Err':<3} | "
            f"{'Type':<5} | {'Target':<6} | {'Err':<3} | "
            f"{'Class':<5} | {'Target':<6} | {'Err':<3} |"
        )
        separator = "-" * len(header)

        rows = []

        # Error counters
        total_axles = error_axles = 0
        total_type = error_type = 0
        total_class = error_class = 0

        # Time accumulators
        dbscan_times = []
        yolo_times = []
        class_times = []

        # Loop through expected predictions
        for expected in self.expected_predictions:
            vid = int(expected.get('ID', -1))

            axles_target = expected.get('Axles', '-')
            type_target = expected.get('Type', '-').strip("'\"")
            class_target = expected.get('Class', '-')

            pred = next((v for v in self.vehicles_data if v['id'] == vid), None)

            if pred:
                axles_pred = pred.get('total_axles', '-')
                type_pred = pred.get('vehicle_type', '-')
                class_pred = pred.get('vehicle_class', '-')

                # Accumulate processing times if available
                try:
                    dbscan_times.append(pred['dbscan_time_end'] - pred['dbscan_time_start'])
                except: pass
                try:
                    yolo_times.append(pred['yolo_time_end'] - pred['yolo_time_start'])
                except: pass
                try:
                    class_times.append(pred['total_time_end'] - pred['total_time_start'])
                except: pass
            else:
                axles_pred = type_pred = class_pred = '-'

            def check_error(pred_val, target_val):
                if pred_val == '-' or target_val == '-':
                    return '-'
                return 'no' if str(pred_val) == str(target_val) else 'yes'

            axles_err = check_error(axles_pred, axles_target)
            type_err = check_error(type_pred, type_target)
            class_err = check_error(class_pred, class_target)

            if axles_err != '-':
                total_axles += 1
                if axles_err == 'yes':
                    error_axles += 1
            if type_err != '-':
                total_type += 1
                if type_err == 'yes':
                    error_type += 1
            if class_err != '-':
                total_class += 1
                if class_err == 'yes':
                    error_class += 1

            row = (
                f"| {vid:<3} | "
                f"{axles_pred:<5} | {axles_target:<6} | {axles_err:<3} | "
                f"{type_pred:<5} | {type_target:<6} | {type_err:<3} | "
                f"{class_pred:<5} | {class_target:<6} | {class_err:<3} |"
            )
            rows.append(row)

        table_text = header + "\n" + separator + "\n" + "\n".join(rows)

        def percent_error(err_count, total_count):
            return f"{(err_count / total_count * 100):.2f}%" if total_count > 0 else "N/A"

        def average_time(times):
            return f"{(sum(times) / len(times)):.2f}s" if times else "N/A"

        # Calculate error percentages
        error_axles_pct = percent_error(error_axles, total_axles)
        error_type_pct = percent_error(error_type, total_type)
        error_class_pct = percent_error(error_class, total_class)

        # Calculate average times
        avg_dbscan_time = average_time(dbscan_times)
        avg_yolo_time = average_time(yolo_times)
        avg_class_time = average_time(class_times)

        # Footer with percentages and times
        footer = (
            "\n\n"
            f"Axles error percentage (ML - DBSCAN): {error_axles_pct}\n"
            f"Type error percentage (ML - YOLOv8): {error_type_pct}\n"
            f"Class error percentage (Regular Algorithm): {error_class_pct}\n\n"
            f"Average DBSCAN time (ML - DBSCAN): {avg_dbscan_time}\n"
            f"Average YOLOv8 time (ML - YOLOv8): {avg_yolo_time}\n"
            f"Average total time: {avg_class_time}\n"
        )

        full_text = table_text + footer

        self.textbox_expected_predictions.configure(state="normal")
        self.textbox_expected_predictions.delete("1.0", tk.END)
        self.textbox_expected_predictions.insert(tk.END, full_text)
        self.textbox_expected_predictions.see("end")

    def update_vehicles_data_textbox(self):
        def format_time(start, end):
            if isinstance(start, float) and isinstance(end, float):
                return f"{end - start:.2f}s"
            return "-"

        # Pastikan textbox pakai font monospaced biar rapi
        self.textbox_vehicles_data.configure(font=("Courier New", 12))

        # Header kolom dengan lebar tetap
        header = (
            f"| {'ID':<3} | {'Axles':<5} | {'Height':<6} | {'Type':<5} | {'Class':<5} | "
            f"{'DBSCAN(s)':<9} | {'YOLOv8(s)':<9} | {'Total(s)':<9} |"
        )
        separator = "-" * len(header)

        rows = []
        for v in self.vehicles_data:
            row = (
                f"| {v['id']:<3} | "
                f"{v['total_axles']:<5} | "
                f"{v['max_height']:<6} | "
                f"{v['vehicle_type']:<5} | "
                f"{str(v['vehicle_class']):<5} | "
                f"{format_time(v.get('dbscan_time_start'), v.get('dbscan_time_end')):<9} | "
                f"{format_time(v.get('yolo_time_start'), v.get('yolo_time_end')):<9} | "
                f"{format_time(v.get('total_time_start'), v.get('total_time_end')):<9} |"
            )
            rows.append(row)

        table_text = header + "\n" + separator + "\n" + "\n".join(rows)

        self.textbox_vehicles_data.configure(state="normal")
        self.textbox_vehicles_data.delete("1.0", tk.END)
        self.textbox_vehicles_data.insert(tk.END, table_text)
        self.textbox_vehicles_data.see("end")

        self.update_expected_predictions_textbox()

    def load_point_cloud_data(self, file_path):
        try:
            pcd = o3d.io.read_point_cloud(file_path)
            self.loaded_pcd = pcd
            points = np.asarray(pcd.points).copy()

            if points.shape[0] == 0:
                self.selected_path.configure(text="Empty file", anchor="w")
                return
            
            # Transformasi: X = 0, Y & Z mulai dari 0
            points[:, 0] = 0
            points[:, 1] -= points[:, 1].min() - 15
            points[:, 2] -= points[:, 2].min()

            # Snap koordinat Y dan Z ke grid
            points[:, 1] = np.round(points[:, 1] / self.vehicle_grid_size) * self.vehicle_grid_size
            points[:, 2] = np.round(points[:, 2] / self.vehicle_grid_size) * self.vehicle_grid_size

            # Hapus titik duplikat berdasarkan (Y, Z)
            _, unique_indices = np.unique(points[:, 1:3], axis=0, return_index=True)
            points = points[unique_indices]

            # Simpan hasil
            self.loaded_points = points

            self.window_start = 0.0
            self.selected_path.configure(text=f"Loaded: {file_path}", anchor="w")
            self.selected_path.configure(wraplength=1000)

        except Exception as e:
            self.selected_path.configure(text=f"Error: {str(e)}", anchor="w")
            self.selected_path.configure(wraplength=800)

    def animate_sliding_window(self):
        if self.loaded_points is None or len(self.loaded_points) == 0:
            return

        y_start = self.window_start
        y_end = y_start + self.window_width

        # Ambil titik dalam window Y
        window_pts = self.loaded_points[
            (self.loaded_points[:, 1] >= y_start) & (self.loaded_points[:, 1] < y_end)
        ]

        self.ax_queue_lidar.clear()
        self.ax_queue_lidar.axis("off")
        self.ax_queue_lidar.set_title(f"\nVehicle Queue Sliding {y_start:.2f}m → {y_end:.2f}m")
        self.ax_queue_lidar.scatter(window_pts[:, 1], window_pts[:, 2], s=2, c='blue')

        # Garis vertikal sliding window (posisi deteksi kendaraan)
        self.line_vehicle_lidar = self.ax_queue_lidar.axvline(x=self.window_start + self.threshold_detect_vehicle, color='red', linestyle='--', linewidth=1)

        # Batas axis tetap agar tidak berubah ubah
        y_max = self.loaded_points[:, 1].max()
        z_min = 0
        z_max = self.loaded_points[:, 2].max()
        self.ax_queue_lidar.set_xlim(y_start, y_end)
        self.ax_queue_lidar.set_ylim(z_min, z_max)
        self.ax_queue_lidar.set_aspect('auto')

        self.fig_queue_lidar.tight_layout(pad=0)
        self.canvas_queue_lidar.draw()

        # DETEKSI KENDARAAN berdasarkan titik dekat garis vertikal (detect_x)
        self.detect_vehicle(self.window_start + self.threshold_detect_vehicle)

        # Geser sliding window
        self.window_start += self.slide_step
        if self.window_start <= y_max + 1.0:
            self.after(self.timer_milisecond, self.animate_sliding_window)
        
    def detect_vehicle(self, threshold_detect_vehicle):
        threshold_x = 0.1

        # Window present: window sliding saat ini
        present_points = self.loaded_points[
            (self.loaded_points[:, 1] >= self.window_start) &
            (self.loaded_points[:, 1] < self.window_start + self.window_width) &
            (np.abs(self.loaded_points[:, 1] - threshold_detect_vehicle) < threshold_x)
        ]

        # Window future: window sliding berikutnya
        future_start = self.window_start + self.slide_step
        future_points = self.loaded_points[
            (self.loaded_points[:, 1] >= future_start) &
            (self.loaded_points[:, 1] < future_start + self.window_width) &
            (np.abs(self.loaded_points[:, 1] - (threshold_detect_vehicle + self.slide_step)) < threshold_x)
        ]

        point_count_present = len(present_points)
        point_count_future = len(future_points)

        if not hasattr(self, "vehicle_active"):
            self.vehicle_active = False
            self.vehicle_start_pos = None

        if point_count_present >= self.threshold_point_count:
            # Kendaraan mulai terdeteksi
            if not self.vehicle_active:
                self.vehicle_active = True
                self.vehicle_start_pos = np.min(present_points[:, 1])
                self.count_vehicles += 1
                vehicle_data = {
                    'id': self.count_vehicles,
                    'total_axles': 0,
                    'max_height': 0,
                    'vehicle_type': "-",
                    'vehicle_class': "-",
                    'yolo_time_start': '-',
                    'yolo_time_end': '-',
                    'dbscan_time_start': '-',
                    'dbscan_time_end': '-',
                    'total_time_start': '-',
                    'total_time_end': '-'
                }
                self.vehicles_data.append(vehicle_data)
                self.vehicles_data[self.count_vehicles]['total_time_start'] = time.time()
                # self.show_vehicle_image()
                self.image_task_queue.put(self.count_vehicles)
        else:
            if self.vehicle_active:
                # Jika titik di future == 0 maka langsung tutup
                if point_count_future == 0:
                    vehicle_end_pos = np.max(present_points[:, 1]) if len(present_points) > 0 else self.window_start + self.window_width
                else:
                    # Bisa ganti logika lain kalau future_points ada, tapi present_points kosong
                    vehicle_end_pos = np.max(future_points[:, 1])

                self.image_label_cctv.configure(image="", text="The image will appear here!")
                self.image_label_cctv.image = None  # pastikan referensi gambar dihapus

                vehicle_points = self.loaded_points[
                    (self.loaded_points[:, 1] >= self.vehicle_start_pos) &
                    (self.loaded_points[:, 1] <= vehicle_end_pos)
                ]

                vehicle_points = self.loaded_points[
                    (self.loaded_points[:, 1] >= self.vehicle_start_pos) &
                    (self.loaded_points[:, 1] <= vehicle_end_pos)
                ]

                vehicle_points[:, 2] = vehicle_points[:, 2] - vehicle_points[:, 2].min()

                self.vehicles_data[self.count_vehicles]['dbscan_time_start'] = time.time()
                total_axles = self.count_axles(vehicle_points)
                self.vehicles_data[self.count_vehicles]['total_axles'] = total_axles
                self.vehicles_data[self.count_vehicles]['dbscan_time_end'] = time.time()

                max_height = self.get_height(vehicle_points)
                self.vehicles_data[self.count_vehicles]['max_height'] = max_height

                self.ax_vehicle_lidar.clear()
                self.ax_vehicle_lidar.axis("off")
                self.ax_vehicle_lidar.set_title(f"\nGet Vehicle: {self.vehicle_start_pos:.2f} → {vehicle_end_pos:.2f} m")
                self.ax_vehicle_lidar.scatter(vehicle_points[:, 1], vehicle_points[:, 2], s=2, c='green')
                self.line_axles_lidar = self.ax_vehicle_lidar.axhline(y=self.threshold_detect_axles, color='red', linestyle='--', linewidth=1)

                z_min = 0
                z_max = self.loaded_points[:, 2].max()
                self.ax_vehicle_lidar.set_ylim(z_min, z_max)
                self.ax_vehicle_lidar.set_xlim(self.vehicle_start_pos, vehicle_end_pos)
                self.ax_vehicle_lidar.set_aspect('equal')
                self.fig_vehicle_lidar.tight_layout(pad=0)
                self.canvas_vehicle_lidar.draw()

                self.update_vehicles_data_textbox()
                self.check_vehicle_queue.put(self.count_vehicles)

                self.vehicle_active = False
                self.vehicle_start_pos = None
                self.totalAxles = 0
                self.maxHeight = 0

        self.update_vehicles_data_textbox()

    def count_axles(self, vehicle_points):
        if not len(vehicle_points):
            return 0

        close_points = vehicle_points[np.abs(vehicle_points[:, 2]) < self.threshold_detect_axles]

        if close_points.size == 0:
            return 0

        if len(close_points[:, 1:3]) == 0:
            return 0
        
        db = DBSCAN(eps=0.25, min_samples=5).fit(close_points[:, 1:3])
        labels = db.labels_

        return len(set(labels)) - (1 if -1 in labels else 0)

    def get_height(self, vehicle_points):
        if vehicle_points is not None and len(vehicle_points) > 0:
            return round(np.max(vehicle_points[:, 2]), 2)
        else:
            return 0

    def image_worker(self):
        while True:
            vehicle_index = self.image_task_queue.get()
            try:
                self.show_vehicle_image(vehicle_index)
            except Exception as e:
                print(f"Error while processing the {vehicle_index + 1} vehicle image: {e}")
            self.image_task_queue.task_done()

    def show_vehicle_image(self, vehicle_index):
        img_idx = vehicle_index % len(self.vehicle_images)
        if 0 <= img_idx < len(self.vehicle_images):
            img_rgb = cv2.cvtColor(self.vehicle_images[img_idx], cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            max_width, max_height = 400, 240
            scale_ratio = min(max_width / pil_img.width, max_height / pil_img.height)
            resized_img = pil_img.resize((int(pil_img.width * scale_ratio), int(pil_img.height * scale_ratio)))
            ctk_image = ctk.CTkImage(light_image=resized_img, size=resized_img.size)
            self.image_label_cctv.image = ctk_image  # keep reference
            self.image_label_cctv.configure(image=ctk_image, text="")

            # Pastikan index valid untuk vehicles_data
            if 0 <= vehicle_index < len(self.vehicles_data):
                self.vehicles_data[vehicle_index]['yolo_time_start'] = time.time()
                vehicle_type = self.predict_vehicle_type(self.vehicle_images[img_idx])
                self.vehicles_data[vehicle_index]['vehicle_type'] = vehicle_type
                self.vehicles_data[vehicle_index]['yolo_time_end'] = time.time()
                self.update_vehicles_data_textbox()
                self.check_vehicle_queue.put(vehicle_index)
        else:
            print(f"There are no images for the {img_idx + 1} vehicle")

    def predict_vehicle_type(self, img):
        if self.model_yolo_selected is None:
            return "-"
        
        results = self.model_yolo_selected(img)[0]

        vehicle_classes = ['car', 'truck', 'bus']
        best_label = "-"
        highest_score = 0

        if not results.boxes or len(results.boxes) == 0:
            return "-"

        for box in results.boxes:

            if len(box.cls) == 0 or len(box.conf) == 0:
                continue
    
            class_id = int(box.cls[0].item())
            label = results.names[class_id]
            score = float(box.conf[0].item())

            if label not in vehicle_classes:
                continue

            if score > highest_score:
                highest_score = score
                best_label = label

        return best_label

    def check_vehicle_worker(self):
        while True:
            vehicle_index = self.check_vehicle_queue.get()
            try:
                self.check_vehicle_completeness(vehicle_index)
            except Exception as e:
                print(f"Error while checking the {vehicle_index} vehicle: {e}")
            self.check_vehicle_queue.task_done()

    def check_vehicle_completeness(self, vehicle_index):
        vehicle = self.vehicles_data[vehicle_index]
        required_keys = ['total_axles', 'max_height', 'vehicle_type']
        if all(k in vehicle and vehicle[k] not in [None, '-', 0] for k in required_keys):
            if vehicle['max_height'] < 2.2:
                self.vehicles_data[vehicle_index]['vehicle_class'] = 1
            elif vehicle['vehicle_type'].lower() == 'bus':
                self.vehicles_data[vehicle_index]['vehicle_class'] = 1
            elif vehicle['total_axles'] == 2:
                self.vehicles_data[vehicle_index]['vehicle_class'] = 2
            elif vehicle['total_axles'] == 3:
                self.vehicles_data[vehicle_index]['vehicle_class'] = 3
            elif vehicle['total_axles'] == 4:
                self.vehicles_data[vehicle_index]['vehicle_class'] = 4
            elif vehicle['total_axles'] >= 5:
                self.vehicles_data[vehicle_index]['vehicle_class'] = 5
            self.vehicles_data[vehicle_index]['total_time_end'] = time.time()
            self.update_vehicles_data_textbox()
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
