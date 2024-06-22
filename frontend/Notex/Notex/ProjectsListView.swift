import SwiftUI

struct ProjectsListView: View {
    @State private var projects = [Project]()
    @State private var showPDF = false
    @State private var showLaTeX = false
    @State private var pdfData: Data? = nil
    @State private var latexData: String? = nil

    var body: some View {
        NavigationView {
            VStack {
                List(projects) { project in
                    NavigationLink(destination: ProjectDetailView(project: project)) {
                        Text(project.name)
                    }
                }
                .onAppear(perform: loadProjects)
                .navigationTitle("Projects")

                Button(action: downloadPDF) {
                    Text("Download PDF")
                }
                .padding()
                
                Button(action: downloadLaTeX) {
                    Text("Download LaTeX")
                }
                .padding()
                
                if showPDF, let data = pdfData {
                    PDFViewer(url: data)
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                }

                if showLaTeX, let data = latexData {
                    Text(data)
                        .padding()
                }
            }
        }
    }

    func loadProjects() {
        // Load projects from local storage
        // This is just a placeholder to simulate loading projects.
        // Replace this with your actual implementation to load projects.
        self.projects = [
            Project(id: 1, name: "Sample Project", pdf_path: "sample.pdf", latex_path: "sample.tex", created_at: "")
        ]
    }

    func downloadPDF() {
        NetworkManager.shared.downloadFile(from: "/api/download_pdf") { result in
            switch result {
            case .success(let data):
                self.pdfData = data
                self.showPDF = true
            case .failure(let error):
                print("Failed to download PDF: \(error)")
            }
        }
    }

    func downloadLaTeX() {
        NetworkManager.shared.downloadFile(from: "/api/download_tex") { result in
            switch result {
            case .success(let data):
                self.latexData = String(data: data, encoding: .utf8)
                self.showLaTeX = true
            case .failure(let error):
                print("Failed to download LaTeX: \(error)")
            }
        }
    }
}

struct ProjectsListView_Previews: PreviewProvider {
    static var previews: some View {
        ProjectsListView()
    }
}

