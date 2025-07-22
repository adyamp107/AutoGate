//
//  MonitorGateView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 17/07/25.
//

import AVKit
import Combine
import SwiftUI

struct MonitorGateView: View {
    @State private var currentStep = 0
    let timer = Timer.publish(every: 5, on: .main, in: .common).autoconnect()

    var body: some View {
        VStack(spacing: 12) {
            CameraGateView(gateName: "Gate 1", step: currentStep)

            HStack {
                VehicleDetailView(
                    carImage: currentStep >= 1 ? "Car_type" : nil,
                    carLidarImage: currentStep >= 1 ? "Lidar_result" : nil,
                    carName: "Kendaraan 1",
                    jenisGolongan: currentStep >= 1 ? 1 : nil
                )
                VehicleDetailView(
                    carImage: currentStep >= 2 ? "Car_type2" : nil,
                    carLidarImage: currentStep >= 2 ? "Lidar_result2" : nil,
                    carName: "Kendaraan 2",
                    jenisGolongan: currentStep >= 2 ? 2 : nil
                )
            }
        }
        .padding(10)
        .background(Color(NSColor.windowBackgroundColor))
        .onReceive(timer) { _ in
            withAnimation(.easeInOut) {
                if currentStep < 2 {
                    currentStep += 1
                }
            }
        }
    }
}

#Preview {
    MonitorGateView()
}
