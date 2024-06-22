import SwiftUI
import PDFKit

enum ViewType {
    case pdf
    case tex
}

struct NewProjectView: View {
    @State private var isDocumentPickerPresented = false
    @State private var selectedDocument: URL?
    @State private var projectName: String = ""
    @State private var isUploading = false
    @State private var uploadSuccess = false
    @State private var texFileURL: URL?
    @State private var pdfFileURL: URL?
    @State private var selectedView: ViewType = .pdf

    var body: some View {
        VStack {
            Image(systemName: "n.circle.fill")
                .resizable()
                .frame(width: 100, height: 100)
                .foregroundColor(.white)
                .padding(.bottom, 40)

            TextField("Project Name", text: $projectName)
                .padding()
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .background(Color("SoftWhite").opacity(0.8))
                .cornerRadius(10)
                .padding(.horizontal, 20)

            Button("Select Document") {
                isDocumentPickerPresented.toggle()
            }
            .padding()
            .background(Color("Teal"))
            .foregroundColor(Color("DarkTeal"))
            .cornerRadius(10)
            .padding(.horizontal, 20)

            if let selectedDocument = selectedDocument {
                Text("Selected Document: \(selectedDocument.lastPathComponent)")
                    .padding()
                    .foregroundColor(.white)
                    .background(Color.white.opacity(0.2))
                    .cornerRadius(10)
                    .padding(.horizontal, 20)
                    .padding(.top, 10)
            }

            if isUploading {
                ProgressView("Uploading...")
                    .padding()
            } else if uploadSuccess {
                Picker("", selection: $selectedView) {
                    Text("PDF").tag(ViewType.pdf)
                    Text("LaTeX").tag(ViewType.tex)
                }
                .pickerStyle(SegmentedPickerStyle())
                .padding()

                if selectedView == .pdf, let pdfURL = pdfFileURL {
                    PDFViewer(url: pdfURL)
                } else if selectedView == .tex, let texURL = texFileURL {
                    TexView(url: texURL)
                }
            } else {
                Button("Upload") {
                    uploadFile()
                }
                .padding()
                .background(Color.white)
                .foregroundColor(Color("DarkTeal"))
                .cornerRadius(10)
                .padding(.horizontal, 20)
                .padding(.top, 20)
            }
        }
        .background(Color("Teal"))
        .edgesIgnoringSafeArea(.all)
        .navigationTitle("New Project")
        .sheet(isPresented: $isDocumentPickerPresented) {
            DocumentPicker(selectedDocument: self.$selectedDocument)
        }
    }

    func uploadFile() {
        guard let selectedDocument = selectedDocument else { return }

        isUploading = true
        NetworkManager.shared.uploadFile(fileURL: selectedDocument) { result in
            DispatchQueue.main.async {
                isUploading = false
                switch result {
                case .success(let folderPath):
                    self.uploadSuccess = true
                    self.texFileURL = URL(string: "\(folderPath)/output.tex")
                    self.pdfFileURL = URL(string: "\(folderPath)/output.pdf")
                case .failure(let error):
                    print("Failed to upload file: \(error.localizedDescription)")
                }
            }
        }
    }
}

struct NewProjectView_Previews: PreviewProvider {
    static var previews: some View {
        NewProjectView()
    }
}

