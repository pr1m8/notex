import Foundation

struct Project: Identifiable, Decodable {
    var id: Int
    var name: String
    var pdf_path: String
    var latex_path: String
    var created_at: String
}

