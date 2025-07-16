import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

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
        self.geometry("1450x800")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=500)
        self.grid_rowconfigure(0, weight=0, minsize=40)
        self.grid_rowconfigure(1, weight=1, uniform="self")
        self.grid_rowconfigure(2, weight=10)
        self.grid_rowconfigure(3, weight=1, uniform="self")
        self.grid_rowconfigure(4, weight=1, uniform="self")

        self.video_cap = None
        self.video_running = False

        # ============================================================================================================

        self.label = ctk.CTkLabel(self, text="Welcome to AutoGate", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # ============================================================================================================

        self.flow_1 = ctk.CTkFrame(self, corner_radius=10)
        self.flow_1.grid(row=1, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew")

        self.title_flow_1 = ctk.CTkLabel(self.flow_1, text="Flow 1: Vehicle In", font=("Arial", 16))
        self.title_flow_1.pack(padx=10, side="left", anchor="center")

        # ============================================================================================================

        self.flow_2 = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.flow_2.grid(row=2, column=0, rowspan=3, padx=(10, 5), pady=(5, 10), sticky="nsew")
        self.flow_2.grid_columnconfigure(0, weight=1, uniform="flow_2")
        self.flow_2.grid_columnconfigure(1, weight=1, uniform="flow_2")
        self.flow_2.grid_rowconfigure(0, weight=1)
        self.flow_2.grid_rowconfigure(1, weight=1)
        self.flow_2.grid_rowconfigure(2, weight=1)
        self.flow_2.grid_rowconfigure(3, weight=1)
        self.flow_2.grid_rowconfigure(4, weight=1)
        self.flow_2.grid_rowconfigure(5, weight=1)
        self.flow_2.grid_rowconfigure(6, weight=1)
        self.flow_2.grid_rowconfigure(7, weight=1)
        self.flow_2.grid_rowconfigure(8, weight=1)
        self.flow_2.grid_rowconfigure(9, weight=1)

        self.title_flow_2 = ctk.CTkLabel(self.flow_2, text="Flow 2: LiDAR Scan", font=("Arial", 16))
        self.title_flow_2.grid(padx=10, pady=(10, 5), row=0, column=0, columnspan=2, sticky="nsw")

        self.browse_button_flow_2 = ctk.CTkButton(self.flow_2, text="Input Dokumen (.pcd)", command=self.browse_file_pcd)
        self.browse_button_flow_2.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.selected_path_flow_2 = ctk.CTkLabel(self.flow_2, text="Belum ada file dipilih", anchor="w")
        self.selected_path_flow_2.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # ============================================================================================================

        self.loaded_points = []
        self.loaded_pcd = None
        self.slider_value_flow_2 = 0
        self.right_side_points = []
        self.left_side_points = []

        # ============================================================================================================

        self.slider_flow_2 = ctk.CTkSlider(self.flow_2, from_=0, to=100, number_of_steps=100, command=self.on_slider_change)
        self.slider_flow_2.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.fig_vehicle_left_flow_2 = plt.Figure(figsize=(5, 3), dpi=100)
        self.ax_vehicle_left_flow_2 = self.fig_vehicle_left_flow_2.add_subplot(111)
        self.ax_vehicle_left_flow_2.set_title("\n2D Left Side View (X-Z)")
        self.ax_vehicle_left_flow_2.scatter([], [])
        self.line_vehicle_left_flow_2 = self.ax_vehicle_left_flow_2.axhline(y=self.slider_value_flow_2, color='red', linestyle='--', linewidth=1)
        self.ax_vehicle_left_flow_2.axis("off")
        self.fig_vehicle_left_flow_2.tight_layout(pad=0)
        self.canvas_vehicle_left_flow_2 = FigureCanvasTkAgg(self.fig_vehicle_left_flow_2, master=self.flow_2)
        self.canvas_vehicle_left_flow_2.draw()
        self.canvas_vehicle_left_flow_2.get_tk_widget().grid(row=4, column=0, padx=(10, 5), pady=(5, 1), sticky="nsew")

        self.fig_vehicle_right_flow_2 = plt.Figure(figsize=(5, 3), dpi=100)
        self.ax_vehicle_right_flow_2 = self.fig_vehicle_right_flow_2.add_subplot(111)
        self.ax_vehicle_right_flow_2.set_title("\n2D Right Side View (Y-Z)")
        self.ax_vehicle_right_flow_2.scatter([], [])
        self.line_vehicle_right_flow_2 = self.ax_vehicle_right_flow_2.axhline(y=self.slider_value_flow_2, color='red', linestyle='--', linewidth=1)
        self.ax_vehicle_right_flow_2.axis("off")
        self.fig_vehicle_right_flow_2.tight_layout(pad=0)
        self.canvas_vehicle_right_flow_2 = FigureCanvasTkAgg(self.fig_vehicle_right_flow_2, master=self.flow_2)
        self.canvas_vehicle_right_flow_2.draw()
        self.canvas_vehicle_right_flow_2.get_tk_widget().grid(row=4, column=1, padx=(5, 10), pady=(5, 1), sticky="nsew")

        self.fig_histogram_left_flow_2 = plt.Figure(figsize=(5, 0.5), dpi=100)
        self.ax_histogram_left_flow_2 = self.fig_histogram_left_flow_2.add_subplot(111)
        self.ax_histogram_left_flow_2.bar(range(0), [], color='red')
        self.ax_histogram_left_flow_2.axis("off")
        self.fig_histogram_left_flow_2.tight_layout(pad=0)
        self.canvas_histogram_left_flow_2 = FigureCanvasTkAgg(self.fig_histogram_left_flow_2, master=self.flow_2)
        self.canvas_histogram_left_flow_2.draw()
        self.canvas_histogram_left_flow_2.get_tk_widget().grid(row=5, column=0, padx=(10, 5), pady=(1, 5), sticky="nsew")

        self.fig_histogram_right_flow_2 = plt.Figure(figsize=(5, 0.5), dpi=100)
        self.ax_histogram_right_flow_2 = self.fig_histogram_right_flow_2.add_subplot(111)
        self.ax_histogram_right_flow_2.bar(range(0), [], color='red')
        self.ax_histogram_right_flow_2.axis("off")
        self.fig_histogram_right_flow_2.tight_layout(pad=0)
        self.canvas_histogram_right_flow_2 = FigureCanvasTkAgg(self.fig_histogram_right_flow_2, master=self.flow_2)
        self.canvas_histogram_right_flow_2.draw()
        self.canvas_histogram_right_flow_2.get_tk_widget().grid(row=5, column=1, padx=(5, 10), pady=(1, 5), sticky="nsew")

        self.axle_count_left_flow_2 = ctk.CTkLabel(self.flow_2, text="Left axle(s): -", font=("Arial", 14, "bold"))
        self.axle_count_left_flow_2.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.axle_count_right_flow_2 = ctk.CTkLabel(self.flow_2, text="Right axle(s): -", font=("Arial", 14, "bold"))
        self.axle_count_right_flow_2.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.axle_count_flow_2 = ctk.CTkLabel(self.flow_2, text="No data!", font=("Arial", 14, "bold"))
        self.axle_count_flow_2.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.show_3d_button_flow_2 = ctk.CTkButton(self.flow_2, text="Show 3D Point Cloud", command=self.show_3d_popup)
        self.show_3d_button_flow_2.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        # ============================================================================================================

        self.flow_3 = ctk.CTkFrame(self, corner_radius=10)
        self.flow_3.grid(row=1, column=1, rowspan=2, padx=(5, 10), pady=(10, 5), sticky="nsew")

        self.title_flow_3 = ctk.CTkLabel(self.flow_3, text="Flow 3: Operator Check", font=("Arial", 16))
        self.title_flow_3.pack(padx=10, pady=(10, 5), anchor="w")

        self.browse_button_flow_3 = ctk.CTkButton(self.flow_3, text="Input Video", command=self.browse_file_video)
        self.browse_button_flow_3.pack(padx=10, pady=5, anchor="w")

        self.selected_path_flow_3 = ctk.CTkLabel(self.flow_3, text="Belum ada video dipilih", anchor="w")
        self.selected_path_flow_3.pack(padx=10, pady=5, fill="x")

        self.video_frame_placeholder = ctk.CTkLabel(self.flow_3, text="Frame video akan tampil di sini", height=200, anchor="center")
        self.video_frame_placeholder.pack(padx=10, pady=5, fill="x")

        self.button1 = ctk.CTkButton(self.flow_3, text="1")
        self.button1.pack(padx=10, pady=5, anchor="w")

        self.button2 = ctk.CTkButton(self.flow_3, text="2")
        self.button2.pack(padx=10, pady=5, anchor="w")

        self.button3 = ctk.CTkButton(self.flow_3, text="3")
        self.button3.pack(padx=10, pady=5, anchor="w")

        self.button4 = ctk.CTkButton(self.flow_3, text="4")
        self.button4.pack(padx=10, pady=5, anchor="w")

        self.button5 = ctk.CTkButton(self.flow_3, text="5")
        self.button5.pack(padx=10, pady=5, anchor="w")

        # ============================================================================================================

        self.flow_4 = ctk.CTkFrame(self, corner_radius=10)
        self.flow_4.grid(row=3, column=1, padx=(5, 10), pady=(5, 5), sticky="nsew")

        self.title_flow_4 = ctk.CTkLabel(self.flow_4, text="Flow 4: E-Toll Payments", font=("Arial", 16))
        self.title_flow_4.pack(padx=10, side="left", anchor="center")

        # ============================================================================================================

        self.flow_5 = ctk.CTkFrame(self, corner_radius=10)
        self.flow_5.grid(row=4, column=1, padx=(5, 10), pady=(5, 10), sticky="nsew")

        self.title_flow_5 = ctk.CTkLabel(self.flow_5, text="Flow 5: Vehicle Out", font=("Arial", 16))
        self.title_flow_5.pack(padx=10, side="left", anchor="center")

    def browse_file_pcd(self):
        file_path = filedialog.askopenfilename(filetypes=[("PCD Files", "*.pcd"), ("All files", "*.*")])
        if file_path:
            self.selected_path_flow_2.configure(text=file_path)
            self.load_pointcloud(file_path)

    def browse_file_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")])
        if file_path:
            self.selected_path_flow_3.configure(text=file_path)
            self.video_cap = cv2.VideoCapture(file_path)
            self.video_running = True
            self.update_video_frame()

    def load_pointcloud(self, file_path):
        try:
            pcd = o3d.io.read_point_cloud(file_path)
            points = np.asarray(pcd.points)
            
            points[:, 0] -= np.min(points[:, 0])
            points[:, 1] -= np.min(points[:, 1])
            points[:, 2] -= np.min(points[:, 2])

            if points.shape[0] == 0:
                self.selected_path_flow_2.configure(text="File kosong")
                return

            self.loaded_points = points
            self.loaded_pcd = pcd
            self.slider_value_flow_2 = 0.1

            x_min, x_max = points[:, 0].min(), points[:, 0].max()
            x_range = x_max - x_min
            threshold = 0.1 * x_range

            self.right_side_points = points[points[:, 0] <= x_min + threshold]
            self.left_side_points = points[points[:, 0] >= x_max - threshold]

            self.ax_vehicle_left_flow_2.clear()
            self.ax_vehicle_left_flow_2.scatter(self.left_side_points[:, 1], self.left_side_points[:, 2], s=1, c='blue')
            self.ax_vehicle_left_flow_2.set_title("\n2D Left Side View (Y-Z, X max slice)")
            self.line_vehicle_left_flow_2 = self.ax_vehicle_left_flow_2.axhline(y=self.slider_value_flow_2, color='red', linestyle='--', linewidth=1)
            self.ax_vehicle_left_flow_2.axis("off")
            self.fig_vehicle_left_flow_2.tight_layout(pad=0)
            self.canvas_vehicle_left_flow_2.draw()

            self.ax_vehicle_right_flow_2.clear()
            self.ax_vehicle_right_flow_2.scatter(self.right_side_points[:, 1], self.right_side_points[:, 2], s=1, c='green')
            self.ax_vehicle_right_flow_2.set_title("\n2D Right Side View (Y-Z, X min slice)")
            self.line_vehicle_right_flow_2 = self.ax_vehicle_right_flow_2.axhline(y=self.slider_value_flow_2, color='red', linestyle='--', linewidth=1)
            self.ax_vehicle_right_flow_2.axis("off")
            self.fig_vehicle_right_flow_2.tight_layout(pad=0)
            self.canvas_vehicle_right_flow_2.draw()

            self.count_axles()

        except Exception as e:
            self.selected_path_flow_2.configure(text=f"Error: {str(e)}")

    def on_slider_change(self, value):
        min_z = np.min(self.loaded_points[:, 2])
        max_z = np.max(self.loaded_points[:, 2])
        z_mapped = min_z + (value / 100) * (max_z - min_z)
        self.slider_value_flow_2 = z_mapped
        self.line_vehicle_left_flow_2.set_ydata([z_mapped])
        self.canvas_vehicle_left_flow_2.draw()
        self.line_vehicle_right_flow_2.set_ydata([z_mapped])
        self.canvas_vehicle_right_flow_2.draw()
        self.count_axles()

    def show_3d_popup(self):
        if self.loaded_pcd is not None:
            o3d.visualization.draw_geometries([self.loaded_pcd])
        else:
            self.selected_path_flow_2.configure(text="Belum ada file pcd yang dimuat.")

    def count_axles(self):
        self.left_side_points
        self.right_side_points
        self.slider_value_flow_2

        threshold = 0.05
        z_value = self.slider_value_flow_2
        close_left_points = self.left_side_points[np.abs(self.left_side_points[:, 2] - z_value) < threshold]
        close_right_points = self.right_side_points[np.abs(self.right_side_points[:, 2] - z_value) < threshold]
        # print(f"Z value (slider): {z_value:.3f}")
        # print(f"Left side - total close points: {(close_left_points)}")
        # print(f"Right side - total close points: {(close_right_points)}")

        # y_min = np.min(self.left_side_points[:, 1])
        # y_max = np.max(self.left_side_points[:, 1])
        # bins = np.linspace(y_min, y_max, 101)

        # self.ax_histogram_left_flow_2.clear()
        # self.ax_histogram_left_flow_2.hist(close_left_points[:, 1], bins=bins, color='blue')
        # self.ax_histogram_left_flow_2.axis("off")
        # self.fig_histogram_left_flow_2.tight_layout(pad=0)
        # self.canvas_histogram_left_flow_2.draw()

        # self.ax_histogram_right_flow_2.clear()
        # self.ax_histogram_right_flow_2.hist(close_right_points[:, 1], bins=bins, color='green')
        # self.ax_histogram_right_flow_2.axis("off")
        # self.fig_histogram_right_flow_2.tight_layout(pad=0)
        # self.canvas_histogram_right_flow_2.draw()

        y_min = np.min(self.left_side_points[:, 1])
        y_max = np.max(self.left_side_points[:, 1])
        bins = np.linspace(y_min, y_max, 101)

        hist_left, bin_edges_left = np.histogram(close_left_points[:, 1], bins=bins)
        hist_right, bin_edges_right = np.histogram(close_right_points[:, 1], bins=bins)

        bin_centers_left = (bin_edges_left[:-1] + bin_edges_left[1:]) / 2
        bin_centers_right = (bin_edges_right[:-1] + bin_edges_right[1:]) / 2

        self.ax_histogram_left_flow_2.clear()
        bar_width_left = (bin_edges_left[1] - bin_edges_left[0]) * 1
        self.ax_histogram_left_flow_2.bar(bin_centers_left, hist_left, width=bar_width_left, color='blue')
        self.ax_histogram_left_flow_2.axis("off")
        self.fig_histogram_left_flow_2.tight_layout(pad=0)
        self.canvas_histogram_left_flow_2.draw()

        self.ax_histogram_right_flow_2.clear()
        bar_width_right = (bin_edges_right[1] - bin_edges_right[0]) * 1
        self.ax_histogram_right_flow_2.bar(bin_centers_right, hist_right, width=bar_width_right, color='green')
        self.ax_histogram_right_flow_2.axis("off")
        self.fig_histogram_right_flow_2.tight_layout(pad=0)
        self.canvas_histogram_right_flow_2.draw()

        left_clusters = self.cluster_by_distance(close_left_points[:, 1:3], side="Left")
        right_clusters = self.cluster_by_distance(close_right_points[:, 1:3], side="Right")
        # print(f"Left axle groups: {left_clusters}")
        # print(f"Right axle groups: {right_clusters}")

        self.axle_count_left_flow_2.configure(text=f"Left axle(s): {left_clusters}")
        self.axle_count_right_flow_2.configure(text=f"Right axle(s): {right_clusters}")
        if left_clusters == right_clusters:
            self.axle_count_flow_2.configure(text=f"Number of axle(s) is {left_clusters}")
        else:
            self.axle_count_flow_2.configure(text=f"Number of axle(s) is not valid")

    def cluster_by_distance(self, points_yz, side=""):
        if len(points_yz) == 0:
            return 0
        db = DBSCAN(eps=0.5, min_samples=5).fit(points_yz)
        labels = db.labels_
        num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        print(f"{side} - Cluster labels: {set(labels)}")
        return num_clusters

    def update_video_frame(self):
        if self.video_running and self.video_cap is not None:
            ret, frame = self.video_cap.read()
            if ret:
                frame = cv2.resize(frame, (400, 240))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_frame_placeholder.configure(image=imgtk, text="")
                self.video_frame_placeholder.image = imgtk
            else:
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.after(30, self.update_video_frame)

if __name__ == "__main__":
    app = App()
    app.mainloop()
