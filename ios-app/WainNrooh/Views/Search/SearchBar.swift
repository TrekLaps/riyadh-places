// SearchBar.swift
// شريط البحث المخصص — يدعم العربي RTL

import SwiftUI

// MARK: - شريط البحث

/// شريط بحث مخصص مع دعم العربي
struct SearchBar: View {
    @Binding var text: String
    var isFocused: FocusState<Bool>.Binding
    var placeholder: String = "ابحث عن مكان، مطعم، كافيه..."
    var onSubmit: (() -> Void)?
    var onClear: (() -> Void)?
    
    var body: some View {
        HStack(spacing: Theme.spacingSmall) {
            // زر المسح
            if !text.isEmpty {
                Button {
                    text = ""
                    onClear?()
                } label: {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundStyle(Color.appTextSecondary)
                        .font(.system(size: 18))
                }
            }
            
            // حقل النص
            TextField(placeholder, text: $text)
                .font(Theme.bodyFont(size: 16))
                .foregroundStyle(Color.appTextPrimary)
                .multilineTextAlignment(.trailing)
                .textInputAutocapitalization(.never)
                .autocorrectionDisabled()
                .focused(isFocused)
                .submitLabel(.search)
                .onSubmit {
                    onSubmit?()
                }
            
            // أيقونة البحث
            Image(systemName: "magnifyingglass")
                .foregroundStyle(Theme.primary)
                .font(.system(size: 18, weight: .medium))
        }
        .padding(.horizontal, Theme.paddingMedium)
        .padding(.vertical, Theme.paddingSmall + 4)
        .background(Color.appSecondaryBackground)
        .clipShape(RoundedRectangle(cornerRadius: Theme.cornerRadiusLarge))
        .overlay(
            RoundedRectangle(cornerRadius: Theme.cornerRadiusLarge)
                .stroke(
                    isFocused.wrappedValue ? Theme.primary.opacity(0.5) : Color.clear,
                    lineWidth: 1.5
                )
        )
        .animation(Theme.animationFast, value: isFocused.wrappedValue)
    }
}

// MARK: - Preview

#Preview {
    @FocusState var focused: Bool
    
    VStack(spacing: 16) {
        SearchBar(
            text: .constant(""),
            isFocused: $focused
        )
        
        SearchBar(
            text: .constant("قهوة مختصة"),
            isFocused: $focused
        )
    }
    .padding()
    .background(Color.appBackground)
}
