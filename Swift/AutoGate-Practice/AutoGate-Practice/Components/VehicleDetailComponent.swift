//
//  VehicleDetailComponentView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 18/07/25.
//

import SwiftUI

struct VehicleAnalysisComponent: View {
    let carImage: String
    let carLidarImage: String
    let carName: String

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text(carName)
                .font(.title3)

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

            HStack(spacing: 4) {
                ManualButton()

                GOLCard()
            }
        }
    }
}

struct ManualButton: View {

    var body: some View {
        Button(action: {

        }) {
            VStack {
                Spacer()
                Text("Tentukan\nManual")
                    .font(.title2)
                    .fontWeight(.semibold)
                    .foregroundColor(.white)
                    .multilineTextAlignment(.center)
                    .lineSpacing(2)
                Spacer()
            }
            .frame(minWidth: 120, maxHeight: .infinity)
            .background(Color("Primer"))
            .cornerRadius(16)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct GolonganButtonGroup: View {
    var body: some View {
        VStack(spacing: 8) {
            // Baris pertama: 1 dan 2
            HStack(spacing: 8) {
                GolonganButton(label: "1")
                    .frame(maxWidth: .infinity)
                GolonganButton(label: "2")
                    .frame(maxWidth: .infinity)
            }

            // Baris kedua: 3, 4, dan 5
            HStack(spacing: 8) {
                GolonganButton(label: "3")
                GolonganButton(label: "4")
                GolonganButton(label: "5")
            }
        }
        .padding(0)
        .frame(maxWidth: .infinity)
    }
}

struct GolonganButton: View {
    let label: String

    var body: some View {
        Button(action: {}) {
            Text(label)
                .font(.title3)
                .fontWeight(.semibold)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(Color.primer)
                .cornerRadius(8)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct GOLCard: View {
    var body: some View {
        HStack(spacing: 12) {
            Spacer()

            Image("Gol1")
                .resizable()
                .scaledToFill()
                .frame(width: 40, height: 40)
                .clipped()
                .cornerRadius(12)

            Text("GOL I")
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(.primary)
            Spacer()
        }
        .frame(minWidth: 100, maxHeight: .infinity)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.secondary.opacity(0.3), lineWidth: 1)
        )

    }
}

//struct BottomLayoutView: View {
//    var body: some View {
//        HStack(spacing: 8) {
//            // Card 1: Tentukan Manual
//            ManualButton()
//
//            // Card 2: GOL I
//            GOLCard()
//
//            // Card 3: Timer
//            TimerCard()
//        }
//    }
//}

//struct TimerCard: View {
//    var body: some View {
//        VStack {
//            Spacer()
//
//            Text("00:05:00")
//                .font(.title)
//                .fontWeight(.bold)
//                .foregroundColor(.primary)
//
//            Spacer()
//        }
//        .frame(minWidth: 150, maxHeight: .infinity)
//        .cornerRadius(16)
//        .overlay(
//            RoundedRectangle(cornerRadius: 16)
//                .stroke(Color.secondary.opacity(0.3), lineWidth: 1)
//        )
//    }
//}
//
//struct DataRowSimple: View {
//    let label: String
//    let value: String
//
//    var body: some View {
//        HStack(alignment: .top) {
//            Text(label)
//                .font(.subheadline)
//                .fontWeight(.medium)
//                .foregroundColor(.primary)
//                .frame(minWidth: 100, alignment: .leading)
//
//            Text(": ")
//                .font(.subheadline)
//                .foregroundColor(.primary)
//
//            Text(value)
//                .font(.subheadline)
//                .foregroundColor(.primary)
//                .frame(maxWidth: .infinity, alignment: .leading)
//        }
//    }
//}
//
//struct DataPembayaran: View {
//    var body: some View {
//        HStack(spacing: 12) {
//            VStack(alignment: .leading, spacing: 16) {
//                Text("Data Kendaraan")
//                    .font(.headline)
//                    .frame(maxWidth: .infinity, alignment: .center)
//
//                VStack(alignment: .leading, spacing: 8) {
//                    DataRowSimple(
//                        label: "Waktu Masuk",
//                        value: "18/01/2025 18:03:24"
//                    )
//                    DataRowSimple(
//                        label: "Waktu Keluar",
//                        value: "18/01/2025 18:03:24"
//                    )
//                    DataRowSimple(label: "Shift", value: "1")
//                    DataRowSimple(
//                        label: "Nomor Kendaraan",
//                        value: "B 1234 WPF"
//                    )
//                }
//            }
//            .padding()
//            .frame(maxWidth: .infinity)
//            .background(Color(NSColor.controlBackgroundColor))
//            .cornerRadius(8)
//            .overlay(
//                RoundedRectangle(cornerRadius: 8)
//                    .stroke(Color.secondary.opacity(0.3), lineWidth: 1)
//            )
//
//            VStack(alignment: .leading, spacing: 16) {
//                Text("Data Pembayaran")
//                    .font(.headline)
//                    .frame(maxWidth: .infinity, alignment: .center)
//
//                VStack(alignment: .leading, spacing: 8) {
//                    DataRowSimple(
//                        label: "Nomor Kartu",
//                        value: "923213121231"
//                    )
//                    DataRowSimple(
//                        label: "Bank",
//                        value: "Mandiri"
//                    )
//                    DataRowSimple(label: "Tarif Gerbang", value: "Rp. 5000")
//                    DataRowSimple(
//                        label: "Sisa Saldo",
//                        value: "Rp. 87000"
//                    )
//                }
//            }
//            .padding()
//            .frame(maxWidth: .infinity)
//            .background(Color(NSColor.controlBackgroundColor))
//            .cornerRadius(8)
//            .overlay(
//                RoundedRectangle(cornerRadius: 8)
//                    .stroke(Color.secondary.opacity(0.3), lineWidth: 1)
//            )
//        }
//    }
//}
