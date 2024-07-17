import SwiftUI
import PDFKit

struct DocumentDetailView: View {
    var document: Document?

    @StateObject private var viewModel = DocumentViewModel()

    var body: some View {
        VStack {
            if viewModel.isLoading {
                ProgressView("Loading...").padding()
            } else {
                if let url = viewModel.selectedDocumentURL {
                    PDFViewer(url: url)
                } else {
                    Text("No document selected")
                }
            }

            Spacer()

            HStack {
                Button(action: {
                    viewModel.testDownloadPDF { result in
                        switch result {
                        case .success(let url):
                            viewModel.selectedDocumentURL = url
                        case .failure(let error):
                            print("Download error: \(error.localizedDescription)")
                        }
                    }
                }) {
                    Text("Download Test PDF")
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }

                Button(action: {
                    if let document = document {
                        viewModel.downloadDocument(document) { result in
                            switch result {
                            case .success(let localURL):
                                viewModel.selectedDocumentURL = localURL
                                print("Downloaded to: \(localURL)")
                            case .failure(let error):
                                print("Download error: \(error.localizedDescription)")
                            }
                        }
                    }
                }) {
                    Text("Download Document")
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
            }
            .padding()
        }
        .onAppear {
            if let document = document {
                viewModel.selectedDocumentURL = document.url
            }
        }
        .navigationTitle("Document Details")
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct DocumentDetailView_Previews: PreviewProvider {
    static var previews: some View {
        DocumentDetailView(document: Document(id: UUID().uuidString, name: "Sample Document", url: URL(string: "https://example.com/sample.pdf")!))
    }
}

