//
//  ContentView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 16/07/25.
//

import SwiftUI

struct ContentView: View {
    @State private var selectedMenu: Menu = .monitor

    var body: some View {
        NavigationSplitView {
            SidebarView(selectedMenu: $selectedMenu)
                .navigationSplitViewColumnWidth(100)
        } detail: {
            switch selectedMenu {
            case .monitor:
                MonitorGateView()
            case .allGate:
                AllGateView()
            case .dataHistory:
                DataHistoryView()
            }
        }
        .toolbar {
            ToolbarItem(placement: .navigation) {
                Text("All Gate")
                    .font(.headline)
            }
            ToolbarItem(placement: .principal) {
                HStack(spacing: 20) {
                    Text("18:03")
                    Text("•")
                    Text("Shift 1")
                }
                .font(.subheadline)
            }
            ToolbarItem(placement: .automatic) {
                Text("Fathur")
                    .font(.subheadline)
            }
        }
    }
}

#Preview {
    ContentView()
}
