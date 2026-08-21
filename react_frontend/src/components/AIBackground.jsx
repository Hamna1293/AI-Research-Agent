import "./AIBackground.css";


function AIBackground(){

    return (

        <div className="ai-background">


            {/* Ambient gradient layers */}

            <div className="ai-gradient gradient-one"></div>

            <div className="ai-gradient gradient-two"></div>



            {/* Neural mesh */}

            <div className="mesh">

                <span className="mesh-node n1"></span>

                <span className="mesh-node n2"></span>

                <span className="mesh-node n3"></span>

                <span className="mesh-node n4"></span>

                <span className="mesh-node n5"></span>

                <span className="mesh-node n6"></span>


                <span className="mesh-line l1"></span>

                <span className="mesh-line l2"></span>

                <span className="mesh-line l3"></span>

                <span className="mesh-line l4"></span>


            </div>




            {/* Floating intelligence particles */}


            <div className="ai-particle p1"></div>

            <div className="ai-particle p2"></div>

            <div className="ai-particle p3"></div>

            <div className="ai-particle p4"></div>

            <div className="ai-particle p5"></div>





            {/* Moving data streams */}


            <div className="data-stream s1"></div>

            <div className="data-stream s2"></div>

            <div className="data-stream s3"></div>



        </div>

    );

}


export default AIBackground;