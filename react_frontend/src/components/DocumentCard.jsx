import { useState } from "react";

import {
    FileText,
    Trash2,
    FileSearch,
    CheckCircle2,
} from "lucide-react";

import ReportModal from "./ReportModal";


function DocumentCard({

    file,

    onDelete,

}) {


    const [showReport, setShowReport] = useState(false);


    return (

        <>

            <div className="document-card">


                <div className="document-icon">

                    <FileText size={30} />

                </div>


                <div className="document-info">

                    <h4>

                        {file.filename}

                    </h4>


                    <span>

                        {file.pages} Pages • {file.chunks} Chunks

                    </span>


                    <div className="document-status">

                        <CheckCircle2 size={14} />

                        Indexed Successfully

                    </div>


                </div>



                <div className="document-actions">


                    <button

                        className="report-btn"

                        onClick={() => setShowReport(true)}

                    >

                        <FileSearch size={16} />

                        View Report

                    </button>



                    <button

                        className="delete-btn"

                        onClick={onDelete}

                    >

                        <Trash2 size={16} />

                    </button>


                </div>


            </div>



            {

                showReport && (

                    <ReportModal

                        filename={file.filename}

                        onClose={() => setShowReport(false)}

                    />

                )

            }


        </>

    );

}


export default DocumentCard;