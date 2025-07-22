//
//  CameraGateView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 17/07/25.
//

import SwiftUI
import AVKit

struct CameraGateView: View {
    let gateName: String
    var body: some View {
        VStack(alignment: .center, spacing: 12) {
            Text(gateName)
                .font(.title2)
                .fontWeight(.semibold)

            HStack {
                CameraPartView(videoName: "Mazda3", camTitle: "Cam 1")
                CameraPartView(videoName: "GarbageTruck", camTitle: "Cam 2")
            }
        }
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(12)
        .shadow(radius: 1)
    }
}

struct CameraPartView: View {
    let videoName: String
    let camTitle: String
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            LoopingVideoPlayer(videoName: videoName)
                .frame(minHeight: 100)
                .cornerRadius(8)
                .clipped()

            HStack(spacing: 6) {
                HStack(spacing: 4) {
                    Text("•")
                        .foregroundStyle(Color.red)
                        .font(.title3)
                    Text("Live")
                }
                Text("•")
                Text(camTitle)
            }
            .font(.callout)
            .fontWeight(.semibold)
        }
    }
}

#Preview {
    CameraGateView(gateName: "Gate 1")
}
