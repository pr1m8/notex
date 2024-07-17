import SwiftUI

struct TexView: View {
    var url: URL

    var body: some View {
        ScrollView {
            if let content = try? String(contentsOf: url) {
                Text(content)
                    .padding()
                    .background(Color.white)
                    .cornerRadius(10)
                    .padding()
            } else {
                Text("Failed to load content")
                    .padding()
            }
        }
    }
}

