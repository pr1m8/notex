import SwiftUI

struct ProjectDetailView: View {
    let project: Project

    var body: some View {
        VStack {
            Text("Project Detail View for \(project.name)")
                .font(.title)

            Button(action: {
                downloadPDF()
            }) {
                Text("Download PDF")
            }
            .padding()

            Button(action: {
                downloadLaTeX()
            }) {
                Text("Download LaTeX")
            }
            .padding()

            Spacer()
        }
        .padding()
        .navigationTitle(project.name)
    }

    private func downloadPDF() {
        NetworkManager.shared.downloadPDF(from: "/api/download_pdf?id=\(project.id)") { result in
            switch result {
            case .success(let url):
                // Handle PDF download (e.g., open it, save it, etc.)
                print("PDF downloaded at: \(url)")
            case .failure(let error):
                print("Failed to download PDF: \(error)")
            }
        }
    }

    private func downloadLaTeX() {
        NetworkManager.shared.downloadLaTeX(from: "/api/download_tex?id=\(project.id)") { result in
            switch result {
            case .success(let data):
                if let latexString = String(data: data, encoding: .utf8) {
                    // Handle LaTeX download (e.g., open it, save it, etc.)
                    print("LaTeX downloaded: \(latexString)")
                } else {
                    print("Failed to convert LaTeX data to string")
                }
            case .failure(let error):
                print("Failed to download LaTeX: \(error)")
            }
        }
    }
}

struct ProjectDetailView_Previews: PreviewProvider {
    static var previews: some View {
        ProjectDetailView(project: Project(id: 1, name: "Sample Project", pdf_path: "sample.pdf", latex_path: "sample.tex", created_at: ""))
    }
}


