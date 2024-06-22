import SwiftUI

struct MainMenuView: View {
    var body: some View {
        VStack {
            NavigationLink(destination: ProjectsListView()) {
                Text("View Projects")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
            NavigationLink(destination: NewProjectView()) {
                Text("New Project")
                    .padding()
                    .background(Color.green)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
        }
        .navigationTitle("Notex")
    }
}

struct MainMenuView_Previews: PreviewProvider {
    static var previews: some View {
        MainMenuView()
    }
}

