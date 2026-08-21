import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

import api from "../api/axios";


function ReportViewer({ filename }) {


    const [report, setReport] = useState("");

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");



    useEffect(() => {


        if (!filename) return;


        let cancelled = false;



        async function fetchReport() {


            try {


                setLoading(true);

                setError("");



                const response = await api.get(

                    `/report/${encodeURIComponent(filename)}`

                );



                if (!cancelled) {

                    console.log("REPORT RESPONSE:", response.data);
                    
                    setReport(

                        response.data.report ||

                        "No report content found."

                    );


                }


            } catch (err) {


                console.error(

                    "Report loading failed:",

                    err

                );



                if (!cancelled) {


                    setError(

                        "Unable to load the research report."

                    );


                }


            } finally {


                if (!cancelled) {


                    setLoading(false);


                }


            }


        }



        fetchReport();



        return () => {


            cancelled = true;


        };


    }, [filename]);



    if (loading) {


        return (

            <div className="report-loading">

                <h3>

                    Loading Report...

                </h3>

                <p>

                    Please wait while your AI report is being loaded.

                </p>

            </div>

        );

    }



    if (error) {


        return (

            <div className="report-error">

                <h3>

                    Error

                </h3>


                <p>

                    {error}

                </p>

            </div>

        );

    }



    return (

        <div className="report-content">

            <ReactMarkdown>

                {report}

            </ReactMarkdown>

        </div>

    );

}


export default ReportViewer;