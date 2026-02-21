// ProfileView.swift
// حسابي — ملف شخصي + إعدادات + AI Chat

import SwiftUI
import SwiftData

struct ProfileView: View {
    @EnvironmentObject var appState: AppState
    @Environment(\.modelContext) private var modelContext
    @Query private var favorites: [CachedFavorite]
    @Query private var lists: [ShareableList]
    @AppStorage("isDarkMode") private var isDarkMode = true
    
    var body: some View {
        NavigationStack {
            List {
                // Profile Header
                Section {
                    HStack(spacing: 16) {
                        Spacer()
                        VStack(spacing: 8) {
                            ZStack {
                                Circle()
                                    .fill(Theme.primary.opacity(0.2))
                                    .frame(width: 70, height: 70)
                                Text(String(appState.currentUser?.name.prefix(1) ?? "؟"))
                                    .font(.title.bold())
                                    .foregroundStyle(Theme.primary)
                            }
                            Text(appState.currentUser?.name ?? "زائر")
                                .font(.headline)
                            Text(appState.currentUser?.phone ?? "")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                    }
                }
                
                // Stats
                Section("إحصائياتي") {
                    HStack {
                        Spacer()
                        StatItem(value: "\(favorites.count)", label: "مفضلة")
                        Spacer()
                        StatItem(value: "\(lists.count)", label: "قوائم")
                        Spacer()
                        StatItem(value: "0", label: "زيارات")
                        Spacer()
                    }
                }
                
                // AI Chat
                Section("المساعد الذكي") {
                    NavigationLink {
                        AIChatView()
                    } label: {
                        Label("🤖 اسأل عن أماكن الرياض", systemImage: "bubble.left.and.bubble.right")
                    }
                }
                
                // Settings
                Section("الإعدادات") {
                    Toggle(isOn: $isDarkMode) {
                        Label("الوضع الداكن", systemImage: "moon.fill")
                    }
                    
                    NavigationLink {
                        // Edit profile
                        Text("تعديل الملف الشخصي")
                    } label: {
                        Label("تعديل البيانات", systemImage: "person.fill")
                    }
                    
                    NavigationLink {
                        Text("الاهتمامات")
                    } label: {
                        Label("اهتماماتي", systemImage: "heart.text.square")
                    }
                }
                
                // About
                Section("عن التطبيق") {
                    HStack {
                        Text("v1.0.0")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        Spacer()
                        Text("الإصدار")
                    }
                    
                    HStack {
                        Text("\(appState.places.count)")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        Spacer()
                        Text("عدد الأماكن")
                    }
                }
                
                // Logout
                Section {
                    Button(role: .destructive) {
                        appState.logout()
                    } label: {
                        Label("تسجيل خروج", systemImage: "rectangle.portrait.and.arrow.right")
                            .foregroundStyle(.red)
                    }
                }
            }
            .navigationTitle("حسابي")
        }
    }
}

struct StatItem: View {
    let value: String
    let label: String
    
    var body: some View {
        VStack(spacing: 4) {
            Text(value)
                .font(.title2.bold())
                .foregroundStyle(Theme.primary)
            Text(label)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }
}
