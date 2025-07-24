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

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nusantara Infrastructure Dashboard")
        self.geometry("1400x800")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=500)
        self.grid_columnconfigure(2, weight=0, minsize=300)
        self.grid_rowconfigure(0, weight=0, minsize=50)
        self.grid_rowconfigure(1, weight=1)

        self.video_cap = None
        self.video_running = False

        self.label = ctk.CTkLabel(self, text="PoC AutoGate - Left Side Only", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="nsew")

        # =================== LEFT PANEL: LiDAR ===================
        self.lidar2d = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.lidar2d.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")

        self.title_lidar2d = ctk.CTkLabel(self.lidar2d, text="LiDAR", font=("Arial", 16))
        self.title_lidar2d.pack(padx=10, pady=(10, 5))

        self.browse_button_lidar2d = ctk.CTkButton(self.lidar2d, text="Input Dokumen (.pcd)", command=self.browse_file_pcd)
        self.browse_button_lidar2d.pack(padx=10, pady=5)

        self.selected_path_lidar2d = ctk.CTkLabel(self.lidar2d, text="Belum ada file dipilih", anchor="w")
        self.selected_path_lidar2d.pack(padx=10, pady=5)

        self.slider_lidar2d = ctk.CTkSlider(self.lidar2d, from_=0, to=100, number_of_steps=100, command=self.on_slider_change)
        self.slider_lidar2d.pack(padx=10, pady=5)

        self.fig_vehicle_left_lidar2d = plt.Figure(figsize=(5, 3), dpi=100)
        self.ax_vehicle_left_lidar2d = self.fig_vehicle_left_lidar2d.add_subplot(111)
        self.ax_vehicle_left_lidar2d.set_title("\n2D Left Side View (Y-Z)")
        self.ax_vehicle_left_lidar2d.scatter([], [])
        self.line_vehicle_left_lidar2d = self.ax_vehicle_left_lidar2d.axhline(y=0, color='red', linestyle='--', linewidth=1)
        # self.ax_vehicle_left_lidar2d.axis("off")
        self.fig_vehicle_left_lidar2d.tight_layout(pad=0)
        self.canvas_vehicle_left_lidar2d = FigureCanvasTkAgg(self.fig_vehicle_left_lidar2d, master=self.lidar2d)
        self.canvas_vehicle_left_lidar2d.draw()
        self.canvas_vehicle_left_lidar2d.get_tk_widget().pack(padx=10, pady=5)

        self.fig_histogram_left_lidar2d = plt.Figure(figsize=(5, 0.5), dpi=100)
        self.ax_histogram_left_lidar2d = self.fig_histogram_left_lidar2d.add_subplot(111)
        self.ax_histogram_left_lidar2d.axis("off")
        self.fig_histogram_left_lidar2d.tight_layout(pad=0)
        self.canvas_histogram_left_lidar2d = FigureCanvasTkAgg(self.fig_histogram_left_lidar2d, master=self.lidar2d)
        self.canvas_histogram_left_lidar2d.draw()
        self.canvas_histogram_left_lidar2d.get_tk_widget().pack(padx=10, pady=5)

        self.axle_count_left_lidar2d = ctk.CTkLabel(self.lidar2d, text="Left axle(s): -", font=("Arial", 14, "bold"))
        self.axle_count_left_lidar2d.pack(padx=10, pady=5)

        self.height_lidar2d = ctk.CTkLabel(self.lidar2d, text="maxHeight: -", font=("Arial", 14, "bold"))
        self.height_lidar2d.pack(padx=10, pady=5)

        self.show_3d_button_lidar2d = ctk.CTkButton(self.lidar2d, text="Show 3D Point Cloud", command=self.show_3d_popup)
        self.show_3d_button_lidar2d.pack(padx=10, pady=(5, 10))

        # =================== MIDDLE PANEL: YOLO ===================
        self.yolov8x = ctk.CTkFrame(self, corner_radius=10)
        self.yolov8x.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky="nsew")

        self.title_yolov8x = ctk.CTkLabel(self.yolov8x, text="YOLOv8x", font=("Arial", 16))
        self.title_yolov8x.pack(padx=10, pady=(10, 5))

        self.yolo_model = YOLO("poc/model/yolov8x.pt")

        self.select_yolo_image_button = ctk.CTkButton(self.yolov8x, text="Pilih Gambar", command=self.select_yolo_image)
        self.select_yolo_image_button.pack(pady=10)

        self.yolo_image_label = ctk.CTkLabel(self.yolov8x, text="Gambar akan muncul di sini")
        self.yolo_image_label.pack(pady=5)

        self.yolo_result_box = ctk.CTkTextbox(self.yolov8x, height=100)
        self.yolo_result_box.pack(padx=10, pady=10, fill="both")

        self.type_yolo = ctk.CTkLabel(self.yolov8x, text="vehicleType: -")
        self.type_yolo.pack(padx=10, pady=10, fill="both")

        # =================== RIGHT PANEL: CLASS ===================

        self.class_vehicle = ctk.CTkFrame(self, corner_radius=10)
        self.class_vehicle.grid(row=1, column=2, padx=10, pady=(5, 10), sticky="nsew")

        self.title_class_result = ctk.CTkLabel(self.class_vehicle, text="Class Result", font=("Arial", 16))
        self.title_class_result.pack(padx=10, pady=(10, 5))

        self.class_result = ctk.CTkLabel(self.class_vehicle, text="Class: -", font=("Arial", 14, "bold"))
        self.class_result.pack(padx=10, pady=(5, 10))

        # =================== STATE ===================
        self.loaded_pcd = None
        self.slider_value_lidar2d = 0
        self.loaded_points = []

        self.totalAxles = 0
        self.maxHeight = 0
        self.vehicleType = ""

    def browse_file_pcd(self):
        file_path = filedialog.askopenfilename(filetypes=[("PCD Files", "*.pcd")])
        if file_path:
            self.selected_path_lidar2d.configure(text=file_path)
            self.load_pointcloud(file_path)

    def load_pointcloud(self, file_path):
        try:
            pcd = o3d.io.read_point_cloud(file_path)
            points = np.asarray(pcd.points)

            if points.shape[0] == 0:
                self.selected_path_lidar2d.configure(text="File kosong")
                return
            
            points = points.copy()

            points[:, 0] = 0

            points[:, 2] -= np.min(points[:, 2])

            self.loaded_points = points
            self.loaded_pcd = pcd
            self.slider_value_lidar2d = 0.07

            self.ax_vehicle_left_lidar2d.clear()
            self.ax_vehicle_left_lidar2d.scatter(self.loaded_points[:, 1], self.loaded_points[:, 2], s=1, c='blue')
            self.ax_vehicle_left_lidar2d.set_title("\n2D Left Side View (Y-Z)")
            self.line_vehicle_left_lidar2d = self.ax_vehicle_left_lidar2d.axhline(y=self.slider_value_lidar2d, color='red', linestyle='--', linewidth=1)
            # self.ax_vehicle_left_lidar2d.axis("off")
            self.fig_vehicle_left_lidar2d.tight_layout(pad=0)
            self.canvas_vehicle_left_lidar2d.draw()

            self.count_axles()
            self.get_height()
            self.get_class_vehicle()

        except Exception as e:
            self.selected_path_lidar2d.configure(text=f"Error: {str(e)}")

    def on_slider_change(self, value):
        if not len(self.loaded_points):
            return
        min_z = np.min(self.loaded_points[:, 2])
        max_z = np.max(self.loaded_points[:, 2])
        z_mapped = min_z + (value / 100) * (max_z - min_z)
        self.slider_value_lidar2d = z_mapped
        self.line_vehicle_left_lidar2d.set_ydata([z_mapped])
        self.canvas_vehicle_left_lidar2d.draw()
        self.count_axles()

    def count_axles(self):
        if not len(self.loaded_points):
            return

        threshold = 0.06
        z_value = self.slider_value_lidar2d
        close_left_points = self.loaded_points[np.abs(self.loaded_points[:, 2] - z_value) < threshold]

        if close_left_points.size == 0:
            self.axle_count_left_lidar2d.configure(text="Left axle(s): -")
            return

        y_min = np.min(self.loaded_points[:, 1])
        y_max = np.max(self.loaded_points[:, 1])
        bins = np.linspace(y_min, y_max, 101)

        hist_left, bin_edges_left = np.histogram(close_left_points[:, 1], bins=bins)
        bin_centers_left = (bin_edges_left[:-1] + bin_edges_left[1:]) / 2

        self.ax_histogram_left_lidar2d.clear()
        bar_width = (bin_edges_left[1] - bin_edges_left[0])
        self.ax_histogram_left_lidar2d.bar(bin_centers_left, hist_left, width=bar_width, color='blue')
        self.ax_histogram_left_lidar2d.axis("off")
        self.canvas_histogram_left_lidar2d.draw()

        left_clusters = self.cluster_by_distance(close_left_points[:, 1:3])
        self.axle_count_left_lidar2d.configure(text=f"Left axle(s): {left_clusters}")

        self.totalAxles = left_clusters

    def get_height(self):
        if self.loaded_points is not None and len(self.loaded_points) > 0:
            max_height = np.max(self.loaded_points[:, 2])
            self.height_lidar2d.configure(text=f"maxHeight: {max_height:.2f} m")

            self.maxHeight = max_height
        else:
            self.height_lidar2d.configure(text="maxHeight: -")

            self.maxHeight = 0

    def cluster_by_distance(self, points_yz):
        if len(points_yz) == 0:
            return 0
        db = DBSCAN(eps=0.5, min_samples=5).fit(points_yz)
        labels = db.labels_
        return len(set(labels)) - (1 if -1 in labels else 0)

    def show_3d_popup(self):
        if self.loaded_pcd is not None:
            o3d.visualization.draw_geometries([self.loaded_pcd])
        else:
            self.selected_path_lidar2d.configure(text="Belum ada file pcd yang dimuat.")

    def select_yolo_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            img = cv2.imread(file_path)
            results = self.yolo_model(img)[0]

            boxes = results.boxes.xyxy.cpu().numpy()
            scores = results.boxes.conf.cpu().numpy()
            class_ids = results.boxes.cls.cpu().numpy()
            labels = results.names

            vehicle_classes = ['car', 'truck', 'bus', 'motorbike']
            detections = []
            for i in range(len(boxes)):
                class_id = int(class_ids[i])
                label = labels[class_id]
                if label not in vehicle_classes:
                    continue
                score = scores[i]
                detections.append(f"{label} ({score:.2f})")

            self.yolo_result_box.delete("0.0", "end")
            if detections:
                self.yolo_result_box.insert("0.0", "\n".join(detections))
            else:
                self.yolo_result_box.insert("0.0", "Tidak ada kendaraan terdeteksi.")

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            max_width, max_height = 400, 240
            scale_ratio = min(max_width / pil_img.width, max_height / pil_img.height)
            resized_img = pil_img.resize((int(pil_img.width * scale_ratio), int(pil_img.height * scale_ratio)))
            self.tk_yolo_image = ImageTk.PhotoImage(resized_img)
            self.yolo_image_label.configure(image=self.tk_yolo_image, text="")

            if detections:
                best = max(detections, key=lambda x: float(x.split('(')[-1].rstrip(')')))
                vehicle_type = best.split()[0]
                conf_val = best.split('(')[1].rstrip(')')
                self.type_yolo.configure(text=f"vehicleType: {vehicle_type} [{conf_val}]")

                self.vehicleType = vehicle_type
            else:
                self.type_yolo.configure(text="vehicleType: -")

                self.vehicleType = ""
        self.get_class_vehicle()

    def get_class_vehicle(self):
        if self.vehicleType.lower() in ["bus", "car", "truck"] and self.maxHeight > 0 and self.totalAxles > 0:
            if self.maxHeight < 2.2:
                self.class_result.configure(text="Class 1")
            elif self.vehicleType.lower() == "bus":
                self.class_result.configure(text="Class 1")
            elif self.totalAxles == 2:
                self.class_result.configure(text="Class 2")
            elif self.totalAxles == 3:
                self.class_result.configure(text="Class 3")
            elif self.totalAxles == 4:
                self.class_result.configure(text="Class 4")
            elif self.totalAxles >= 5:
                self.class_result.configure(text="Class 5")

if __name__ == "__main__":
    app = App()
    app.mainloop()
