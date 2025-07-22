//
//  MonitorGateView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 17/07/25.
//

import SwiftUI

struct MonitorGateView: View {
    @State private var showPopup = false
    @State private var selectedGolongan: String? = nil

    var body: some View {
        VStack(spacing: 12) {
            CameraGateView(gateName: "Gate 1")
            
            HStack {
                VehicleDetailView(carImage: "Car_type", carLidarImage: "Lidar_result", carName: "Kendaraan 1")
                
                VehicleDetailView(carImage: "Car_type2", carLidarImage: "Lidar_result2", carName: "Kendaraan 2")
            }
        }
        .padding(10)
        .background(Color(NSColor.windowBackgroundColor))
    }
}

#Preview {
    MonitorGateView()
}
