import SwiftUI

struct FilePicker: UIViewControllerRepresentable {
    @Binding var selectedFile: URL?

    class Coordinator: NSObject, UIDocumentPickerDelegate {
        var parent: FilePicker

        init(parent: FilePicker) {
            self.parent = parent
        }

        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            parent.selectedFile = urls.first
        }

        func documentPickerWasCancelled(_ controller: UIDocumentPickerViewController) {
            parent.selectedFile = nil
        }
    }

    func makeCoordinator() -> Coordinator {
        return Coordinator(parent: self)
    }

    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: [.pdf, .image])
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}
}

struct FilePicker_Previews: PreviewProvider {
    static var previews: some View {
        FilePicker(selectedFile: .constant(nil))
    }
}

