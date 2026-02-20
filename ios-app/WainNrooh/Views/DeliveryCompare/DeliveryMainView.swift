// DeliveryMainView.swift
// صفحة مقارنة التوصيل الرئيسية

import SwiftUI

// MARK: - صفحة التوصيل الرئيسية

/// صفحة مقارنة أسعار التوصيل — تعرض كل التطبيقات
struct DeliveryMainView: View {
    
    @StateObject private var viewModel = DeliveryViewModel()
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: Theme.spacingLarge) {
                    // العنوان والوصف
                    headerSection
                    
                    // تطبيقات التوصيل
                    appsSection
                    
                    // شرح الخدمة
                    infoSection
                    
                    Spacer(minLength: 80)
                }
            }
            .background(Color.appBackground)
            .navigationTitle("مقارنة التوصيل")
            .navigationBarTitleDisplayMode(.large)
        }
    }
    
    // MARK: - العنوان
    
    private var headerSection: some View {
        VStack(alignment: .trailing, spacing: 8) {
            Text("🛵 قارن أسعار التوصيل")
                .font(Theme.titleFont(size: 22))
                .foregroundStyle(Color.appTextPrimary)
            
            Text("ابحث عن مطعم وشوف أسعار التوصيل من 8 تطبيقات مختلفة — واختر الأرخص!")
                .font(Theme.bodyFont(size: 14))
                .foregroundStyle(Color.appTextSecondary)
                .multilineTextAlignment(.trailing)
        }
        .padding(.horizontal, Theme.paddingMedium)
        .padding(.top, Theme.paddingMedium)
    }
    
    // MARK: - تطبيقات التوصيل
    
    private var appsSection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            Text("التطبيقات المدعومة")
                .font(Theme.headlineFont(size: 16))
                .foregroundStyle(Color.appTextPrimary)
                .padding(.horizontal, Theme.paddingMedium)
            
            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible()),
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: Theme.spacingLarge) {
                ForEach(DeliveryApp.allCases) { app in
                    VStack(spacing: 8) {
                        AppLogo(app: app, size: .large, showName: false)
                        
                        Text(app.nameAr)
                            .font(Theme.captionFont(size: 11))
                            .foregroundStyle(Color.appTextPrimary)
                            .lineLimit(1)
                    }
                }
            }
            .padding(.horizontal, Theme.paddingMedium)
        }
    }
    
    // MARK: - معلومات
    
    private var infoSection: some View {
        VStack(alignment: .trailing, spacing: Theme.spacingMedium) {
            // كيف تعمل
            VStack(alignment: .trailing, spacing: 12) {
                Text("كيف يشتغل؟")
                    .font(Theme.headlineFont(size: 16))
                    .foregroundStyle(Color.appTextPrimary)
                
                infoRow(number: "1", text: "ابحث عن المطعم اللي تبيه")
                infoRow(number: "2", text: "شوف أسعار التوصيل من كل التطبيقات")
                infoRow(number: "3", text: "اختر الأرخص أو الأسرع")
                infoRow(number: "4", text: "اضغط واطلب مباشرة من التطبيق")
            }
            
            // ملاحظة
            HStack(spacing: 8) {
                Spacer()
                Text("الأسعار تتحدث كل 6 ساعات وممكن تختلف عن التطبيق")
                    .font(Theme.captionFont(size: 11))
                    .foregroundStyle(Color.appTextSecondary)
                    .multilineTextAlignment(.trailing)
                
                Image(systemName: "info.circle")
                    .font(.system(size: 14))
                    .foregroundStyle(Theme.warning)
            }
            .padding(Theme.paddingMedium)
            .background(Theme.warning.opacity(0.1))
            .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusSmall))
        }
        .padding(.horizontal, Theme.paddingMedium)
    }
    
    private func infoRow(number: String, text: String) -> some View {
        HStack(spacing: 12) {
            Spacer()
            
            Text(text)
                .font(Theme.bodyFont(size: 14))
                .foregroundStyle(Color.appTextPrimary)
                .multilineTextAlignment(.trailing)
            
            ZStack {
                Circle()
                    .fill(Theme.primary)
                    .frame(width: 28, height: 28)
                Text(number)
                    .font(.system(size: 14, weight: .bold))
                    .foregroundStyle(.white)
            }
        }
    }
}
