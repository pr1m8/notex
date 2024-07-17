import SwiftUI

struct LoginView: View {
    @EnvironmentObject var authViewModel: AuthViewModel

    var body: some View {
        VStack {
            Button("Sign In with Google") {
                if let rootViewController = UIApplication.shared.windows.first?.rootViewController {
                    authViewModel.signInWithGoogle(presentingViewController: rootViewController)
                }
            }
        }
    }
}
