import Foundation
import GoogleSignIn
import Firebase

class AuthService {
    static let shared = AuthService()
    
    private init() {}

    func signInWithGoogle(presentingViewController: UIViewController, completion: @escaping (Result<GIDGoogleUser, Error>) -> Void) {
        guard let clientID = FirebaseApp.app()?.options.clientID else {
            completion(.failure(NSError(domain: "AuthService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Google client ID is missing."])))
            return
        }

        let config = GIDConfiguration(clientID: clientID)
        GIDSignIn.sharedInstance.configuration = config

        GIDSignIn.sharedInstance.signIn(withPresenting: presentingViewController) { result, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            guard let user = result?.user else {
                completion(.failure(NSError(domain: "AuthService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Google Sign-In user is missing."])))
                return
            }
            completion(.success(user))
        }
    }

    func signOut() throws {
        try GIDSignIn.sharedInstance.signOut()
    }

    func currentUser() -> GIDGoogleUser? {
        return GIDSignIn.sharedInstance.currentUser
    }
}
