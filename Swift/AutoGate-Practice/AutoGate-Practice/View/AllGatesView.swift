//
//  AllGatesView.swift
//  AutoGate-Practice
//
//  Created by Miftah Fauzy on 22/07/25.
//

import SwiftUI

struct AllGateView: View {
    @StateObject private var viewModel = AllGateViewModel()
    @State private var currentTime = getCurrentTime()

    let columns = [
        GridItem(.flexible()),
        GridItem(.flexible()),
        GridItem(.flexible())
    ]

    var body: some View {
        VStack(spacing: 0) {
            // Custom macOS Header
            HStack {
                // Left: All Gate with icon
                HStack(spacing: 8) {
                    Text("All Gate")
                        .font(.system(size: 16, weight: .semibold))
                }

                Spacer()

                // Center: Time and Shift
                HStack(spacing: 6) {
                    Text(currentTime)
                        .font(.system(size: 14, weight: .regular))
                    Circle()
                        .frame(width: 4, height: 4)
                    Text("Shift 1")
                        .font(.system(size: 14, weight: .regular))
                }
                .foregroundColor(.secondary)

                Spacer()

                // Right: User
                HStack(spacing: 6) {
                    Text("Fathur")
                        .font(.system(size: 14, weight: .regular))
                    Circle()
                        .frame(width: 10, height: 10)
                        .foregroundColor(.gray) // status indicator
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
            .background(Color(NSColor.windowBackgroundColor))
            .overlay(
                Divider(), alignment: .bottom
            )
            .onAppear {
                // Start timer for clock updates
                Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
                    currentTime = getCurrentTime()
                }
            }

            // Grid of camera feeds
            ScrollView {
                LazyVGrid(columns: columns, spacing: 16) {
                    ForEach(viewModel.cameraFeeds) { feed in
                        VStack {
                            LoopingVideoPlayer(videoName: feed.imageName)
                            Text("\(feed.cameraName) • \(feed.gateName)")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        .background(Color(NSColor.controlBackgroundColor))
                        .cornerRadius(8)
                        .shadow(radius: 1)
                        .frame(height: 250)
                    }
                }
                .padding()
            }
        }
        .frame(minWidth: 800, minHeight: 600)
    }
}

// Helper to get current time in HH:mm format
func getCurrentTime() -> String {
    let formatter = DateFormatter()
    formatter.dateFormat = "HH:mm"
    return formatter.string(from: Date())
}
