import SwiftUI

struct ContentView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var selectedDocument: Document?

    var body: some View {
        NavigationView {
            if authViewModel.firebaseUser != nil {
                ProjectListView(onDocumentSelected: { document in
                    selectedDocument = document
                })
                .navigationTitle("Projects")
                .navigationBarItems(trailing: Button(action: {
                    authViewModel.signOut()
                }) {
                    Text("Sign Out")
                })
                NavigationLink(destination: DocumentDetailView(document: selectedDocument), isActive: .constant(selectedDocument != nil)) {
                    EmptyView()
                }
            } else {
                LoginView()
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView().environmentObject(AuthViewModel())
    }
}

