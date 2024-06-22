import SwiftUI

struct ProjectDetailView: View {
    var project: Project

    var body: some View {
        VStack {
            Text(project.name)
                .font(.largeTitle)
                .padding()

            if let url = URL(string: project.pdf_path) {
                PDFViewer(url: url)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                Text("Invalid PDF URL")
                    .foregroundColor(.red)
            }
        }
        .navigationTitle("Project Details")
    }
}

struct ProjectDetailView_Previews: PreviewProvider {
    static var previews: some View {
        ProjectDetailView(project: Project(id: 1, name: "Sample Project", pdf_path: "https://example.com/sample.pdf", latex_path: "", created_at: ""))
    }
}

