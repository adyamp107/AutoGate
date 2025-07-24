//
//  AllGatesViewModel.swift
//  AutoGate-Practice
//
//  Created by Miftah Fauzy on 22/07/25.
//


import SwiftUI

class AllGateViewModel: ObservableObject {
    @Published var cameraFeeds: [CameraFeed] = [
        CameraFeed(cameraName: "Cam 1", gateName: "Gate 1", imageName: "Cam1"),
        CameraFeed(cameraName: "Cam 2", gateName: "Gate 1", imageName: "Cam2"),
        CameraFeed(cameraName: "Cam 3", gateName: "Gate 1", imageName: "Cam1"),
        CameraFeed(cameraName: "Cam 4", gateName: "Gate 1", imageName: "Cam2"),
        CameraFeed(cameraName: "Cam 5", gateName: "Gate 1", imageName: "Cam1"),
        CameraFeed(cameraName: "Cam 6", gateName: "Gate 1", imageName: "Cam2"),
        CameraFeed(cameraName: "Cam 7", gateName: "Gate 1", imageName: "Cam1"),
        CameraFeed(cameraName: "Cam 8", gateName: "Gate 1", imageName: "Cam2"),
        CameraFeed(cameraName: "Cam 9", gateName: "Gate 1", imageName: "Cam1"),
        CameraFeed(cameraName: "Cam 10", gateName: "Gate 1", imageName: "Cam2"),
        // Add more mock data
    ]
}
