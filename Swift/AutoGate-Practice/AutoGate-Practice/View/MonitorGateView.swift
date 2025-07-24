////
////  MonitorGateView.swift
////  AutoGate-Practice
////
////  Created by Ali Jazzy Rasyid on 17/07/25.
////
//
//import SwiftUI
//
//struct MonitorGateView: View {
//    @State private var showPopup = false
//    @State private var selectedGolongan: String? = nil
//
//    var body: some View {
//        VStack(spacing: 12) {
//            CameraGateView(gateName: "Gate 1")
//            
//            HStack {
//                VehicleDetailView(carImage: "Car_type", carLidarImage: "Lidar_result", carName: "Kendaraan 1")
//                
//                VehicleDetailView(carImage: "Car_type2", carLidarImage: "Lidar_result2", carName: "Kendaraan 2")
//            }
//        }
//        .padding(10)
//        .background(Color(NSColor.windowBackgroundColor))
//    }
//}
//
//#Preview {
//    MonitorGateView()
//}


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
    
    @State private var currentStep1: Int = 0
    @State private var currentStep2: Int = 0
    
    let timer = Timer.publish(every: 5, on: .main, in: .common).autoconnect()
    
    @State private var jenis1: Int? = nil
    @State private var jenis2: Int? = nil

    var body: some View {
        VStack(spacing: 12) {
            CameraGateView(firstVideoName: "Cam1", secondVideoName: "Cam2")

            HStack {
                VehicleDetailView(
                    carImage: currentStep1 == 0 ? nil : "Car_type",
                    carLidarImage: currentStep1 == 0 ? nil : "Lidar_result",
                    carName: "Kendaraan 1",
                    jenisGolongan: currentStep1 == 0 ? nil : currentStep1,
                    bruh1: { gol in
                        currentStep1 = gol
                    },
                    bruh2: {
                        currentStep1 = 0
                    }
                )
                VehicleDetailView(
                    carImage: currentStep2 == 0 ? nil : "Car_type2",
                    carLidarImage: currentStep2 == 0 ? nil : "Lidar_result2",
                    carName: "Kendaraan 2",
                    jenisGolongan: currentStep2 == 0 ? nil : currentStep2,
                    bruh1: { gol in
                        currentStep2 = gol
                    },
                    bruh2: {
                        currentStep2 = 0
                    }
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
                if currentStep == 1 {
                    currentStep1 = 1
                } else if currentStep == 2 {
                    currentStep2 = 2
                }
            }
        }
    }
}

#Preview {
    MonitorGateView()
}
