//
//  CameraGateView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 17/07/25.
//

import AVKit
import SwiftUI

struct CameraGateView: View {
    let gateName: String
    let step: Int
    var body: some View {
        VStack(alignment: .center, spacing: 12) {
            Text(gateName)
                .font(.title2)
                .fontWeight(.semibold)

            HStack {
                CameraPartView(
                    step: step,
                    index: 1,
                    videoName: "Mazda3",
                    camTitle: "Cam 1"
                )
                CameraPartView(
                    step: step,
                    index: 1,
                    videoName: "GarbageTruck",
                    camTitle: "Cam 2"
                )
            }
        }
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(12)
        .shadow(radius: 1)
    }
}

struct CameraPartView: View {
    let step: Int
    let index: Int
    let videoName: String
    let camTitle: String
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Group {
                if step >= index {
                    LoopingVideoPlayer(videoName: videoName)
                } else {
                    Rectangle()
                        .fill(Color.black)
                }
            }
            .frame(minHeight: 100)
            .cornerRadius(8)

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
    CameraGateView(gateName: "Gate 1", step: 1)
}
