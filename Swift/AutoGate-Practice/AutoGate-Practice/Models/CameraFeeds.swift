//
//  Untitled.swift
//  AutoGate-Practice
//
//  Created by Miftah Fauzy on 22/07/25.
//

import Foundation

struct CameraFeed: Identifiable {
    let id = UUID()
    let cameraName: String
    let gateName: String
    let imageName: String // Assume you have asset images
}
