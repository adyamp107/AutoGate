//
//  VehicleDetailComponentView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 18/07/25.
//

import SwiftUI

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
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(Color.primer)
                .cornerRadius(8)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct GOLCard: View {
    let golonganNumber: Int?
    var body: some View {
        HStack(spacing: 12) {
            Spacer()

            if let number = golonganNumber {
                Image("Gol\(number)")
                    .resizable()
                    .scaledToFill()
                    .frame(width: 56, height: 56)
                    .clipped()
                    .cornerRadius(12)

                Text("GOL \(number)")
                    .font(.system(size: 48))
                    .fontWeight(.black)
                    .foregroundColor(.primary)
            } else {
                Text("-")
                    .font(.system(size: 48))
                    .fontWeight(.bold)
            }
            Spacer()
        }
        .frame(minWidth: 100, maxHeight: .infinity)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.primer, lineWidth: 1.5)
        )

    }
}
