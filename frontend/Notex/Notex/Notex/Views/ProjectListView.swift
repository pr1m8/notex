import SwiftUI

struct ProjectListView: View {
    @State private var projects = [Project]()
    @State private var showNewProjectView = false
    var onDocumentSelected: (Document) -> Void

    var body: some View {
        NavigationView {
            VStack {
                List(projects) { project in
                    NavigationLink(destination: ProjectDetailView(project: project, onDocumentSelected: onDocumentSelected)) {
                        Text(project.name)
                    }
                }
                .onAppear(perform: loadProjects)
                .navigationTitle("Projects")

                Button(action: {
                    showNewProjectView = true
                }) {
                    Text("New Project")
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding()
                .sheet(isPresented: $showNewProjectView) {
                    NewProjectView(projects: $projects)
                }
            }
        }
    }

    func loadProjects() {
        // Load projects from local storage or API
        // Example placeholder:
        self.projects = [
            Project(id: 1, name: "Sample Project", pdf_path: "sample.pdf", latex_path: "sample.tex", created_at: "")
        ]
    }
}

struct ProjectListView_Previews: PreviewProvider {
    static var previews: some View {
        ProjectListView { _ in }
    }
}

