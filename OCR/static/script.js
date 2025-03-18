function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("Please select a file first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById("extractedText").value = data.text;
            
            let uploadedImage = document.getElementById("uploadedImage");
            uploadedImage.src = data.image_url;
            uploadedImage.style.display = "block"; 
        }
    })
    .catch(error => console.error("Error:", error));
}

function downloadFile(fileType) {
    let text = document.getElementById("extractedText").value;

    let formData = new FormData();
    formData.append("text", text);

    fetch(`/download/${fileType}`, {
        method: "POST",
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        let link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `extracted_text.${fileType}`;
        link.click();
    })
    .catch(error => console.error("Error:", error));
}
