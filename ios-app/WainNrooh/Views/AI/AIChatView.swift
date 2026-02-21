// AIChatView.swift
// AI Chatbot — يفهم عربي سعودي ويقترح أماكن
// Phase 1: Rule-based | Phase 2: OpenAI API

import SwiftUI

struct AIChatView: View {
    @EnvironmentObject var appState: AppState
    @State private var messages: [ChatMessage] = [
        ChatMessage(text: "أهلاً! أنا مساعدك لاكتشاف أماكن الرياض 🏙️\nاسألني مثل: \"وين أروح مع العائلة؟\" أو \"أبي كافيه هادي بالعليا\"", isUser: false)
    ]
    @State private var inputText = ""
    @FocusState private var isInputFocused: Bool
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Messages
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(spacing: 12) {
                            ForEach(messages) { msg in
                                ChatBubble(message: msg)
                                    .id(msg.id)
                            }
                        }
                        .padding()
                    }
                    .onChange(of: messages.count) { _, _ in
                        if let last = messages.last {
                            proxy.scrollTo(last.id, anchor: .bottom)
                        }
                    }
                }
                
                Divider()
                
                // Input
                HStack(spacing: 8) {
                    Button {
                        sendMessage()
                    } label: {
                        Image(systemName: "arrow.up.circle.fill")
                            .font(.title2)
                            .foregroundStyle(inputText.isEmpty ? .secondary : Theme.primary)
                    }
                    .disabled(inputText.isEmpty)
                    
                    TextField("اسأل عن أي مكان بالرياض...", text: $inputText)
                        .textFieldStyle(.roundedBorder)
                        .focused($isInputFocused)
                        .onSubmit { sendMessage() }
                }
                .padding()
            }
            .navigationTitle("🤖 المساعد الذكي")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
    
    // MARK: - Send Message
    
    private func sendMessage() {
        let text = inputText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !text.isEmpty else { return }
        
        // Add user message
        messages.append(ChatMessage(text: text, isUser: true))
        inputText = ""
        
        // Generate response (rule-based for MVP)
        Task {
            try? await Task.sleep(for: .milliseconds(500))
            let response = generateResponse(for: text)
            messages.append(ChatMessage(text: response.text, isUser: false, places: response.places))
        }
    }
    
    // MARK: - Rule-Based Response (Phase 1)
    
    private func generateResponse(for query: String) -> (text: String, places: [Place]) {
        let q = query.lowercased()
        var category: String?
        var neighborhood: String?
        var occasion: Occasion?
        
        // Detect category
        if q.contains("مطعم") || q.contains("أكل") || q.contains("غداء") || q.contains("عشاء") {
            category = "restaurant"
        } else if q.contains("كافيه") || q.contains("قهوة") || q.contains("كوفي") {
            category = "cafe"
        } else if q.contains("حلويات") || q.contains("كيك") || q.contains("آيسكريم") {
            category = "desserts"
        } else if q.contains("ترفيه") || q.contains("ملاهي") || q.contains("ألعاب") {
            category = "entertainment"
        } else if q.contains("تسوق") || q.contains("مول") || q.contains("محل") {
            category = "shopping"
        }
        
        // Detect occasion
        if q.contains("عائل") || q.contains("أطفال") || q.contains("عيال") {
            occasion = .family
        } else if q.contains("رومانسي") || q.contains("زوجت") || q.contains("حبيب") {
            occasion = .romantic
        } else if q.contains("شباب") || q.contains("أصدقاء") || q.contains("ربع") {
            occasion = .friends
        } else if q.contains("هادي") || q.contains("هادئ") || q.contains("قراءة") {
            occasion = .quiet
        } else if q.contains("بزنس") || q.contains("اجتماع") || q.contains("عمل") {
            occasion = .business
        }
        
        // Detect neighborhood
        let neighborhoods = ["العليا", "النرجس", "الملقا", "العقيق", "الياسمين", "السليمانية", "الورود", "الصحافة", "حطين", "الربيع"]
        for hood in neighborhoods {
            if q.contains(hood) { neighborhood = hood; break }
        }
        
        // Filter places
        var results = appState.places
        if let cat = category {
            results = results.filter { ($0.categoryEn ?? $0.category) == cat }
        }
        if let occ = occasion {
            results = results.filter { $0.occasions.contains(occ) }
        }
        if let hood = neighborhood {
            results = results.filter { $0.neighborhood?.contains(hood) ?? false }
        }
        
        let topResults = results
            .sorted { ($0.googleRating ?? 0) > ($1.googleRating ?? 0) }
            .prefix(5).map { $0 }
        
        // Generate response text
        if topResults.isEmpty {
            return ("ما لقيت نتائج مطابقة 😅 جرّب تسأل بطريقة ثانية", [])
        }
        
        var text = "عندك كم خيار حلو"
        if let hood = neighborhood { text += " بـ\(hood)" }
        text += ":\n\n"
        
        for (i, p) in topResults.enumerated() {
            text += "\(i + 1). **\(p.nameAr)**"
            if let r = p.googleRating { text += " ⭐ \(String(format: "%.1f", r))" }
            if let price = p.priceLevel { text += " • \(price)" }
            text += "\n"
            if let desc = p.descriptionAr { text += "   \(String(desc.prefix(80)))\n" }
        }
        
        text += "\nتبي تفاصيل أكثر عن أي واحد؟ 😊"
        
        return (text, topResults)
    }
}

// MARK: - Chat Models

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let isUser: Bool
    let places: [Place]
    let timestamp = Date()
    
    init(text: String, isUser: Bool, places: [Place] = []) {
        self.text = text
        self.isUser = isUser
        self.places = places
    }
}

// MARK: - Chat Bubble

struct ChatBubble: View {
    let message: ChatMessage
    
    var body: some View {
        HStack {
            if message.isUser { Spacer(minLength: 60) }
            
            VStack(alignment: message.isUser ? .trailing : .leading, spacing: 8) {
                Text(message.text)
                    .font(.subheadline)
                    .padding(12)
                    .background(message.isUser ? Theme.primary : Color(.secondarySystemBackground))
                    .foregroundStyle(message.isUser ? .white : .primary)
                    .clipShape(RoundedRectangle(cornerRadius: 16))
                
                // Place suggestions
                if !message.places.isEmpty {
                    ForEach(message.places) { place in
                        NavigationLink {
                            PlaceDetailView(place: place)
                        } label: {
                            PlaceListRow(place: place)
                        }
                        .buttonStyle(.plain)
                    }
                }
            }
            
            if !message.isUser { Spacer(minLength: 60) }
        }
    }
}
