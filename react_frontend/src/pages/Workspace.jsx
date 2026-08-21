import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";

import {
    Upload,
    FileText,
    Sparkles,
    ArrowLeft,
    X,
    Clock,
} from "lucide-react";

import DocumentCard from "../components/DocumentCard";
import ChatBox from "../components/ChatBox";

import {
    uploadDocument,
    getDocuments,
    deleteDocument,
} from "../services/documentService";

import "./Workspace.css";


function Workspace() {

    const [activePanel, setActivePanel] = useState(null);

    const [documents, setDocuments] = useState([]);

    const [loading, setLoading] = useState(false);

    const [uploadProgress, setUploadProgress] = useState(0);

    const [uploadStage, setUploadStage] = useState("");

    const [elapsedTime, setElapsedTime] = useState(0);

    const [error, setError] = useState("");

    const [cancelled, setCancelled] = useState(false);


    // ==========================================================
    // UPLOAD CONTROL REFS
    // ==========================================================

    const uploadCancelledRef = useRef(false);

    const progressTimerRef = useRef(null);

    const elapsedTimerRef = useRef(null);


    // ==========================================================
    // LOAD DOCUMENTS
    // ==========================================================

    useEffect(() => {

        loadDocuments();

    }, []);


    // ==========================================================
    // CLEANUP TIMERS
    // ==========================================================

    useEffect(() => {

        return () => {

            if (progressTimerRef.current) {

                clearInterval(
                    progressTimerRef.current
                );

            }

            if (elapsedTimerRef.current) {

                clearInterval(
                    elapsedTimerRef.current
                );

            }

        };

    }, []);


    async function loadDocuments() {

        try {

            setError("");

            const data = await getDocuments();

            setDocuments(data);

        }

        catch (err) {

            console.error(err);

            setError(
                "Failed to load documents."
            );

        }

    }


    // ==========================================================
    // FORMAT ELAPSED TIME
    // ==========================================================

    function formatElapsedTime(seconds) {

        const minutes = Math.floor(
            seconds / 60
        );

        const remainingSeconds = seconds % 60;


        return `${String(minutes).padStart(2, "0")}:${String(
            remainingSeconds
        ).padStart(2, "0")}`;

    }


    // ==========================================================
    // STOP UPLOAD TIMERS
    // ==========================================================

    function stopUploadTimers() {

        if (progressTimerRef.current) {

            clearInterval(
                progressTimerRef.current
            );

            progressTimerRef.current = null;

        }


        if (elapsedTimerRef.current) {

            clearInterval(
                elapsedTimerRef.current
            );

            elapsedTimerRef.current = null;

        }

    }


    // ==========================================================
    // START FRONTEND PROGRESS SIMULATION
    // ==========================================================

    function startProgressSimulation() {

        const stages = [

            {
                progress: 10,
                stage: "Uploading document..."
            },

            {
                progress: 20,
                stage: "Saving document..."
            },

            {
                progress: 30,
                stage: "Loading document..."
            },

            {
                progress: 40,
                stage: "Preprocessing document..."
            },

            {
                progress: 50,
                stage: "Extracting research information..."
            },

            {
                progress: 65,
                stage: "Generating AI research report..."
            },

            {
                progress: 75,
                stage: "Creating document chunks..."
            },

            {
                progress: 85,
                stage: "Generating embeddings..."
            },

            {
                progress: 95,
                stage: "Storing document in knowledge base..."
            },

        ];


        let stageIndex = 0;


        setUploadProgress(
            stages[0].progress
        );

        setUploadStage(
            stages[0].stage
        );


        progressTimerRef.current = setInterval(() => {

            if (uploadCancelledRef.current) {

                return;

            }


            if (
                stageIndex <
                stages.length - 1
            ) {

                stageIndex += 1;


                setUploadProgress(
                    stages[stageIndex].progress
                );


                setUploadStage(
                    stages[stageIndex].stage
                );

            }

        }, 3500);

    }


    // ==========================================================
    // START ELAPSED TIMER
    // ==========================================================

    function startElapsedTimer() {

        const startTime = Date.now();


        setElapsedTime(0);


        elapsedTimerRef.current = setInterval(() => {

            if (uploadCancelledRef.current) {

                return;

            }


            const elapsed = Math.floor(
                (Date.now() - startTime) / 1000
            );


            setElapsedTime(elapsed);

        }, 1000);

    }


    // ==========================================================
    // CANCEL UPLOAD
    // ==========================================================

    const cancelUpload = () => {

        uploadCancelledRef.current = true;

        setCancelled(true);

        setLoading(false);

        setUploadStage(
            "Upload cancelled."
        );


        stopUploadTimers();

    };


    // ==========================================================
    // UPLOAD DOCUMENT
    // ==========================================================

    const handleUpload = async (event) => {

        const files = [
            ...event.target.files
        ];


        if (!files.length) {

            return;

        }


        // ------------------------------------------------------
        // Only one upload process at a time
        // ------------------------------------------------------

        if (loading) {

            return;

        }


        uploadCancelledRef.current = false;

        setCancelled(false);

        setLoading(true);

        setError("");

        setUploadProgress(5);

        setUploadStage(
            "Preparing upload..."
        );


        startElapsedTimer();

        startProgressSimulation();


        try {

            for (const file of files) {

                // ------------------------------------------------
                // Check cancellation before each file
                // ------------------------------------------------

                if (
                    uploadCancelledRef.current
                ) {

                    break;

                }


                setUploadProgress(10);

                setUploadStage(
                    `Uploading ${file.name}...`
                );


                await uploadDocument(file);


                // ------------------------------------------------
                // Check cancellation after upload
                // ------------------------------------------------

                if (
                    uploadCancelledRef.current
                ) {

                    break;

                }

            }


            // ----------------------------------------------------
            // Upload was cancelled
            // ----------------------------------------------------

            if (
                uploadCancelledRef.current
            ) {

                return;

            }


            // ----------------------------------------------------
            // Final processing state
            // ----------------------------------------------------

            setUploadProgress(100);

            setUploadStage(
                "Upload completed successfully."
            );


            await loadDocuments();

        }

        catch (err) {

            console.error(
                "Upload failed:",
                err
            );


            if (
                !uploadCancelledRef.current
            ) {

                setError(
                    "Upload failed. Please try again."
                );

            }

        }

        finally {

            stopUploadTimers();


            if (
                !uploadCancelledRef.current
            ) {

                setLoading(false);

            }


            event.target.value = "";

        }

    };


    // ==========================================================
    // RESET CANCELLED STATE
    // ==========================================================

    const dismissCancelled = () => {

        setCancelled(false);

        setUploadProgress(0);

        setUploadStage("");

        setElapsedTime(0);

    };


    // ==========================================================
    // DELETE DOCUMENT
    // ==========================================================

    const removeDocument = async (filename) => {

        try {

            setError("");

            await deleteDocument(filename);

            await loadDocuments();

        }

        catch (err) {

            console.error(err);

            setError(
                "Unable to delete document."
            );

        }

    };


    // ==========================================================
    // BACK TO WORKSPACE
    // ==========================================================

    const goBack = () => {

        setActivePanel(null);

        setError("");

    };


    // ==========================================================
    // FULL PAGE DOCUMENTS
    // ==========================================================

    if (activePanel === "documents") {

        return (

            <section className="workspace workspace-full">

                <button
                    className="workspace-back-btn"
                    onClick={goBack}
                >

                    <ArrowLeft size={18} />

                    Back to Workspace

                </button>


                <div className="workspace-full-header">

                    <div className="workspace-badge">

                        <FileText size={16} />

                        Research Documents

                    </div>


                    <h1>

                        Your Research

                        <span>
                            Documents
                        </span>

                    </h1>


                    <p>

                        Upload, manage and build your
                        AI knowledge base from research documents.

                    </p>

                </div>


                <div className="workspace-full-content">


                    {/* ==================================================
                        UPLOAD BUTTON
                    ================================================== */}

                    {!loading && !cancelled && (

                        <label className="upload-btn">

                            <Upload size={20} />

                            <strong>
                                Upload PDF
                            </strong>

                            <span>
                                Drag & Drop or Click
                            </span>


                            <input
                                hidden
                                multiple
                                type="file"
                                accept=".pdf"
                                onChange={handleUpload}
                            />

                        </label>

                    )}


                    {/* ==================================================
                        PROCESSING CARD
                    ================================================== */}

                    {
                        loading && (

                            <div className="processing-card">

                                <div className="processing-title">

                                    <div>

                                        <h4>
                                            Processing document...
                                        </h4>

                                        <p className="processing-stage">

                                            {uploadStage}

                                        </p>

                                    </div>


                                    <span className="processing-percent">

                                        {uploadProgress}%

                                    </span>

                                </div>


                                <div className="progress-track">

                                    <motion.div

                                        className="progress-bar"

                                        initial={{
                                            width: "0%",
                                        }}

                                        animate={{
                                            width: `${uploadProgress}%`,
                                        }}

                                        transition={{
                                            duration: 0.5,
                                            ease: "easeOut",
                                        }}

                                    />

                                </div>


                                <div className="processing-footer">

                                    <div className="elapsed-time">

                                        <Clock size={15} />

                                        <span>

                                            Elapsed:

                                            {" "}

                                            {formatElapsedTime(
                                                elapsedTime
                                            )}

                                        </span>

                                    </div>


                                    <button

                                        type="button"

                                        className="cancel-upload-btn"

                                        onClick={
                                            cancelUpload
                                        }

                                    >

                                        <X size={16} />

                                        Cancel Upload

                                    </button>

                                </div>

                            </div>

                        )

                    }


                    {/* ==================================================
                        CANCELLED CARD
                    ================================================== */}

                    {
                        cancelled && !loading && (

                            <div className="processing-card upload-cancelled-card">

                                <div className="processing-title">

                                    <div>

                                        <h4>
                                            Upload Cancelled
                                        </h4>

                                        <p className="processing-stage">

                                            The upload was cancelled.

                                        </p>

                                    </div>


                                    <span className="processing-percent">

                                        {uploadProgress}%

                                    </span>

                                </div>


                                <div className="progress-track">

                                    <div

                                        className="progress-bar"

                                        style={{
                                            width: `${uploadProgress}%`,
                                        }}

                                    />

                                </div>


                                <div className="processing-footer">

                                    <div className="elapsed-time">

                                        <Clock size={15} />

                                        <span>

                                            Stopped after:

                                            {" "}

                                            {formatElapsedTime(
                                                elapsedTime
                                            )}

                                        </span>

                                    </div>


                                    <button

                                        type="button"

                                        className="cancel-upload-btn"

                                        onClick={
                                            dismissCancelled
                                        }

                                    >

                                        <Upload size={16} />

                                        Start New Upload

                                    </button>

                                </div>

                            </div>

                        )

                    }


                    {/* ==================================================
                        ERROR
                    ================================================== */}

                    {
                        error && (

                            <div className="workspace-error">

                                {error}

                            </div>

                        )
                    }


                    {/* ==================================================
                        DOCUMENT LIST
                    ================================================== */}

                    <div className="documents-list">

                        {
                            documents.length === 0 ? (

                                <div className="empty-documents">

                                    <FileText size={40} />

                                    <h3>
                                        No documents yet
                                    </h3>

                                    <p>
                                        Upload a research paper
                                        to start building your
                                        knowledge base.
                                    </p>

                                </div>

                            ) : (

                                documents.map((document) => (

                                    <DocumentCard

                                        key={
                                            document.filename
                                        }

                                        file={document}

                                        onDelete={() =>
                                            removeDocument(
                                                document.filename
                                            )
                                        }

                                    />

                                ))

                            )
                        }

                    </div>

                </div>

            </section>

        );

    }


    // ==========================================================
    // FULL PAGE AI ASSISTANT
    // ==========================================================

    if (activePanel === "assistant") {

        return (

            <section className="workspace workspace-full">

                <button
                    className="workspace-back-btn"
                    onClick={goBack}
                >

                    <ArrowLeft size={18} />

                    Back to Workspace

                </button>


                <div className="workspace-full-header">

                    <div className="workspace-badge">

                        <Sparkles size={16} />

                        AI Research Assistant

                    </div>


                    <h1>

                        Research

                        <span>
                            Assistant
                        </span>

                    </h1>


                    <p>

                        Ask questions and explore insights
                        from your uploaded research documents.

                    </p>

                </div>


                <div className="assistant-full-content">

                    <ChatBox />

                </div>

            </section>

        );

    }


    // ==========================================================
    // MAIN WORKSPACE
    // ==========================================================

    return (

        <section className="workspace">

            <div className="workspace-header">

                <div className="workspace-badge">

                    <Sparkles size={16} />

                    AI Research Environment

                </div>


                <h1>

                    Research

                    <span>
                        Workspace
                    </span>

                </h1>


                <p>

                    Upload documents, analyze knowledge,
                    and interact with your research using AI.

                </p>

            </div>


            <div className="workspace-grid">


                {/* ==================================================
                    DOCUMENT CARD
                ================================================== */}

                <motion.div

                    className="workspace-card"

                    whileHover={{
                        y: -8,
                    }}

                    onClick={() =>
                        setActivePanel("documents")
                    }

                >

                    <div className="card-icon">

                        <FileText size={35} />

                    </div>


                    <h2>
                        Research Documents
                    </h2>


                    <p>

                        Upload research papers and
                        create your AI knowledge base.

                    </p>


                    <div className="card-action">

                        Open Documents

                        <ArrowLeft
                            size={16}
                            style={{
                                transform: "rotate(180deg)",
                            }}
                        />

                    </div>

                </motion.div>


                {/* ==================================================
                    AI ASSISTANT CARD
                ================================================== */}

                <motion.div

                    className="workspace-card"

                    whileHover={{
                        y: -8,
                    }}

                    onClick={() =>
                        setActivePanel("assistant")
                    }

                >

                    <div className="card-icon">

                        <Sparkles size={35} />

                    </div>


                    <h2>
                        AI Research Assistant
                    </h2>


                    <p>

                        Ask questions and generate
                        intelligent insights from your documents.

                    </p>


                    <div className="card-action">

                        Open Assistant

                        <ArrowLeft
                            size={16}
                            style={{
                                transform: "rotate(180deg)",
                            }}
                        />

                    </div>

                </motion.div>


            </div>

        </section>

    );

}


export default Workspace;