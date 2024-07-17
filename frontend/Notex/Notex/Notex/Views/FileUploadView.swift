import SwiftUI

struct FileUploadView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @StateObject var documentViewModel = DocumentViewModel()
    @State private var selectedFile: URL?
    @State private var showingFilePicker = false
    var project: Project
    var onDocumentSelected: (Document) -> Void

    var body: some View {
        VStack {
            Button("Select File") {
                showingFilePicker.toggle()
            }
            .sheet(isPresented: $showingFilePicker) {
                DocumentPicker { url in
                    if let url = url {
                        selectedFile = url
                    }
                }
            }
            
            if let file = selectedFile {
                Text("Selected file: \(file.lastPathComponent)")
                Button("Upload File") {
                    documentViewModel.uploadDocument(file, to: project)
                }
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(10)
            }

            if documentViewModel.isLoading {
                ProgressView("Uploading...")
                    .padding()
            }

            if let errorMessage = documentViewModel.errorMessage {
                Text(errorMessage)
                    .foregroundColor(.red)
                    .padding()
            }

            if let url = documentViewModel.selectedDocumentURL {
                Button("View Document") {
                    onDocumentSelected(Document(id: UUID().uuidString, name: selectedFile?.lastPathComponent ?? "", url: url))
                }
                .padding()
                .background(Color.green)
                .foregroundColor(.white)
                .cornerRadius(10)
            }
        }
    }
}

struct FileUploadView_Previews: PreviewProvider {
    static var previews: some View {
        FileUploadView(project: Project(id: 1, name: "Sample Project", pdf_path: "", latex_path: "", created_at: "")) { _ in }
            .environmentObject(AuthViewModel())
    }
}

