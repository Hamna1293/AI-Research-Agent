import "./ReportModal.css";

import { X, FileText } from "lucide-react";

import ReportViewer from "./ReportViewer";

function ReportModal({

    filename,

    onClose,

}) {

    if (!filename) return null;

    return (

        <div
            className="modal-overlay"
            onClick={onClose}
        >

            <div
                className="report-modal"
                onClick={(e) => e.stopPropagation()}
            >

                <div className="report-header">

                    <div className="report-title">

                        <FileText size={22} />

                        <div>

                            <h2>

                                AI Research Report

                            </h2>

                            <p>

                                {filename}

                            </p>

                        </div>

                    </div>

                    <button

                        className="modal-close"

                        onClick={onClose}

                    >

                        <X size={20} />

                    </button>

                </div>

                <div className="report-body">

                    <ReportViewer

                        filename={filename}

                    />

                </div>

            </div>

        </div>

    );

}

export default ReportModal;