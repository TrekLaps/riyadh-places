// AIChatView.swift
// الذكاء الاصطناعي — محادثة عربية
// Phase 1: Rule-based → Phase 2: LLM

import SwiftUI

struct AIChatView: View {
    @EnvironmentObject var appState: AppState
    var initialPlace: Place? = nil
    
    @State private var messages: [ChatMessage] = []
    @State private var inputText = ""
    @State private var isTyping = false
    
    var body: some View {
        VStack(spacing: 0) {
            // الهيدر
            header
            
            // المحادثة
            ScrollViewReader { proxy in
                ScrollView(showsIndicators: false) {
                    LazyVStack(spacing: Theme.spacingM) {
                        ForEach(messages) { message in
                            chatBubble(message)
                        }
                        
                        if isTyping {
                            typingIndicator
                        }
                    }
                    .padding(Theme.spacingL)
                }
                .onChange(of: messages.count) { _ in
                    if let last = messages.last {
                        withAnimation {
                            proxy.scrollTo(last.id, anchor: .bottom)
                        }
                    }
                }
            }
            
            // الإدخال
            inputBar
        }
        .background(Color.appBackground)
        .onAppear {
            sendWelcome()
        }
    }
    
    // MARK: - الهيدر
    
    private var header: some View {
        HStack {
            Spacer()
            
            VStack(spacing: 2) {
                Text("🤖 مساعد وين نروح")
                    .font(Theme.headline(size: 16))
                    .foregroundStyle(.appTextPrimary)
                
                Text("اسألني وش تبي وأنا أرشحلك")
                    .font(Theme.badge())
                    .foregroundStyle(.appTextSecondary)
            }
            
            Spacer()
        }
        .padding(Theme.spacingL)
        .background(.ultraThinMaterial)
    }
    
    // MARK: - فقاعة المحادثة
    
    private func chatBubble(_ message: ChatMessage) -> some View {
        HStack {
            if message.isUser { Spacer(minLength: 60) }
            
            VStack(alignment: message.isUser ? .trailing : .leading, spacing: Theme.spacingXS) {
                Text(message.text)
                    .font(Theme.body(size: 15))
                    .foregroundStyle(message.isUser ? .white : .appTextPrimary)
                    .multilineTextAlignment(message.isUser ? .trailing : .leading)
                
                // لو فيه أماكن مقترحة
                if let places = message.suggestedPlaces, !places.isEmpty {
                    VStack(spacing: Theme.spacingS) {
                        ForEach(places) { place in
                            NavigationLink {
                                PlaceDetailView(place: place)
                            } label: {
                                HStack(spacing: Theme.spacingS) {
                                    VStack(alignment: .trailing, spacing: 2) {
                                        Text(place.nameAr)
                                            .font(Theme.detail().bold())
                                            .foregroundStyle(.appTextPrimary)
                                        if let hood = place.neighborhood {
                                            Text(hood)
                                                .font(Theme.badge())
                                                .foregroundStyle(.appTextSecondary)
                                        }
                                    }
                                    Spacer()
                                    if let r = place.googleRating {
                                        HStack(spacing: 2) {
                                            Text(String(format: "%.1f", r))
                                                .font(Theme.badge().bold())
                                            Image(systemName: "star.fill")
                                                .font(.system(size: 8))
                                                .foregroundStyle(Theme.gold500)
                                        }
                                    }
                                }
                                .padding(Theme.spacingM)
                                .background(Color.appCardBackground)
                                .clipShape(RoundedRectangle(cornerRadius: Theme.radiusMedium, style: .continuous))
                            }
                        }
                    }
                }
            }
            .padding(Theme.spacingM)
            .background(
                message.isUser
                    ? AnyShapeStyle(Theme.primaryGradient)
                    : AnyShapeStyle(Color.appCardBackground)
            )
            .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
            .id(message.id)
            
            if !message.isUser { Spacer(minLength: 60) }
        }
    }
    
    // MARK: - مؤشر الكتابة
    
    private var typingIndicator: some View {
        HStack {
            Spacer()
            HStack(spacing: 4) {
                ForEach(0..<3) { i in
                    Circle()
                        .fill(Theme.green400)
                        .frame(width: 6, height: 6)
                        .opacity(0.6)
                }
            }
            .padding(Theme.spacingM)
            .background(Color.appCardBackground)
            .clipShape(RoundedRectangle(cornerRadius: Theme.radiusLarge, style: .continuous))
        }
    }
    
