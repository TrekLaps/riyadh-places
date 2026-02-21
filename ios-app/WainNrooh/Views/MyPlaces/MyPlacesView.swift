// MyPlacesView.swift
// أماكني — Mapstr Pattern (personal map + favorites + shareable lists)

import SwiftUI
import SwiftData

struct MyPlacesView: View {
    @EnvironmentObject var appState: AppState
    @Environment(\.modelContext) private var modelContext
    @Query private var favorites: [CachedFavorite]
    @Query private var lists: [ShareableList]
    @State private var selectedTab = 0
    
    var favoritePlaces: [Place] {
        let favIds = Set(favorites.map(\.placeId))
        return appState.places.filter { favIds.contains($0.id) }
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Tab: المفضلة | قوائمي
                Picker("", selection: $selectedTab) {
                    Text("❤️ المفضلة (\(favorites.count))").tag(0)
                    Text("📋 قوائمي (\(lists.count))").tag(1)
                }
                .pickerStyle(.segmented)
                .padding()
                
                if selectedTab == 0 {
                    favoritesTab
                } else {
                    listsTab
                }
            }
            .navigationTitle("أماكني")
        }
    }
    
    // MARK: - Favorites Tab
    
    private var favoritesTab: some View {
        Group {
            if favoritePlaces.isEmpty {
                VStack(spacing: 16) {
                    Image(systemName: "heart.slash")
                        .font(.system(size: 48))
                        .foregroundStyle(.secondary)
                    Text("ما عندك أماكن مفضلة بعد")
                        .font(.headline)
                        .foregroundStyle(.secondary)
                    Text("اضغط ❤️ على أي مكان عشان تحفظه هنا")
                        .font(.caption)
                        .foregroundStyle(.tertiary)
                }
                .padding(.top, 60)
            } else {
                List {
                    ForEach(favoritePlaces) { place in
                        NavigationLink {
                            PlaceDetailView(place: place)
                        } label: {
                            PlaceListRow(place: place)
                        }
                    }
                    .onDelete { indexSet in
                        for i in indexSet {
                            let place = favoritePlaces[i]
                            if let fav = favorites.first(where: { $0.placeId == place.id }) {
                                modelContext.delete(fav)
                            }
                        }
                    }
                }
                
                // Share all favorites
                if !favoritePlaces.isEmpty {
                    Button {
                        shareAsList()
                    } label: {
                        Label("شارك أماكني", systemImage: "square.and.arrow.up")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Theme.primary)
                            .foregroundStyle(.white)
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                    .padding()
                }
            }
        }
    }
    
    // MARK: - Lists Tab
    
    private var listsTab: some View {
        Group {
            if lists.isEmpty {
                VStack(spacing: 16) {
                    Image(systemName: "list.bullet.clipboard")
                        .font(.system(size: 48))
                        .foregroundStyle(.secondary)
                    Text("ما عندك قوائم بعد")
                        .font(.headline)
                        .foregroundStyle(.secondary)
                    
                    Button {
                        createList()
                    } label: {
                        Label("أنشئ قائمة جديدة", systemImage: "plus")
                            .padding()
                            .background(Theme.primary)
                            .foregroundStyle(.white)
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                }
                .padding(.top, 60)
            } else {
                List {
                    ForEach(lists) { list in
                        VStack(alignment: .trailing, spacing: 4) {
                            Text(list.name)
                                .font(.headline)
                            Text("\(list.placeIds.count) مكان")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    .onDelete { indexSet in
                        for i in indexSet {
                            modelContext.delete(lists[i])
                        }
                    }
                }
                
                Button {
                    createList()
                } label: {
                    Label("قائمة جديدة", systemImage: "plus")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Theme.primary)
                        .foregroundStyle(.white)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                }
                .padding()
            }
        }
    }
    
    // MARK: - Actions
    
    private func shareAsList() {
        let ids = favoritePlaces.map(\.id)
        let list = ShareableList(name: "أماكني المفضلة", placeIds: ids)
        modelContext.insert(list)
        // TODO: share sheet with list.shareURL
    }
    
    private func createList() {
        let list = ShareableList(name: "قائمة جديدة")
        modelContext.insert(list)
    }
}
