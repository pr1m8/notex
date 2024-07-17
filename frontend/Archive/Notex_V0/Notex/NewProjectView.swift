import SwiftUI

struct NewProjectView: View {
    @Binding var projects: [Project]
    @State private var isDocumentPickerPresented = false
    @State private var selectedDocument: URL?
    @State private var projectName: String = ""
    @State private var isUploading = false
    @State private var uploadSuccess = false

    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        VStack {
            TextField("Project Name", text: $projectName)
                .padding()
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding(.horizontal, 20)

            Button("Select Document") {
                isDocumentPickerPresented.toggle()
            }
            .padding()
            .background(Color.gray)
            .cornerRadius(10)
            .padding(.horizontal, 20)

            if let selectedDocument = selectedDocument {
                Text("Selected Document: \(selectedDocument.lastPathComponent)")
                    .padding()
                    .background(Color.gray.opacity(0.2))
                    .cornerRadius(10)
                    .padding(.horizontal, 20)
                    .padding(.top, 10)
            }

            if isUploading {
                ProgressView("Uploading...")
                    .padding()
            } else if uploadSuccess {
                Button("Enter") {
                    let newProject = Project(id: projects.count + 1, name: projectName, pdf_path: "uploaded.pdf", latex_path: "uploaded.tex", created_at: "")
                    projects.append(newProject)
                    presentationMode.wrappedValue.dismiss()
                }
                .padding()
                .background(Color.gray)
                .cornerRadius(10)
            } else {
                Button("Upload") {
                    uploadFile()
                }
                .padding()
                .background(Color.gray)
                .cornerRadius(10)
                .padding(.horizontal, 20)
                .padding(.top, 20)
            }
        }
        .sheet(isPresented: $isDocumentPickerPresented) {
            DocumentPicker(selectedDocument: self.$selectedDocument)
        }
        .navigationTitle("New Project")
    }

    func uploadFile() {
        guard let selectedDocument = selectedDocument else { return }

        isUploading = true
        NetworkManager.shared.uploadFile(fileURL: selectedDocument) { result in
            DispatchQueue.main.async {
                isUploading = false
                switch result {
                case .success(_):
                    self.uploadSuccess = true
                case .failure(let error):
                    print("Failed to upload file: \(error.localizedDescription)")
                }
            }
        }
    }
}

struct NewProjectView_Previews: PreviewProvider {
    static var previews: some View {
        NewProjectView(projects: .constant([]))
    }
}

