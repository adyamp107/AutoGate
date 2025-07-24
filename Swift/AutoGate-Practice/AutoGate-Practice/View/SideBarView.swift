//
//  SideBarView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 16/07/25.
//

import SwiftUI

struct SidebarView: View {
    @Binding var selectedMenu: Menu

    var body: some View {
        VStack(spacing: 20) {
            ForEach(Menu.allCases) { item in
                Button(action: {
                    selectedMenu = item
                }) {
                    VStack(spacing: 6) {
                        Image(systemName: item.icon)
                            .font(.largeTitle)
                        Text(item.title)
                            .font(.caption)
                            .multilineTextAlignment(.center)
                    }
                    .foregroundColor(.white)
                    .padding()
                    .background(selectedMenu == item ? Color.sekunder : Color.clear)
                    .cornerRadius(16)
                }
                .buttonStyle(.plain)
            }

            Spacer()
        }
        .padding(.top, 24)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color.primer)
    }
}

