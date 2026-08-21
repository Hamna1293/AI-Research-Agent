import { Link } from "react-router-dom";
import { Sparkles } from "lucide-react";

import "./Navbar.css";


function Navbar(){


    return (

        <nav className="navbar">


            <div className="brand">


                <div className="logo">

                    <Sparkles size={22}/>

                </div>


                <span>

                    ResearchAI

                </span>


            </div>



            <div className="nav-links">


                <Link to="/">
                    Home
                </Link>


                <Link to="/documents">
                    Documents
                </Link>


                <Link to="/chat">
                    AI Chat
                </Link>


                <Link to="/reports">
                    Reports
                </Link>


            </div>



            <button className="nav-button">

                Launch App

            </button>



        </nav>

    );

}


export default Navbar;