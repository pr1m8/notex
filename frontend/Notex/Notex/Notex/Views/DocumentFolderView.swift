import SwiftUI

struct DocumentFolderView: View {
    @StateObject private var viewModel = DocumentViewModel()
    @State private var showDocumentPicker = false
    var project: Project
    var onDocumentSelected: (Document) -> Void

    var body: some View {
        VStack {
            if viewModel.isLoading {
                ProgressView("Loading...").padding()
            } else {
                List(viewModel.documents) { document in
                    HStack {
                        Text(document.name)
                        Spacer()
                        Button(action: {
                            onDocumentSelected(document)
                        }) {
                            Image(systemName: "arrow.right.circle").padding()
                        }
                        .buttonStyle(BorderlessButtonStyle())
                    }
                }
                .listStyle(PlainListStyle())
                .onAppear {
                    viewModel.fetchDocuments(in: project)
                }
            }

            if let errorMessage = viewModel.errorMessage {
                Text(errorMessage).foregroundColor(.red).padding()
            }
        }
        .navigationTitle("Documents")
        .navigationBarItems(trailing: Button(action: {
            showDocumentPicker = true
        }) {
            Image(systemName: "plus")
        })
        .sheet(isPresented: $showDocumentPicker) {
            DocumentPicker { url in
                if let url = url {
                    viewModel.uploadDocument(url, to: project)
                }
            }
        }
    }
}

struct DocumentFolderView_Previews: PreviewProvider {
    static var previews: some View {
        DocumentFolderView(project: Project(id: 1, name: "Sample Project", pdf_path: "", latex_path: "", created_at: "")) { _ in }
    }
}

