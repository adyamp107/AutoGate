//
//  ContentView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 16/07/25.
//

import SwiftUI

enum Menu: String, CaseIterable, Identifiable {
    case allGate = "All Gate"
    case monitor = "Monitor"
    case dataHistory = "Data History"

    var id: String { self.rawValue }

    var title: String {
        switch self {
        case .allGate: return "All Gate"
        case .monitor: return "Monitor"
        case .dataHistory: return "Data History"
        }
    }

    var icon: String {
        switch self {
        case .allGate: return "video.bubble.fill"
        case .monitor: return "display"
        case .dataHistory: return "chart.bar.fill"
        }
    }
}

struct ContentView: View {
    @State private var selectedMenu: Menu = .allGate

    var body: some View {
        NavigationSplitView {
            SidebarView(selectedMenu: $selectedMenu)
                .navigationSplitViewColumnWidth(100)
        } detail: {
            switch selectedMenu {
            case .allGate:
                Text("All Gate View")
            case .monitor:
                MonitorGateView()
            case .dataHistory:
                Text("Data History View")
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
