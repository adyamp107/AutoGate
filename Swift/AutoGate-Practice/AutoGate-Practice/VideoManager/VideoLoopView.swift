//
//  VideoLoopView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 21/07/25.
//

import AVKit
import SwiftUI

struct LoopingVideoPlayer: View {
    let videoName: String

    var body: some View {
        if let player = AVPlayerLooperManager.shared.player(for: videoName) {
            VideoPlayer(player: player)
                .onAppear {
                    AVPlayerLooperManager.shared.play(videoName)
                }
        } else {
            Color.black
        }
    }
}
#Preview {
    LoopingVideoPlayer(videoName: "Mazda 3 Clip")
}
