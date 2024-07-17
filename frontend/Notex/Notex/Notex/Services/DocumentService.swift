// Need to remove - outdated.

import Foundation
import UniformTypeIdentifiers

class DocumentService {
    static let shared = DocumentService()
    private let baseURL = "http://127.0.0.1:5001"  // Replace with your actual backend URL

    private init() {}

    func uploadDocument(_ file: URL, completion: @escaping (Result<String, Error>) -> Void) {
        let uploadURL = URL(string: "\(baseURL)/upload")!
        var request = URLRequest(url: uploadURL)
        request.httpMethod = "POST"

        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()

        // Add the file data
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(file.lastPathComponent)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: \(file.mimeType)\r\n\r\n".data(using: .utf8)!)
        body.append(try! Data(contentsOf: file))
        body.append("\r\n".data(using: .utf8)!)

        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "DocumentService", code: -1, userInfo: [NSLocalizedDescriptionKey: "No data received"])))
                return
            }

            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
                   let projectId = json["project_id"] as? String,
                   let pdfPath = json["pdf_path"] as? String {
                    completion(.success(projectId))
                } else {
                    completion(.failure(NSError(domain: "DocumentService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid server response"])))
                }
            } catch {
                completion(.failure(error))
            }
        }

        task.resume()
    }

    func downloadPDF(projectId: String, completion: @escaping (Result<URL, Error>) -> Void) {
        let downloadURL = URL(string: "\(baseURL)/api/download_pdf?project_id=\(projectId)")!
        
        let task = URLSession.shared.downloadTask(with: downloadURL) { localURL, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let localURL = localURL else {
                completion(.failure(NSError(domain: "DocumentService", code: -1, userInfo: [NSLocalizedDescriptionKey: "No file received"])))
                return
            }
            
            let documentsURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            let destinationURL = documentsURL.appendingPathComponent("downloaded_pdf_\(projectId).pdf")
            
            do {
                if FileManager.default.fileExists(atPath: destinationURL.path) {
                    try FileManager.default.removeItem(at: destinationURL)
                }
                try FileManager.default.moveItem(at: localURL, to: destinationURL)
                completion(.success(destinationURL))
            } catch {
                completion(.failure(error))
            }
        }
        
        task.resume()
    }
}

extension URL {
    var mimeType: String {
        let pathExtension = self.pathExtension
        if let utType = UTType(filenameExtension: pathExtension) {
            return utType.preferredMIMEType ?? "application/octet-stream"
        }
        return "application/octet-stream"
    }
}

