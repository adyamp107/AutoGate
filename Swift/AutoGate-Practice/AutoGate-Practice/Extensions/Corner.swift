//
//  Corner.swift
//  AutoGate-Practice
//
//  Created by Miftah Fauzy on 22/07/25.
//

import SwiftUI

struct TopCornersRounded: Shape {
    let radius: CGFloat
    
    func path(in rect: CGRect) -> Path {
        var path = Path()
        
        path.move(to: CGPoint(x: 0, y: radius))
        path.addArc(center: CGPoint(x: radius, y: radius), radius: radius, startAngle: Angle(radians: .pi), endAngle: Angle(radians: 3 * .pi / 2), clockwise: false)
        
        path.addLine(to: CGPoint(x: rect.width - radius, y: 0))
        path.addArc(center: CGPoint(x: rect.width - radius, y: radius), radius: radius, startAngle: Angle(radians: 3 * .pi / 2), endAngle: Angle(radians: 0), clockwise: false)
        
        path.addLine(to: CGPoint(x: rect.width, y: rect.height))
        path.addLine(to: CGPoint(x: 0, y: rect.height))
        path.closeSubpath()
        
        return path
    }
}

struct BottomCornersRounded: Shape {
    let radius: CGFloat
    
    func path(in rect: CGRect) -> Path {
        var path = Path()
        
        path.move(to: CGPoint(x: 0, y: 0))
        path.addLine(to: CGPoint(x: rect.width, y: 0))
        path.addLine(to: CGPoint(x: rect.width, y: rect.height - radius))
        
        path.addArc(center: CGPoint(x: rect.width - radius, y: rect.height - radius), radius: radius, startAngle: Angle(radians: 0), endAngle: Angle(radians: .pi / 2), clockwise: false)
        
        path.addLine(to: CGPoint(x: radius, y: rect.height))
        path.addArc(center: CGPoint(x: radius, y: rect.height - radius), radius: radius, startAngle: Angle(radians: .pi / 2), endAngle: Angle(radians: .pi), clockwise: false)
        
        path.closeSubpath()
        
        return path
    }
}

