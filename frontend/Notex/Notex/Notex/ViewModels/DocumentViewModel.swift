import Foundation
import FirebaseStorage
import FirebaseAuth

class DocumentViewModel: ObservableObject {
    @Published var documents: [Document] = []
    @Published var errorMessage: String?
    @Published var isLoading: Bool = false
    @Published var selectedDocumentURL: URL?

    private let storage = Storage.storage()

    func uploadDocument(_ file: URL, to project: Project) {
        guard let user = Auth.auth().currentUser else {
            self.errorMessage = "User is not logged in."
            return
        }

        isLoading = true

        NetworkManager.shared.uploadFile(fileURL: file, to: project) { result in
            DispatchQueue.main.async {
                self.isLoading = false
                switch result {
                case .success(let path):
                    let document = Document(id: UUID().uuidString, name: file.lastPathComponent, url: URL(string: path)!)
                    self.documents.append(document)
                    self.selectedDocumentURL = URL(string: path)
                case .failure(let error):
                    self.errorMessage = "Upload error: \(error.localizedDescription)"
                }
            }
        }
    }

    func fetchDocuments(in project: Project) {
        isLoading = true

        // Mock fetching documents from the project for demo purposes
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            self.isLoading = false
            self.documents = [
                Document(id: UUID().uuidString, name: "Sample Document 1", url: URL(string: "https://example.com/sample1.pdf")!),
                Document(id: UUID().uuidString, name: "Sample Document 2", url: URL(string: "https://example.com/sample2.pdf")!)
            ]
        }
    }
}

