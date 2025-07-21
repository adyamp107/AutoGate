//
//  TransactionDetailView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 17/07/25.
//

import SwiftUI

struct VehicleDetailView: View {
    @Binding var showPopup: Bool
    
    var body: some View {

        HStack(spacing: 16) {
            VehicleAnalysisComponent(carImage: "Car_type", carLidarImage: "Lidar_result", carName: "Kendaraan 1", showPopup: $showPopup)

            VehicleAnalysisComponent(carImage: "Car_type2", carLidarImage: "Lidar_result2", carName: "Kendaraan 2", showPopup: $showPopup)
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(12)
        .shadow(radius: 1)
    }
}

#Preview {
    VehicleDetailView(showPopup: .constant(false))
}
