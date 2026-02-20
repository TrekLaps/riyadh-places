// AppLogo.swift
// شعارات تطبيقات التوصيل

import SwiftUI

// MARK: - شعار تطبيق التوصيل

/// عرض شعار تطبيق التوصيل مع اسمه
struct AppLogo: View {
    let app: DeliveryApp
    var size: LogoSize = .medium
    var showName: Bool = true
    
    enum LogoSize {
        case small, medium, large
        
        var iconSize: CGFloat {
            switch self {
            case .small: return 28
            case .medium: return 40
            case .large: return 56
            }
        }
        
        var fontSize: CGFloat {
            switch self {
            case .small: return 10
            case .medium: return 12
            case .large: return 14
            }
        }
    }
    
    var body: some View {
        VStack(spacing: 4) {
            // أيقونة التطبيق
            ZStack {
                RoundedRectangle(cornerRadius: size.iconSize * 0.22)
                    .fill(app.brandColor.gradient)
                    .frame(width: size.iconSize, height: size.iconSize)
                
                // حرف التطبيق كـ placeholder
                Text(app.nameEn.prefix(1).uppercased())
                    .font(.system(size: size.iconSize * 0.45, weight: .bold, design: .rounded))
                    .foregroundStyle(.white)
            }
            
            // اسم التطبيق
            if showName {
                Text(app.nameAr)
                    .font(.system(size: size.fontSize, weight: .medium))
                    .foregroundStyle(Color.appTextPrimary)
                    .lineLimit(1)
            }
        }
    }
}

// MARK: - صف شعارات التطبيقات

/// عرض كل شعارات تطبيقات التوصيل في صف
struct DeliveryAppsRow: View {
    var apps: [DeliveryApp] = DeliveryApp.allCases
    var size: AppLogo.LogoSize = .medium
    var onAppTap: ((DeliveryApp) -> Void)?
    
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: Theme.spacingMedium) {
                ForEach(apps) { app in
                    Button {
                        onAppTap?(app)
                    } label: {
                        AppLogo(app: app, size: size)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, Theme.paddingMedium)
        }
    }
}

// MARK: - Preview

#Preview {
    VStack(spacing: 24) {
        // أحجام مختلفة
        HStack(spacing: 16) {
            AppLogo(app: .hungerstation, size: .small)
            AppLogo(app: .jahez, size: .medium)
            AppLogo(app: .keeta, size: .large)
        }
        
        Divider()
        
        // صف كامل
        DeliveryAppsRow()
    }
    .padding()
    .background(Color.appBackground)
}
