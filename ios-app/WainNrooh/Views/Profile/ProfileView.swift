// ProfileView.swift
// حسابي — إحصائيات + إعدادات
// هوية ليالي الرياض

import SwiftUI

struct ProfileView: View {
    @EnvironmentObject var appState: AppState
    @State private var showAuth = false
    @State private var showSettings = false
    @AppStorage("isLoggedIn") private var isLoggedIn = false
    @AppStorage("userName") private var userName = ""
    
    var body: some View {
        NavigationStack {
            ScrollView(showsIndicators: false) {
                VStack(spacing: Theme.spacingXL) {
                    // الهيدر
                    profileHeader
                    
                    // الإحصائيات
                    statsSection
                    
                    // القائمة
                    menuSection
                    
                    // عن التطبيق
                    aboutSection
                    
                    Spacer(minLength: 100)
                }
                .padding(.top, Theme.spacingL)
            }
            .background(Color.appBackground)
            .navigationBarHidden(true)
            .sheet(isPresented: $showAuth) {
                AuthView()
            }
        }
    }
    
    // MARK: - الهيدر
    
    private var profileHeader: some View {
        VStack(spacing: Theme.spacingM) {
            // الصورة الرمزية
            ZStack {
                Circle()
                    .fill(Theme.primaryGradient)
                    .frame(width: 80, height: 80)
                
                Text(isLoggedIn && !userName.isEmpty ? String(userName.prefix(1)) : "👤")
                    .font(.system(size: isLoggedIn ? 32 : 36))
                    .foregroundStyle(.white)
            }
            
            if isLoggedIn {
                Text(userName.isEmpty ? "مستخدم" : userName)
                    .font(Theme.title())
                    .foregroundStyle(.appTextPrimary)
            } else {
                Button {
                    showAuth = true
                } label: {
                    Text("سجّل دخولك")
                        .wainPrimaryButton()
                }
            }
        }
        .padding(.horizontal, Theme.spacingL)
    }
    
    // MARK: - الإحصائيات
    
    private var statsSection: some View {
        HStack(spacing: Theme.spacingL) {
            statCard(
                value: "\(appState.favorites.count)",
                label: "مفضلاتي",
                icon: "heart.fill",
                color: Theme.error
            )
            
            statCard(
                value: "\(appState.places.count)",
                label: "مكان متاح",
                icon: "mappin.circle.fill",
                color: Theme.green400
            )
            
            statCard(
                value: "١١",
                label: "تصنيف",
                icon: "square.grid.2x2.fill",
                color: Theme.gold500
            )
        }
        .padding(.horizontal, Theme.spacingL)
    }
    
    private func statCard(value: String, label: String, icon: String, color: Color) -> some View {
        VStack(spacing: Theme.spacingS) {
            Image(systemName: icon)
                .font(.system(size: 20))
                .foregroundStyle(color)
            
            Text(value)
                .font(Theme.title(size: 20))
                .foregroundStyle(.appTextPrimary)
            
            Text(label)
                .font(Theme.badge())
                .foregroundStyle(.appTextSecondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, Theme.spacingL)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.radiusMedium, style: .continuous))
    }
    
    // MARK: - القائمة
    
    private var menuSection: some View {
        VStack(spacing: 1) {
            menuRow(icon: "heart.fill", title: "المفضلات", color: Theme.error) {
                // navigate to favorites
            }
            
            menuRow(icon: "clock.fill", title: "آخر الزيارات", color: Theme.info) {
                // navigate to history
            }
            
            menuRow(icon: "sparkles", title: "اسأل الذكاء", color: Theme.gold500) {
                // navigate to AI
            }
            
            menuRow(icon: "gearshape.fill", title: "الإعدادات", color: Theme.sand) {
                showSettings = true
            }
        }
        .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
        .padding(.horizontal, Theme.spacingL)
    }
    
    private func menuRow(icon: String, title: String, color: Color, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            HStack(spacing: Theme.spacingM) {
                Image(systemName: "chevron.left")
                    .font(.system(size: 12))
                    .foregroundStyle(.appTextSecondary)
                
                Spacer()
                
                Text(title)
                    .font(Theme.body())
                    .foregroundStyle(.appTextPrimary)
                
                Image(systemName: icon)
                    .font(.system(size: 16))
                    .foregroundStyle(color)
                    .frame(width: 32, height: 32)
                    .background(color.opacity(0.1))
                    .clipShape(Circle())
            }
            .padding(Theme.spacingL)
            .background(Color.appCardBackground)
        }
    }
    
    // MARK: - عن التطبيق
    
    private var aboutSection: some View {
        VStack(spacing: Theme.spacingS) {
            Text("وين نروح بالرياض؟ 🏙")
                .font(Theme.detail())
                .foregroundStyle(.appTextSecondary)
            
            Text("الإصدار ١.٠.٠")
                .font(Theme.badge())
                .foregroundStyle(.appTextSecondary.opacity(0.6))
        }
        .padding(.top, Theme.spacingXL)
    }
}
