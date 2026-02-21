// AuthView.swift
// تسجيل الدخول — رقم سعودي + OTP
// هوية ليالي الرياض

import SwiftUI

struct AuthView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var phoneNumber = ""
    @State private var otpCode = ""
    @State private var showOTP = false
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        ZStack {
            Color.appBackground.ignoresSafeArea()
            
            VStack(spacing: Theme.spacingXXL) {
                Spacer()
                
                // الشعار
                VStack(spacing: Theme.spacingM) {
                    Text("🏙")
                        .font(.system(size: 60))
                    
                    Text("وين نروح؟")
                        .font(Theme.largeTitle())
                        .foregroundStyle(.appTextPrimary)
                    
                    Text("سجّل عشان تحفظ مفضلاتك")
                        .font(Theme.body())
                        .foregroundStyle(.appTextSecondary)
                }
                
                Spacer()
                
                // الفورم
                VStack(spacing: Theme.spacingL) {
                    if !showOTP {
                        // إدخال رقم الجوال
                        phoneInput
                    } else {
                        // إدخال رمز التحقق
                        otpInput
                    }
                    
                    // رسالة خطأ
                    if let error = errorMessage {
                        Text(error)
                            .font(Theme.caption())
                            .foregroundStyle(Theme.error)
                            .multilineTextAlignment(.center)
                    }
                    
                    // زر الإرسال
                    Button {
                        if showOTP {
                            verifyOTP()
                        } else {
                            sendOTP()
                        }
                    } label: {
                        Group {
                            if isLoading {
                                ProgressView()
                                    .tint(.white)
                            } else {
                                Text(showOTP ? "تحقق" : "أرسل رمز التحقق")
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .wainPrimaryButton()
                    }
                    .disabled(showOTP ? otpCode.count < 4 : !isValidSaudiPhone)
                    .opacity(showOTP ? (otpCode.count < 4 ? 0.5 : 1) : (isValidSaudiPhone ? 1 : 0.5))
                }
                .padding(.horizontal, Theme.spacingXL)
                
                Spacer()
                
                // الشروط
                Text("بالتسجيل أنت توافق على شروط الاستخدام")
                    .font(Theme.badge())
                    .foregroundStyle(.appTextSecondary)
                    .padding(.bottom, Theme.spacingXL)
            }
        }
    }
    
    // MARK: - إدخال رقم الجوال
    
    private var phoneInput: some View {
        HStack(spacing: Theme.spacingM) {
            TextField("5XXXXXXXX", text: $phoneNumber)
                .font(Theme.title())
                .keyboardType(.phonePad)
                .multilineTextAlignment(.center)
                .foregroundStyle(.appTextPrimary)
            
            Text("🇸🇦 966+")
                .font(Theme.body())
                .foregroundStyle(.appTextSecondary)
        }
        .padding(Theme.spacingL)
        .background(Color.appCardBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous)
                .stroke(isValidSaudiPhone ? Theme.green400.opacity(0.3) : .clear, lineWidth: 1)
        )
    }
    
    // MARK: - إدخال OTP
    
    private var otpInput: some View {
        VStack(spacing: Theme.spacingM) {
            Text("أرسلنا رمز التحقق لـ \(formattedPhone)")
                .font(Theme.detail())
                .foregroundStyle(.appTextSecondary)
                .multilineTextAlignment(.center)
            
            TextField("رمز التحقق", text: $otpCode)
                .font(Theme.largeTitle())
                .keyboardType(.numberPad)
                .multilineTextAlignment(.center)
                .foregroundStyle(.appTextPrimary)
                .padding(Theme.spacingL)
                .background(Color.appCardBackground)
                .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
            
            Button("أرسل مرة ثانية") {
                sendOTP()
            }
            .font(Theme.caption())
            .foregroundStyle(Theme.green400)
        }
    }
    
    // MARK: - Validation
    
    private var isValidSaudiPhone: Bool {
        let cleaned = phoneNumber.replacingOccurrences(of: " ", with: "")
        return cleaned.count >= 9 && cleaned.hasPrefix("5")
    }
    
    private var formattedPhone: String {
        "+966 \(phoneNumber)"
    }
    
    // MARK: - Actions
    
    private func sendOTP() {
        guard isValidSaudiPhone else { return }
        isLoading = true
        errorMessage = nil
        
        // TODO: ربط مع Firebase Auth أو Twilio
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            isLoading = false
            showOTP = true
        }
    }
    
    private func verifyOTP() {
        guard otpCode.count >= 4 else { return }
        isLoading = true
        errorMessage = nil
        
        // TODO: تحقق من OTP
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            isLoading = false
            dismiss()
        }
    }
}
