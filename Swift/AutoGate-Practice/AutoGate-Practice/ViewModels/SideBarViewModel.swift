//
//  SideBarViewModel.swift
//  AutoGate-Practice
//
//  Created by Miftah Fauzy on 22/07/25.
//

import SwiftUI

enum Menu: String, CaseIterable, Identifiable {
    case monitor = "Monitor"
    case allGate = "All Gate"
    case dataHistory = "Data History"

    var id: String { self.rawValue }

    var title: String {
        switch self {
        case .monitor: return "Monitor"
        case .allGate: return "All Gate"
        case .dataHistory: return "Data History"
        }
    }

    var icon: String {
        switch self {
        case .monitor: return "display"
        case .allGate: return "video.bubble.fill"
        case .dataHistory: return "chart.bar.fill"
        }
    }
}