    // MARK: - شريط الإدخال
    
    private var inputBar: some View {
        HStack(spacing: Theme.spacingM) {
            // زر الإرسال
            Button {
                sendMessage()
            } label: {
                Image(systemName: "arrow.up.circle.fill")
                    .font(.system(size: 32))
                    .foregroundStyle(inputText.isEmpty ? Theme.sand.opacity(0.3) : Theme.green400)
            }
            .disabled(inputText.isEmpty)
            
            // حقل الإدخال
            TextField("اكتب سؤالك هنا...", text: $inputText)
                .font(Theme.body())
                .foregroundStyle(.appTextPrimary)
                .multilineTextAlignment(.trailing)
                .padding(Theme.spacingM)
                .background(Color.appCardBackground)
                .clipShape(RoundedRectangle(cornerRadius: Theme.radiusXL, style: .continuous))
                .onSubmit {
                    sendMessage()
                }
        }
        .padding(Theme.spacingL)
        .background(.ultraThinMaterial)
    }
    
    // MARK: - Logic
    
    private func sendWelcome() {
        let welcome: String
        if let place = initialPlace {
            welcome = "أهلاً! تبي تعرف أكثر عن \(place.nameAr)؟ اسألني أي شي 😊"
        } else {
            welcome = "أهلاً! أنا مساعد وين نروح 🏙\nقولّي وش تبي تسوي وأنا أرشحلك أماكن حلوة بالرياض"
        }
        
        messages.append(ChatMessage(text: welcome, isUser: false))
    }
    
    private func sendMessage() {
        guard !inputText.trimmingCharacters(in: .whitespaces).isEmpty else { return }
        
        let userText = inputText
        messages.append(ChatMessage(text: userText, isUser: true))
        inputText = ""
        isTyping = true
        
        // Rule-based response (Phase 1)
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            let response = generateResponse(for: userText)
            isTyping = false
            messages.append(response)
        }
    }
    
    private func generateResponse(for query: String) -> ChatMessage {
        let q = query.lowercased()
        
        // بحث بالفئة
        if q.contains("مطعم") || q.contains("أكل") || q.contains("عشاء") || q.contains("غداء") {
            let places = appState.places.filter { $0.category == "restaurants" }
                .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            return ChatMessage(
                text: "هذي أفضل المطاعم اللي عندنا 🍽",
                isUser: false,
                suggestedPlaces: Array(places.prefix(3))
            )
        }
        
        if q.contains("قهوة") || q.contains("كافيه") || q.contains("كوفي") {
            let places = appState.places.filter { $0.category == "cafes" }
                .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            return ChatMessage(
                text: "تبي قهوة حلوة؟ هذي أفضل الكافيهات ☕️",
                isUser: false,
                suggestedPlaces: Array(places.prefix(3))
            )
        }
        
        if q.contains("ترفيه") || q.contains("طلعة") || q.contains("نطلع") {
            let places = appState.places.filter { $0.category == "entertainment" }
                .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            return ChatMessage(
                text: "فيه أماكن حلوة للترفيه 🎉",
                isUser: false,
                suggestedPlaces: Array(places.prefix(3))
            )
        }
        
        if q.contains("عوائل") || q.contains("عائلة") || q.contains("أطفال") {
            let places = appState.places.filter {
                $0.perfectFor?.contains("عوائل") ?? false || $0.audience == "عوائل"
            }
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            return ChatMessage(
                text: "أماكن عائلية ممتازة 👨‍👩‍👧‍👦",
                isUser: false,
                suggestedPlaces: Array(places.prefix(3))
            )
        }
        
        // بحث عام بالاسم
        let nameMatches = appState.places.filter {
            $0.nameAr.localizedCaseInsensitiveContains(q) ||
            ($0.nameEn?.localizedCaseInsensitiveContains(q) ?? false)
        }
        if !nameMatches.isEmpty {
            return ChatMessage(
                text: "لقيت لك هذي 👇",
                isUser: false,
                suggestedPlaces: Array(nameMatches.prefix(3))
            )
        }
        
        // ما فهمت
        return ChatMessage(
            text: "ما قدرت أفهم طلبك 😅\nجرّب تقول مثلاً:\n• \"أبي مطعم حلو\"\n• \"كافيه للدراسة\"\n• \"مكان عائلي\"",
            isUser: false
        )
    }
}

// MARK: - ChatMessage

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let isUser: Bool
    var suggestedPlaces: [Place]? = nil
}
