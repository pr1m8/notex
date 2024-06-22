import Foundation

class NetworkManager {
    static let shared = NetworkManager()

    private let baseURL = "http://127.0.0.1:5001"

    private init() {}

    func uploadFile(fileURL: URL, completion: @escaping (Result<String, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/upload")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.timeoutInterval = 120000

        let boundary = UUID().uuidString
        let contentType = "multipart/form-data; boundary=\(boundary)"
        request.setValue(contentType, forHTTPHeaderField: "Content-Type")

        var body = Data()

        // File data
        if let fileData = try? Data(contentsOf: fileURL) {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(fileURL.lastPathComponent)\"\r\n".data(using: .utf8)!)
            body.append("Content-Type: application/pdf\r\n\r\n".data(using: .utf8)!)
            body.append(fileData)
            body.append("\r\n".data(using: .utf8)!)
        }

        // End boundary
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200,
                  let responseData = data,
                  let json = try? JSONSerialization.jsonObject(with: responseData, options: []) as? [String: Any],
                  let path = json["path"] as? String else {
                completion(.failure(NetworkError.invalidResponse))
                return
            }

            completion(.success(path))
        }

        task.resume()
    }

    func compileLatexCode(latexCode: String, completion: @escaping (Result<Data, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/compile_text")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.timeoutInterval = 120000
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let parameters = ["latex": latexCode]
        request.httpBody = try? JSONSerialization.data(withJSONObject: parameters, options: [])

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
                completion(.failure(NetworkError.invalidResponse))
                return
            }

            if let data = data {
                completion(.success(data))
            } else {
                completion(.failure(NetworkError.noData))
            }
        }

        task.resume()
    }

    func downloadFile(from endpoint: String, completion: @escaping (Result<Data, Error>) -> Void) {
        let url = URL(string: "\(baseURL)\(endpoint)")!
        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
                completion(.failure(NetworkError.invalidResponse))
                return
            }

            if let data = data {
                completion(.success(data))
            } else {
                completion(.failure(NetworkError.noData))
            }
        }

        task.resume()
    }
}

enum NetworkError: Error {
    case invalidResponse
    case noData
}

