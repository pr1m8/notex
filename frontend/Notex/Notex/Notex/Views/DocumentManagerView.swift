import SwiftUI

struct DocumentManagerView: View {
    @State private var selectedFolder: Folder?
    @StateObject private var viewModel = DocumentViewModel()
    @State private var showDocumentPicker = false

    var body: some View {
        NavigationView {
            VStack {
                HStack {
                    FolderListView(selectedFolder: $selectedFolder)
                    Divider()
                    VStack {
                        HStack {
                            Text("Document Manager")
                                .font(.largeTitle)
                                .padding()
                            Spacer()
                        }

                        if viewModel.isLoading {
                            ProgressView("Loading...")
                                .padding()
                        } else {
                            if let url = viewModel.selectedDocumentURL {
                                PDFViewWrapper(url: url)
                            } else {
                                Text("No document selected")
                            }
                        }

                        Spacer()

                        HStack {
                            Button(action: {
                                showDocumentPicker = true
                            }) {
                                Text("Upload Document")
                                    .padding()
                                    .background(Color.blue)
                                    .foregroundColor(.white)
                                    .cornerRadius(10)
                            }

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
                        }
                        .padding()
                    }
                    .padding()
                }
                .navigationTitle("Document Manager")
            }
            .sheet(isPresented: $showDocumentPicker) {
                DocumentPicker { url in
                    if let url = url, let folder = selectedFolder {
                        viewModel.uploadDocument(url, to: folder)
                    } else {
                        // Handle the case where there is no selected folder
                        print("No folder selected for upload")
                    }
                }
            }
        }
    }
}

struct DocumentManagerView_Previews: PreviewProvider {
    static var previews: some View {
        DocumentManagerView()
    }
}

