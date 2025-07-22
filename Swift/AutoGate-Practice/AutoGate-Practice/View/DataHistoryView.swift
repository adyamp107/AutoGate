//
//  DataHistoryView.swift
//  AutoGate-Practice
//
//  Created by Miftah Fauzy on 22/07/25.
//

import SwiftUI

struct DataHistoryView: View {
    @Environment(\.colorScheme) var colorScheme
    @StateObject private var viewModel = DataHistoryViewModel()
    @State private var searchText = ""
    @State private var selectedDate = Date()
    @State private var showingDatePicker = false
    @State private var currentTime = getCurrentTime()
    
    var body: some View {
        VStack(spacing: 0) {
            // Account Header Section
            AccountHeaderView(currentTime: $currentTime)
            
            // Statistics Cards Section
            StatisticsSection()
            
            // Search and Table Section
            SearchAndTableSection(
                searchText: $searchText,
                selectedDate: $selectedDate,
                showingDatePicker: $showingDatePicker,
                colorScheme: colorScheme,
                viewModel: viewModel
            )
        }
        .navigationTitle("Monitor")
        .navigationSubtitle("Shift 1")
        .clipShape(BottomCornersRounded(radius: 12))
    }
}

// MARK: - Stat Card View
struct StatCardView: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        HStack(alignment: .top, spacing: 8) {
            Image(systemName: icon)
                .foregroundColor(.white)
                .font(.title2)
                .frame(width: 40, height: 40)
                .background(Color(hex: "#C70039"))
                .cornerRadius(8)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                Text(value)
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.primary)
            }
            
            Spacer() // Ini penting untuk mendorong konten ke kiri
        }
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(.controlBackgroundColor))
        .cornerRadius(12)
        .foregroundStyle(Color.white)
        .shadow(color: Color.black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct AccountHeaderView: View {
    @Binding var currentTime: String
    
    var body: some View {
        HStack {
            // Left: All Gate with icon
            HStack(spacing: 8) {
                Text("All Gate")
                    .font(.system(size: 16, weight: .semibold))
            }

            Spacer()

            // Center: Time and Shift
            HStack(spacing: 6) {
                Text(currentTime)
                    .font(.system(size: 14, weight: .regular))
                Circle()
                    .frame(width: 4, height: 4)
                Text("Shift 1")
                    .font(.system(size: 14, weight: .regular))
            }
            .foregroundColor(.secondary)

            Spacer()

            // Right: User
            HStack(spacing: 6) {
                Text("Fathur")
                    .font(.system(size: 14, weight: .regular))
                Circle()
                    .frame(width: 10, height: 10)
                    .foregroundColor(.gray) // status indicator
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        .background(Color(.windowBackgroundColor))
        .overlay(
            Divider(), alignment: .bottom
        )
        .onAppear {
            // Start timer for clock updates
            Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
                currentTime = getCurrentTime()
            }
        }
    }
}


struct StatisticsSection: View {
    var body: some View {
        // Header with statistics cards
        HStack(spacing: 20) {
            StatCardView(
                title: "Golongan I",
                value: "1324",
                icon: "car.fill",
                color: .red
            )
            
            StatCardView(
                title: "Golongan II",
                value: "1324",
                icon: "truck.box.fill",
                color: .red
            )
            
            StatCardView(
                title: "Golongan III",
                value: "1324",
                icon: "truck.box.fill",
                color: .red
            )
            
            StatCardView(
                title: "Golongan IV",
                value: "645",
                icon: "truck.box.fill",
                color: .red
            )
            
            StatCardView(
                title: "Golongan VI",
                value: "312",
                icon: "truck.box.fill",
                color: .red
            )
        }
        .padding(10)
    }
}

struct SearchAndTableSection: View {
    @Binding var searchText: String
    @Binding var selectedDate: Date
    @Binding var showingDatePicker: Bool
    let colorScheme: ColorScheme
    let viewModel: DataHistoryViewModel
    
    var body: some View {
        VStack(spacing: 0) {
            // Search and filter section
            SearchBarSection(
                searchText: $searchText,
                selectedDate: $selectedDate,
                showingDatePicker: $showingDatePicker,
                colorScheme: colorScheme
            )
            
            // Data table
            DataTableSection(viewModel: viewModel)
            
            // Pagination
            PaginationSection()
        }
        .padding(10)
        .clipShape(BottomCornersRounded(radius: 12))
    }
}

struct SearchBarSection: View {
    @Binding var searchText: String
    @Binding var selectedDate: Date
    @Binding var showingDatePicker: Bool
    let colorScheme: ColorScheme
    
    var body: some View {
        HStack(spacing: 12) {
            // Search bar
            SearchBar(searchText: $searchText, colorScheme: colorScheme)
            
            // Date picker button
            DatePickerButton(
                selectedDate: $selectedDate,
                showingDatePicker: $showingDatePicker,
                colorScheme: colorScheme
            )
            
            CustomDropdownView(colorScheme: colorScheme)
            
            // Download CSV button
            DownloadButton(colorScheme: colorScheme)
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 12)
        .background(Color(.controlBackgroundColor))
        .clipShape(TopCornersRounded(radius: 12))
    }
}


// MARK: - Search Bar Component
struct SearchBar: View {
    @Binding var searchText: String
    let colorScheme: ColorScheme
    
    var body: some View {
        HStack {
            Image(systemName: "magnifyingglass")
                .foregroundColor(.secondary)
            TextField("Search", text: $searchText)
                .textFieldStyle(.plain)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(
            colorScheme == .dark ? Color.black : Color(hex: "#F9FAFB")
        )
        .foregroundColor(
            colorScheme == .dark ? .white : .black
        )
        .cornerRadius(8)
        .frame(maxWidth: .infinity)
    }
}

// MARK: - Date Picker Button Component
struct DatePickerButton: View {
    @Binding var selectedDate: Date
    @Binding var showingDatePicker: Bool
    let colorScheme: ColorScheme
    
    var body: some View {
        Button(action: { showingDatePicker.toggle() }) {
            HStack {
                Image(systemName: "calendar")
                Text("Select date")
                Image(systemName: "chevron.down")
                    .font(.caption)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
        }
        .frame(maxWidth: 500, alignment: .leading)
        .background(
            colorScheme == .dark ? Color.black : Color(hex: "#F9FAFB")
        )
        .foregroundColor(
            colorScheme == .dark ? .white : .black
        )
        .cornerRadius(8)
        .buttonStyle(PlainButtonStyle())
        .popover(isPresented: $showingDatePicker) {
            VStack {
                Text("Select date")
                DatePicker("", selection: $selectedDate, displayedComponents: .date)
                    .datePickerStyle(GraphicalDatePickerStyle())
            }
            .padding()
        }
    }
}

struct CustomDropdownView: View {
    let colorScheme: ColorScheme
    
    var body: some View {
        HStack(spacing: 6) {
            Image(systemName: "clock")
                .font(.system(size: 14))
            Text("terdahulu")
                .font(.system(size: 14, weight: .medium))
            Image(systemName: "chevron.down")
                .font(.system(size: 12, weight: .medium))
                .foregroundColor(.gray)
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 6)
        .background(
            colorScheme == .dark ? Color.black : Color(hex: "#F9FAFB")
        )
        .foregroundColor(
            colorScheme == .dark ? .white : .black
        )
        .cornerRadius(8)
    }
}


// MARK: - Download Button Component
struct DownloadButton: View {
    let colorScheme: ColorScheme
    
    var body: some View {
        Button(action: {}) {
            HStack {
                Image(systemName: "square.and.arrow.down")
                Text("Download CSV")
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(
                colorScheme == .dark ? Color.black : Color(hex: "#F9FAFB")
            )
            .foregroundColor(
                colorScheme == .dark ? .white : .black
            )
            .cornerRadius(8)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct DataTableSection: View {
    let viewModel: DataHistoryViewModel
    
    var body: some View {
        Table(viewModel.entries) {
            TableColumn("NO") { entry in
                Text(entry.no.description)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .width(50)
            
            TableColumn("TANGGAL MASUK") { entry in
                Text(entry.tanggalMasuk)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .width(120)
            
            TableColumn("TANGGAL KELUAR") { entry in
                Text(entry.tanggalKeluar)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .width(120)
            
            TableColumn("WAKTU MASUK") { entry in
                Text(entry.waktuMasuk)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .width(100)
            
            TableColumn("WAKTU KELUAR") { entry in
                Text(entry.waktuKeluar)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .width(100)
            
            TableColumn("SHIFT") { entry in
                Text(entry.shift)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .width(80)
            
            TableColumn("PETUGAS") { entry in
                Text(entry.petugas)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .width(80)
            
            TableColumn("KEPALA") { entry in
                Text(entry.kepala)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .width(80)
            
            TableColumn("ACTION") { entry in
                Text(entry.action)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .width(80)
            
            TableColumn("STATUS") { entry in
                Text(entry.status)
                    .font(.caption)
                    .foregroundColor(.white)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(entry.status == "Sudah Divalidasi" ? Color.blue : Color(hex: "#C70039"))
                    .cornerRadius(4)
            }
            .width(120)
        }
        .tableStyle(InsetTableStyle())
        .frame(maxHeight: .infinity)
        .background(Color(hex: "#1E284E"))
    }
}

struct PaginationSection: View {
    var body: some View {
        HStack {
            Text("Showing 1-10 of 3")
                .font(.caption)
                .foregroundColor(.secondary)
            
            Spacer()
            
            HStack(spacing: 8) {
                Button(action: {}) {
                    Image(systemName: "chevron.left")
                        .font(.caption)
                }
                .buttonStyle(PlainButtonStyle())
                .disabled(true)
                
                Button("1") { }
                    .buttonStyle(PlainButtonStyle())
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color.accentColor)
                    .foregroundColor(.white)
                    .cornerRadius(4)
                
                Button("2") { }
                    .buttonStyle(PlainButtonStyle())
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                
                Button("3") { }
                    .buttonStyle(PlainButtonStyle())
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                
                Button(action: {}) {
                    Image(systemName: "chevron.right")
                        .font(.caption)
                }
                .buttonStyle(PlainButtonStyle())
            }
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 12)
        .background(Color(.controlBackgroundColor))
        .clipShape(BottomCornersRounded(radius: 12))
    }
}

