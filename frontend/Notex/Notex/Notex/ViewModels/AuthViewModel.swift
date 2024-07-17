import SwiftUI
import GoogleSignIn
import FirebaseAuth

class AuthViewModel: ObservableObject {
    @Published var firebaseUser: FirebaseAuth.User?
    
    init() {
        checkCurrentUser()
    }
    
    func checkCurrentUser() {
        self.firebaseUser = Auth.auth().currentUser
    }
    
    func signInWithGoogle(presentingViewController: UIViewController) {
        AuthService.shared.signInWithGoogle(presentingViewController: presentingViewController) { [weak self] result in
            switch result {
            case .success(let user):
                guard let idToken = user.idToken?.tokenString else { return }
                let accessToken = user.accessToken.tokenString
                
                let credential = GoogleAuthProvider.credential(withIDToken: idToken, accessToken: accessToken)
                
                Auth.auth().signIn(with: credential) { authResult, error in
                    if let error = error {
                        print("Firebase sign-in error: \(error.localizedDescription)")
                        return
                    }
                    self?.firebaseUser = Auth.auth().currentUser
                }
            case .failure(let error):
                print("Google sign-in error: \(error.localizedDescription)")
            }
        }
    }
    
    func signOut() {
        do {
            try Auth.auth().signOut()
            try AuthService.shared.signOut()
            self.firebaseUser = nil
        } catch {
            print("Error signing out: \(error.localizedDescription)")
        }
    }
}

