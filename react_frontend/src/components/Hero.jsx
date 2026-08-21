import { motion } from "framer-motion";

import { 
    ArrowRight,
    Sparkles,
    Brain,
    FileText,
    Search
} from "lucide-react";


import { useNavigate } from "react-router-dom";


import AIBackground from "./AIBackground";


import "./Hero.css";



function Hero(){


    const navigate = useNavigate();



    return (

        <section className="hero">



            <AIBackground />



            <div className="hero-glow glow-purple"></div>

            <div className="hero-glow glow-cyan"></div>





            <div className="hero-content">



                <div className="badge">


                    <Sparkles size={16}/>


                    AI Powered Research Intelligence


                </div>





                <h1>


                    Your Research.


                    <br/>


                    Amplified By


                    <br/>


                    <span className="gradient-text">


                        Artificial Intelligence


                    </span>


                </h1>





                <p>


                    Transform thousands of pages into meaningful insights.
                    Upload research papers, discover hidden connections,
                    generate reports, and interact with your knowledge base.


                </p>





                <div className="hero-actions">



                    <button


                    className="primary-btn"


                    onClick={()=>navigate("/workspace")}


                    >



                        Start Discovery



                        <ArrowRight size={18}/>


                    </button>






                    <button


                    className="secondary-btn"


                    onClick={()=>navigate("/knowledge")}


                    >


                        Explore Knowledge



                    </button>



                </div>




            </div>








            <motion.div


            className="floating-card card-one"


            animate={{


                y:[0,-15,0]


            }}


            transition={{


                duration:5,

                repeat:Infinity,

                ease:"easeInOut"


            }}



            >


                <Brain size={25}/>


                <h3>

                    AI Engine

                </h3>


                <span>

                    Semantic Understanding

                </span>



            </motion.div>







            <motion.div


            className="floating-card card-two"



            animate={{


                y:[0,15,0]


            }}



            transition={{


                duration:6,

                repeat:Infinity,

                ease:"easeInOut"


            }}


            >


                <FileText size={25}/>


                <h3>

                    100+

                </h3>


                <span>

                    Research Papers Indexed

                </span>



            </motion.div>








            <motion.div


            className="floating-card card-three"



            animate={{


                y:[0,-10,0]


            }}



            transition={{


                duration:4,

                repeat:Infinity,

                ease:"easeInOut"


            }}



            >



                <Search size={22}/>


                <h3>

                    Smart Retrieval

                </h3>


                <span>

                    Find answers instantly

                </span>



            </motion.div>





        </section>


    );


}



export default Hero;