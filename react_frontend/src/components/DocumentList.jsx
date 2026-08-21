import { useEffect, useState } from "react";
import api from "../api/axios";


function DocumentList() {


    const [documents, setDocuments] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");



    useEffect(() => {


        let mounted = true;



        const loadDocuments = async () => {


            try {


                setLoading(true);

                setError("");



                const response = await api.get(
                    "/documents"
                );



                console.log(
                    "API Documents:",
                    response.data
                );



                if (!mounted) return;



                if (Array.isArray(response.data)) {


                    setDocuments(
                        response.data
                    );


                } else {


                    setDocuments([]);


                    setError(
                        "Invalid document response from server."
                    );


                }



            } catch (err) {


                console.error(
                    "Document fetch error:",
                    err
                );


                if (mounted) {

                    setError(
                        "Unable to load documents."
                    );

                }



            } finally {


                if (mounted) {

                    setLoading(false);

                }


            }


        };



        loadDocuments();



        return () => {

            mounted = false;

        };


    }, []);





    const handleDelete = async (filename) => {


        try {


            await api.delete(
                `/documents/${filename}`
            );



            // reload documents after deletion

            const response = await api.get(
                "/documents"
            );



            if (Array.isArray(response.data)) {


                setDocuments(
                    response.data
                );


            }



        } catch (err) {


            console.error(
                "Delete error:",
                err
            );


            setError(
                "Unable to delete document."
            );


        }


    };





    if (loading) {


        return (

            <div>

                <h2>
                    Uploaded Documents
                </h2>


                <p>
                    Loading...
                </p>


            </div>

        );

    }




    return (

        <div className="documents">


            <h2>
                Uploaded Documents
            </h2>



            {
                error && (

                    <p>
                        {error}
                    </p>

                )

            }




            {
                documents.length === 0 ? (

                    <p>
                        No documents available.
                    </p>


                ) : (


                    documents.map((doc) => (


                        <div

                            key={doc.filename}

                            className="document-card"

                        >


                            <h3>
                                {doc.filename}
                            </h3>



                            <p>
                                Pages:
                                {" "}
                                {doc.pages}
                            </p>



                            <p>
                                Chunks:
                                {" "}
                                {doc.chunks}
                            </p>




                            <button

                                onClick={() =>
                                    handleDelete(
                                        doc.filename
                                    )
                                }

                            >

                                Delete

                            </button>



                        </div>


                    ))

                )

            }



        </div>

    );

}



export default DocumentList;