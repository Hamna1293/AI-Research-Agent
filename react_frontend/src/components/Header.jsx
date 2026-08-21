import { Brain, FileText, Home, Sparkles } from "lucide-react";
import { NavLink } from "react-router-dom";

import "./Header.css";


function Header(){


    return (

        <header className="header">


            <div className="logo">


                <div className="logo-icon">

                    <Brain size={24}/>

                </div>



                <span>

                    ResearchAI

                </span>


            </div>





            <nav className="nav-links">


                <NavLink to="/">

                    <Home size={17}/>

                    Home

                </NavLink>



                <NavLink to="/workspace">


                    <FileText size={17}/>

                    Workspace


                </NavLink>



                <NavLink to="/knowledge">


                    <Sparkles size={17}/>

                    Knowledge


                </NavLink>



            </nav>





            <button className="header-btn">


                Launch AI


            </button>




        </header>

    );

}


export default Header;