//
//  VideoLoopView.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 21/07/25.
//

import SwiftUI
import AVKit

struct LoopingVideoPlayer: View {
    let videoName: String

    var body: some View {
        VideoPlayer(player: AVPlayerLooperManager.shared.player(for: videoName))
            .onAppear {
                AVPlayerLooperManager.shared.play(videoName)
            }
    }
}
#Preview {
    LoopingVideoPlayer(videoName: "Mazda 3 Clip")
}
