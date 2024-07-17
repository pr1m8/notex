import SwiftUI

struct NewProjectView: View {
    @Binding var projects: [Project]
    @State private var projectName: String = ""
    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        VStack {
            TextField("Project Name", text: $projectName)
                .padding()
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding(.horizontal, 20)

            Button("Create Project") {
                let newProject = Project(id: projects.count + 1, name: projectName, pdf_path: "", latex_path: "", created_at: "")
                projects.append(newProject)
                presentationMode.wrappedValue.dismiss()
            }
            .padding()
            .background(Color.gray)
            .cornerRadius(10)
        }
        .navigationTitle("New Project")
    }
}

struct NewProjectView_Previews: PreviewProvider {
    static var previews: some View {
        NewProjectView(projects: .constant([]))
    }
}

