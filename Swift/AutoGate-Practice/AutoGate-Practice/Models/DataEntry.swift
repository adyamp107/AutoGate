//
//  DataEntry.swift
//  AutoGate-Practice
//
//  Created by Miftah Fauzy on 22/07/25.
//

import Foundation

struct DataEntry: Identifiable {
    let id = UUID()
    let no: Int
    let tanggalMasuk: String
    let tanggalKeluar: String
    let waktuMasuk: String
    let waktuKeluar: String
    let shift: String
    let petugas: String
    let kepala: String
    let action: String
    let status: String
}
