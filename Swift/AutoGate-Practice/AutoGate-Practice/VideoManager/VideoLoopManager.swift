//
//  VideoPlayer.swift
//  AutoGate-Practice
//
//  Created by Ali Jazzy Rasyid on 21/07/25.
//

import SwiftUI
import AVKit

class AVPlayerLooperManager {
    static let shared = AVPlayerLooperManager()
    
    private var loopers: [String: AVPlayerLooper] = [:]
    private var players: [String: AVQueuePlayer] = [:]

    private let supportedExtensions = ["mp4", "mov", "m4v"] // bisa ditambah

    func player(for resource: String) -> AVQueuePlayer? {
        if let player = players[resource] {
            return player
        }

        // Cari URL dengan ekstensi apa pun yang didukung
        guard let url = findVideoURL(resource: resource) else {
            print("❌ Video not found: \(resource)")
            return nil
        }

        let item = AVPlayerItem(url: url)
        let queue = AVQueuePlayer()
        let looper = AVPlayerLooper(player: queue, templateItem: item)

        loopers[resource] = looper
        players[resource] = queue

        return queue
    }

    func play(_ resource: String) {
        players[resource]?.play()
    }

    private func findVideoURL(resource: String) -> URL? {
        for ext in supportedExtensions {
            if let url = Bundle.main.url(forResource: resource, withExtension: ext) {
                return url
            }
        }
        return nil
    }
}

