//
//  TransactionDetailView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 17/07/25.
//

import SwiftUI

struct VehicleDetailView: View {
    let carImage: String
    let carLidarImage: String
    let carName: String

    var body: some View {

        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Text(carName)
                    .font(.title3)
                    .fontWeight(.semibold)

                Spacer()

                Button(action: {}) {
                    Image(systemName: "trash")
                        .padding(8)
                        .font(.title3)
                        .background(Color.gray.opacity(0.2))
                        .clipShape(RoundedRectangle(cornerRadius: 5))

                }
                .buttonStyle(PlainButtonStyle())

            }

            HStack (spacing: 16){
                Image(carImage)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(height: 150)
                    .cornerRadius(8)
                    .clipped()

                Image(carLidarImage)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(height: 150)
                    .cornerRadius(8)
                    .clipped()
            }

            HStack(spacing: 16) {
                GolonganButtonGroup()

                GOLCard()
            }
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(12)
        .shadow(radius: 1)
    }
}

#Preview {
    VehicleDetailView(
        carImage: "Car_type",
        carLidarImage: "Lidar_result",
        carName: "Kendaraan 1"
    )
}
