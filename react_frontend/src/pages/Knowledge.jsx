import { useEffect, useState } from "react";

import "./Knowledge.css";

import api from "../api/axios";


function Knowledge() {

    const [documents, setDocuments] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    const [selectedPaper, setSelectedPaper] = useState(null);

    const [insights, setInsights] = useState([]);

    const [insightsLoading, setInsightsLoading] = useState(false);

    const [insightsError, setInsightsError] = useState("");


    // ==========================================================
    // LOAD DOCUMENTS
    // ==========================================================

    useEffect(() => {

        let mounted = true;


        async function loadDocuments() {

            try {

                setLoading(true);

                setError("");


                const response = await api.get(
                    "/documents"
                );


                if (!mounted) return;


                if (Array.isArray(response.data)) {

                    setDocuments(
                        response.data
                    );

                } else {

                    setDocuments([]);

                    setError(
                        "Invalid document response."
                    );

                }

            } catch (err) {

                console.error(
                    "Knowledge documents error:",
                    err
                );


                if (mounted) {

                    setError(
                        "Unable to load your research library."
                    );

                }

            } finally {

                if (mounted) {

                    setLoading(false);

                }

            }

        }


        loadDocuments();


        return () => {

            mounted = false;

        };

    }, []);


    // ==========================================================
    // CALCULATE TOTAL CHUNKS
    // ==========================================================

    const totalChunks = documents.reduce(
        (total, document) =>
            total + (document.chunks || 0),
        0
    );


    // ==========================================================
    // LOAD INSIGHTS FOR SELECTED PAPER
    // ==========================================================

    const handleExploreInsights = async (document) => {

        setSelectedPaper(document);

        setInsights([]);

        setInsightsError("");

        setInsightsLoading(true);


        try {

            console.log(
                "Loading insights for:",
                document.filename
            );


            const response = await api.get(
                `/insights/${encodeURIComponent(
                    document.filename
                )}`
            );


            console.log(
                "Insights response:",
                response.data
            );


            if (
                response.data &&
                Array.isArray(response.data.insights)
            ) {

                setInsights(
                    response.data.insights
                );

            } else {

                setInsights([]);

                setInsightsError(
                    "No learning insights were generated for this paper."
                );

            }

        } catch (err) {

            console.error(
                "Insights loading failed:",
                err
            );


            setInsights([]);

            setInsightsError(
                "Unable to generate insights for this paper."
            );

        } finally {

            setInsightsLoading(false);

        }

    };


    // ==========================================================
    // CLOSE INSIGHTS
    // ==========================================================

    const closeInsights = () => {

        setSelectedPaper(null);

        setInsights([]);

        setInsightsError("");

    };


    // ==========================================================
    // LOADING STATE
    // ==========================================================

    if (loading) {

        return (

            <div className="knowledge">

                <h1>
                    Knowledge Intelligence
                </h1>

                <p>
                    Loading your research library...
                </p>

            </div>

        );

    }


    // ==========================================================
    // PAGE
    // ==========================================================

    return (

        <div className="knowledge">


            {/* ==================================================
                PAGE HEADER
            ================================================== */}

            <h1>
                Knowledge Intelligence
            </h1>


            <p>
                Turn your research papers into
                focused learning insights.
            </p>


            {/* ==================================================
                ERROR
            ================================================== */}

            {error && (

                <div className="knowledge-error">

                    {error}

                </div>

            )}


            {/* ==================================================
                KNOWLEDGE STATS
            ================================================== */}

            <div className="knowledge-stats">


                <div className="info-card">

                    <h2>
                        Papers Indexed
                    </h2>

                    <span>
                        {documents.length}
                    </span>

                    <p>
                        Research papers in your library
                    </p>

                </div>


                <div className="info-card">

                    <h2>
                        Chunks Analyzed
                    </h2>

                    <span>
                        {totalChunks}
                    </span>

                    <p>
                        Knowledge units available to AI
                    </p>

                </div>


            </div>


            {/* ==================================================
                RESEARCH LIBRARY
            ================================================== */}

            <section className="research-library">


                <div className="section-heading">

                    <div>

                        <span className="section-label">
                            YOUR RESEARCH
                        </span>

                        <h2>
                            AI Learning Insights
                        </h2>

                        <p>
                            Select a paper and let the AI
                            identify the important topics
                            you should understand.
                        </p>

                    </div>

                </div>


                {/* ==================================================
                    EMPTY STATE
                ================================================== */}

                {documents.length === 0 ? (

                    <div className="empty-knowledge">

                        <div className="empty-icon">
                            📚
                        </div>

                        <h3>
                            No research papers yet
                        </h3>

                        <p>
                            Upload a research paper
                            to generate learning insights.
                        </p>

                    </div>

                ) : (

                    <div className="paper-grid">


                        {documents.map((document) => (

                            <div
                                key={document.filename}
                                className={
                                    selectedPaper?.filename ===
                                    document.filename
                                        ? "paper-card selected"
                                        : "paper-card"
                                }
                            >


                                {/* ==========================================
                                    PAPER CARD TOP
                                ========================================== */}

                                <div className="paper-card-top">

                                    <div className="paper-card-icon">
                                        📄
                                    </div>

                                    <span className="paper-badge">
                                        INDEXED
                                    </span>

                                </div>


                                {/* ==========================================
                                    PAPER INFORMATION
                                ========================================== */}

                                <div className="paper-card-content">

                                    <h3>
                                        {document.filename}
                                    </h3>

                                    <p>
                                        {document.pages} Pages
                                        {" • "}
                                        {document.chunks} Chunks
                                    </p>

                                </div>


                                {/* ==========================================
                                    EXPLORE INSIGHTS BUTTON
                                ========================================== */}

                                <button
                                    className="insights-btn"
                                    onClick={() =>
                                        handleExploreInsights(
                                            document
                                        )
                                    }
                                    disabled={
                                        insightsLoading &&
                                        selectedPaper?.filename ===
                                        document.filename
                                    }
                                >

                                    <span>

                                        {
                                            insightsLoading &&
                                            selectedPaper?.filename ===
                                            document.filename
                                                ? "Analyzing..."
                                                : "Explore Insights"
                                        }

                                    </span>


                                    <span className="button-arrow">

                                        {
                                            insightsLoading &&
                                            selectedPaper?.filename ===
                                            document.filename
                                                ? "..."
                                                : "→"
                                        }

                                    </span>

                                </button>


                            </div>

                        ))}


                    </div>

                )}


            </section>


            {/* ==================================================
                SELECTED PAPER INSIGHTS
            ================================================== */}

            {selectedPaper && (

                <section className="insights-panel">


                    {/* ==================================================
                        INSIGHTS HEADER
                    ================================================== */}

                    <div className="insights-panel-header">


                        <div className="insights-title-area">

                            <span className="insights-label">
                                AI LEARNING INSIGHTS
                            </span>


                            <h2>
                                {selectedPaper.filename}
                            </h2>


                            <p>
                                Important topics and concepts
                                identified from this research paper.
                            </p>

                        </div>


                        <button
                            className="close-insights"
                            onClick={closeInsights}
                            aria-label="Close insights"
                        >
                            ×
                        </button>


                    </div>


                    {/* ==================================================
                        INSIGHTS LOADING
                    ================================================== */}

                    {insightsLoading && (

                        <div className="insights-placeholder">

                            <div className="insights-placeholder-icon">
                                🧠
                            </div>


                            <h3>
                                Analyzing your paper
                            </h3>


                            <p>
                                The AI is reading the indexed
                                content and identifying the
                                topics that are most important
                                to understand.
                            </p>


                            <div className="insight-loading-bar">

                                <div className="insight-loading-progress">
                                </div>

                            </div>

                        </div>

                    )}


                    {/* ==================================================
                        INSIGHTS ERROR
                    ================================================== */}

                    {!insightsLoading && insightsError && (

                        <div className="insights-placeholder">

                            <div className="insights-placeholder-icon">
                                ⚠️
                            </div>


                            <h3>
                                Unable to generate insights
                            </h3>


                            <p>
                                {insightsError}
                            </p>

                        </div>

                    )}


                    {/* ==================================================
                        NO INSIGHTS
                    ================================================== */}

                    {!insightsLoading &&
                        !insightsError &&
                        insights.length === 0 && (

                            <div className="insights-placeholder">

                                <div className="insights-placeholder-icon">
                                    🧠
                                </div>


                                <h3>
                                    No insights found
                                </h3>


                                <p>
                                    The AI could not identify
                                    enough learning topics from
                                    this paper.
                                </p>

                            </div>

                        )
                    }


                    {/* ==================================================
                        INSIGHTS RESULTS
                    ================================================== */}

                    {!insightsLoading &&
                        !insightsError &&
                        insights.length > 0 && (

                            <div className="insights-results">


                                <div className="insights-results-heading">

                                    <span>
                                        WHAT YOU SHOULD KNOW
                                    </span>

                                    <p>
                                        These topics were identified
                                        from the content of this paper.
                                    </p>

                                </div>


                                <div className="insights-list">


                                    {insights.map(
                                        (insight, index) => (

                                            <div
                                                className="insight-card"
                                                key={
                                                    `${insight.topic || insight.title || "insight"}-${index}`
                                                }
                                            >


                                                <div className="insight-number">

                                                    {String(
                                                        index + 1
                                                    ).padStart(
                                                        2,
                                                        "0"
                                                    )}

                                                </div>


                                                <div className="insight-content">


                                                    <h3>

                                                        {
                                                            insight.topic ||
                                                            insight.title ||
                                                            `Topic ${index + 1}`
                                                        }

                                                    </h3>


                                                    <p>

                                                        {
                                                            insight.description ||
                                                            insight.explanation ||
                                                            insight.preview ||
                                                            "Important concept identified from this research paper."
                                                        }

                                                    </p>


                                                    {insight.page && (

                                                        <span className="insight-source">

                                                            Page {
                                                                insight.page
                                                            }

                                                        </span>

                                                    )}

                                                </div>


                                            </div>

                                        )
                                    )}


                                </div>


                            </div>

                        )
                    }


                </section>

            )}


        </div>

    );

}


export default Knowledge;