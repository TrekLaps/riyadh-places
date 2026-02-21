// AuthView.swift
// تسجيل دخول / حساب جديد — Saudi phone validation

import SwiftUI

struct AuthView: View {
    @EnvironmentObject var appState: AppState
    @State private var isLogin = true
    @State private var name = ""
    @State private var phone = ""
    @State private var email = ""
    @State private var password = ""
    @State private var selectedInterests: Set<String> = []
    @State private var showError = false
    @State private var errorMessage = ""
    
    let interests = [
        ("restaurant", "مطاعم", "fork.knife"),
        ("cafe", "كافيهات", "cup.and.saucer.fill"),
        ("entertainment", "ترفيه", "sparkles"),
        ("shopping", "تسوق", "bag.fill"),
        ("nature", "طبيعة", "leaf.fill"),
        ("family", "عائلي", "figure.2.and.child"),
    ]
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Logo
                    Text("وين نروح؟")
                        .font(.system(size: 36, weight: .bold))
                        .foregroundStyle(Theme.primary)
                        .padding(.top, 40)
                    
                    // Tab Switch
                    Picker("", selection: $isLogin) {
                        Text("دخول").tag(true)
                        Text("حساب جديد").tag(false)
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal)
                    
                    if isLogin {
                        loginForm
                    } else {
                        registerForm
                    }
                    
                    // Social Login
                    socialLoginButtons
                }
                .padding()
            }
            .environment(\.layoutDirection, .rightToLeft)
            .alert("خطأ", isPresented: $showError) {
                Button("حسناً") {}
            } message: {
                Text(errorMessage)
            }
        }
    }
    
    // MARK: - Login Form
    
    private var loginForm: some View {
        VStack(spacing: 16) {
            TextField("رقم الجوال أو البريد", text: $phone)
                .textFieldStyle(.roundedBorder)
                .keyboardType(.phonePad)
            
            SecureField("كلمة المرور", text: $password)
                .textFieldStyle(.roundedBorder)
            
            Button("نسيت كلمة المرور؟") {}
                .font(.caption)
                .foregroundStyle(Theme.primary)
            
            Button {
                login()
            } label: {
                Text("دخول")
                    .font(.headline)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Theme.primary)
                    .foregroundStyle(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
            }
            
            // Skip login
            Button {
                skipLogin()
            } label: {
                Text("تصفّح بدون حساب")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
        }
    }
    
    // MARK: - Register Form
    
    private var registerForm: some View {
        VStack(spacing: 16) {
            TextField("الاسم", text: $name)
                .textFieldStyle(.roundedBorder)
            
            TextField("رقم الجوال (05xxxxxxxx)", text: $phone)
                .textFieldStyle(.roundedBorder)
                .keyboardType(.phonePad)
            
            TextField("البريد الإلكتروني (اختياري)", text: $email)
                .textFieldStyle(.roundedBorder)
                .keyboardType(.emailAddress)
            
            SecureField("كلمة المرور (8 أحرف على الأقل)", text: $password)
                .textFieldStyle(.roundedBorder)
            
            // Interests
            VStack(alignment: .trailing, spacing: 8) {
                Text("اهتماماتك:")
                    .font(.headline)
                
                LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 3), spacing: 8) {
                    ForEach(interests, id: \.0) { id, name, icon in
                        Button {
                            if selectedInterests.contains(id) {
                                selectedInterests.remove(id)
                            } else {
                                selectedInterests.insert(id)
                            }
                        } label: {
                            VStack(spacing: 4) {
                                Image(systemName: icon)
                                    .font(.title3)
                                Text(name)
                                    .font(.caption)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 12)
                            .background(selectedInterests.contains(id) ? Theme.primary.opacity(0.2) : Color(.systemGray6))
                            .foregroundStyle(selectedInterests.contains(id) ? Theme.primary : .primary)
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                            .overlay(
                                RoundedRectangle(cornerRadius: 12)
                                    .stroke(selectedInterests.contains(id) ? Theme.primary : .clear, lineWidth: 2)
                            )
                        }
                    }
                }
            }
            
            Button {
                register()
            } label: {
                Text("سجّل")
                    .font(.headline)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Theme.primary)
                    .foregroundStyle(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
            }
        }
    }
    
    // MARK: - Social Login
    
    private var socialLoginButtons: some View {
        VStack(spacing: 12) {
            Text("أو").foregroundStyle(.secondary)
            
            Button {} label: {
                Label("سجّل بحساب Apple", systemImage: "apple.logo")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(.black)
                    .foregroundStyle(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
            }
            
            Button {} label: {
                Label("سجّل بحساب Google", systemImage: "g.circle.fill")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color(.systemGray6))
                    .foregroundStyle(.primary)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
            }
        }
    }
    
    // MARK: - Actions
    
    private func login() {
        guard !phone.isEmpty, !password.isEmpty else {
            errorMessage = "ادخل رقم الجوال وكلمة المرور"
            showError = true
            return
        }
        let user = UserProfile(name: "مستخدم", phone: phone)
        appState.login(user: user)
    }
    
    private func register() {
        guard !name.isEmpty else {
            errorMessage = "ادخل اسمك"
            showError = true
            return
        }
        guard phone.hasPrefix("05"), phone.count == 10 else {
            errorMessage = "رقم الجوال لازم يبدأ بـ 05 ويكون 10 أرقام"
            showError = true
            return
        }
        guard password.count >= 8 else {
            errorMessage = "كلمة المرور لازم 8 أحرف على الأقل"
            showError = true
            return
        }
        let user = UserProfile(
            name: name, phone: phone, email: email.isEmpty ? nil : email,
            interests: Array(selectedInterests)
        )
        appState.login(user: user)
    }
    
    private func skipLogin() {
        let guest = UserProfile(name: "زائر", phone: "0500000000")
        appState.login(user: guest)
    }
}
