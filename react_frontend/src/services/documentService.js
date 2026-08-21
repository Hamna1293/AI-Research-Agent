const API = "http://127.0.0.1:8000";

export async function uploadDocument(file) {

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(`${API}/upload`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Upload failed");
    }

    return await response.json();
}

export async function getDocuments() {

    const response = await fetch(`${API}/documents`);

    if (!response.ok) {
        throw new Error("Unable to fetch documents");
    }

    return await response.json();
}

export async function deleteDocument(filename) {

    const response = await fetch(

        `${API}/documents/${filename}`,

        {
            method: "DELETE",
        }

    );

    if (!response.ok) {
        throw new Error("Delete failed");
    }

    return await response.json();
}

export async function getReport(filename) {

    const response = await fetch(

        `${API}/report/${filename}`

    );

    if (!response.ok) {

        throw new Error("Unable to load report");

    }

    return await response.json();

}

export async function getInsights(filename) {

    const response = await fetch(
        `${API}/insights/${encodeURIComponent(filename)}`
    );

    if (!response.ok) {
        throw new Error("Unable to load insights");
    }

    return await response.json();
}