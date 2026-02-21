// MyPlacesView.swift
// مفضلاتي — قوائم محفوظة
// هوية ليالي الرياض

import SwiftUI

struct MyPlacesView: View {
    @EnvironmentObject var appState: AppState
    
    private var favoritePlaces: [Place] {
        appState.places.filter { appState.isFavorite($0.id) }
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // الهيدر
                HStack {
                    Spacer()
                    Text("❤️ مفضلاتي")
                        .font(Theme.title())
                        .foregroundStyle(.appTextPrimary)
                }
                .padding(Theme.spacingL)
                
                if favoritePlaces.isEmpty {
                    // فارغة
                    emptyState
                } else {
                    // القائمة
                    ScrollView(showsIndicators: false) {
                        LazyVStack(spacing: Theme.spacingM) {
                            Text("\(favoritePlaces.count) مكان محفوظ")
                                .font(Theme.caption())
                                .foregroundStyle(.appTextSecondary)
                                .frame(maxWidth: .infinity, alignment: .trailing)
                            
                            ForEach(favoritePlaces) { place in
                                NavigationLink {
                                    PlaceDetailView(place: place)
                                } label: {
                                    PlaceCard(place: place, style: .compact)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding(.horizontal, Theme.spacingL)
                        .padding(.bottom, 100)
                    }
                }
            }
            .background(Color.appBackground)
        }
    }
    
    // MARK: - حالة فارغة
    
    private var emptyState: some View {
        VStack(spacing: Theme.spacingXL) {
            Spacer()
            
            Image(systemName: "heart.slash")
                .font(.system(size: 50))
                .foregroundStyle(Theme.sand.opacity(0.4))
            
            VStack(spacing: Theme.spacingS) {
                Text("ما عندك مفضلات بعد")
                    .font(Theme.headline())
                    .foregroundStyle(.appTextPrimary)
                
                Text("اضغط ❤️ على أي مكان عشان تحفظه هنا")
                    .font(Theme.detail())
                    .foregroundStyle(.appTextSecondary)
                    .multilineTextAlignment(.center)
            }
            
            NavigationLink {
                ExploreView()
            } label: {
                Text("استكشف الأماكن")
                    .wainSecondaryButton()
            }
            
            Spacer()
        }
        .padding(Theme.spacingXL)
    }
}
