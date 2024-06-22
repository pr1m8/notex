import SwiftUI

struct ProjectsListView: View {
    @State private var projects = [Project]()
    @State private var showNewProjectView = false

    var body: some View {
        NavigationView {
            VStack {
                List(projects) { project in
                    NavigationLink(destination: ProjectDetailView(project: project, onPDFDownload: { url in
                        // Handle PDF download
                    }, onLaTeXDownload: { data in
                        // Handle LaTeX download
                    })) {
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
                    NewProjectView()
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

struct ProjectsListView_Previews: PreviewProvider {
    static var previews: some View {
        ProjectsListView()
    }
}

