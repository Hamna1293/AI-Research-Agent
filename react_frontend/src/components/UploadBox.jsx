import { useState } from "react";
import api from "../api/axios";


function UploadBox() {

    const [file, setFile] = useState(null);
    const [status, setStatus] = useState("");
    const [result, setResult] = useState(null);


    const handleUpload = async () => {

        if (!file) {

            setStatus(
                "Please select a file first."
            );

            return;
        }


        const formData = new FormData();

        formData.append(
            "file",
            file
        );


        try {

            setStatus(
                "Uploading and processing..."
            );


            const response = await api.post(
                "/upload",
                formData
            );


            setResult(
                response.data
            );


            setStatus(
                "Upload successful."
            );


        } catch(error) {

            console.error(
                error
            );


            setStatus(
                "Upload failed."
            );

        }

    };


    return (

        <div className="upload-box">

            <h2>
                Upload Research Paper
            </h2>


            <input

                type="file"

                onChange={(event)=>{

                    setFile(
                        event.target.files[0]
                    );

                }}

            />


            <button
                onClick={handleUpload}
            >
                Upload
            </button>


            <p>
                {status}
            </p>



            {
                result && (

                    <div>

                        <h3>
                            Document Information
                        </h3>


                        <p>
                            Filename:
                            {" "}
                            {result.filename}
                        </p>


                        <p>
                            Pages:
                            {" "}
                            {result.pages}
                        </p>


                        <p>
                            Chunks:
                            {" "}
                            {result.chunks}
                        </p>


                    </div>

                )
            }


        </div>

    );

}


export default UploadBox;