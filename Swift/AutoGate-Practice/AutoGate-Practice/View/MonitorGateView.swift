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
        ZStack {
            HStack {
                VStack(spacing: 12) {
                    CameraGateView(gateName: "Gate 1")
                    VehicleDetailView(showPopup: $showPopup)
                }
                .padding(10)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(Color(NSColor.windowBackgroundColor))

                Divider()

                VStack(spacing: 12) {
                    CameraGateView(gateName: "Gate 2")
                    VehicleDetailView(showPopup: $showPopup)
                }
                .padding(10)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(Color(NSColor.windowBackgroundColor))
            }

            if showPopup {
                Color.black.opacity(0.4)
                    .ignoresSafeArea()

                ManualPopupView { selected in
                    selectedGolongan = selected
                    showPopup = false
                    print("Golongan dipilih: \(selected)")
                }
                .frame(width: 300)
                .transition(.scale)
            }
        }
        .animation(.easeInOut, value: showPopup)
    }
}

#Preview {
    MonitorGateView()
}
