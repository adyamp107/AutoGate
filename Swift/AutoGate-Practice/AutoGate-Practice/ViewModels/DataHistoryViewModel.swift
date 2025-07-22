//
//  DataHistoryViewModel.swift
//  AutoGate-Practice
//
//  Created by Miftah Fauzy on 22/07/25.
//

import SwiftUI

class DataHistoryViewModel: ObservableObject {
    @Published var entries: [DataEntry] = [
        DataEntry(no: 1, tanggalMasuk: "25-06-2025", tanggalKeluar: "25-06-2025", waktuMasuk: "14:30:00", waktuKeluar: "14:30:02", shift: "Shift 1", petugas: "Fathur", kepala: "Abim", action: "sudah", status: "Sudah Divalidasi"),
        DataEntry(no: 2, tanggalMasuk: "25-06-2025", tanggalKeluar: "25-06-2025", waktuMasuk: "14:31:02", waktuKeluar: "14:31:03", shift: "Shift 1", petugas: "Fathur", kepala: "Abim", action: "sudah", status: "Belum Divalidasi"),
        // Add more mock data
    ]
}
