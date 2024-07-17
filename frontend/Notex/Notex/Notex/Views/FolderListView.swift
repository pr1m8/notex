import SwiftUI



struct FolderListView: View {
    @Binding var selectedFolder: Folder?
    @State private var folders: [Folder] = [
        Folder(id: UUID(), name: "Folder 1"),
        Folder(id: UUID(), name: "Folder 2"),
        Folder(id: UUID(), name: "Folder 3")
    ]

    var body: some View {
        List(folders) { folder in
            Text(folder.name)
                .onTapGesture {
                    selectedFolder = folder
                }
        }
        .navigationTitle("Folders")
    }
}

