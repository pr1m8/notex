import SwiftUI
import UniformTypeIdentifiers

struct AddProjectView: View {
    @Environment(\.presentationMode) var presentationMode
    @Binding var projects: [Project]
    @State private var projectName = ""
    @State private var selectedPDF: URL?

    var body: some View {
        NavigationView {
            Form {
                Section {
                    TextField("Project Name", text: $projectName)
                }

                Section {
                    Button("Select PDF") {
                        selectPDF()
                    }
                    if selectedPDF != nil {
                        Text("PDF Selected")
                    }
                }

                Section {
                    Button("Add Project") {
                        if let pdfURL = selectedPDF {
                            let project = Project(name: projectName, pdfURL: pdfURL, texURL: URL(fileURLWithPath: ""))
                            projects.append(project)
                            uploadPDF(pdfURL: pdfURL, project: project)
                        }
                        presentationMode.wrappedValue.dismiss()
                    }
                }
            }
            .navigationBarTitle("New Project")
        }
    }

    func selectPDF() {
        let documentPicker = UIDocumentPickerViewController(forOpeningContentTypes: [UTType.pdf])
        documentPicker.delegate = self
        UIApplication.shared.windows.first?.rootViewController?.present(documentPicker, animated: true, completion: nil)
    }

    func uploadPDF(pdfURL: URL, project: Project) {
        // Handle the upload logic here
        // This should communicate with your backend to upload the PDF and get the .tex file
    }
}

extension AddProjectView: UIDocumentPickerDelegate {
    func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
        selectedPDF = urls.first
    }
}

