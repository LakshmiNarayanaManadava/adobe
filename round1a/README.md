# Adobe Hackathon Round 1A – Understand Your Document
## 📌 Approach
Uses PyMuPDF to extract Title & Headings (H1, H2, H3) with page numbers.
## 🚀 Build & Run
```bash
docker build --platform linux/amd64 -t mysolution:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolution:latest
```
