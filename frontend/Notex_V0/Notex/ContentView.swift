import SwiftUI

struct ContentView: View {
    @State private var projects: [Project] = []
    @State private var showingAddProject = false

    var body: some View {
        NavigationView {
            List(projects) { project in
                NavigationLink(destination: ProjectDetailView(project: project)) {
                    Text(project.name)
                }
            }
            .navigationBarTitle("Notex")
            .navigationBarItems(trailing: Button(action: {
                self.showingAddProject.toggle()
            }) {
                Image(systemName: "plus")
            })
            .sheet(isPresented: $showingAddProject) {
                AddProjectView(projects: self.$projects)
            }
        }
    }
}

struct Project: Identifiable {
    var id = UUID()
    var name: String
    var pdfURL: URL
    var texURL: URL
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

