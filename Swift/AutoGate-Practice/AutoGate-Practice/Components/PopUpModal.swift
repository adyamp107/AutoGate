//
//  PopUpModal.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 21/07/25.
//

import SwiftUI

struct ManualPopupView: View {
    var onSelect: (String) -> Void

    var body: some View {
        VStack(spacing: 12) {
            Text("Tentukan manual")
                .font(.headline)

            VStack(spacing: 12) {
                HStack(spacing: 12) {
                    ForEach(["I", "II"], id: \.self) { title in
                        popupButton(title)
                    }
                }

                HStack(spacing: 12) {
                    ForEach(["III", "IV"], id: \.self) { title in
                        popupButton(title)
                    }
                }

                popupButton("V")
                    .frame(width: 100)
            }
            .padding(.bottom)
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 16).fill(.background))
        .shadow(radius: 8)
    }

    private func popupButton(_ title: String) -> some View {
        Button(action: {
            onSelect(title)
        }) {
            Text(title)
                .font(.title3)
                .fontWeight(.medium)
                .foregroundColor(.white)
                .frame(width: 80, height: 50)
                .background(Color("Primer"))
                .cornerRadius(10)
        }
        .buttonStyle(.plain)
    }
}

