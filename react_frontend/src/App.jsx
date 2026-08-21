import { BrowserRouter, Routes, Route } from "react-router-dom";


import Header from "./components/Header";


import Hero from "./components/Hero";


import Workspace from "./pages/Workspace";


import Knowledge from "./pages/Knowledge";


function App(){


    return (


        <BrowserRouter>


            <Header />



            <main className="app-content">


                <Routes>


                    <Route

                        path="/"

                        element={<Hero />}

                    />



                    <Route

                        path="/workspace"

                        element={<Workspace />}

                    />



                    <Route

                        path="/knowledge"

                        element={<Knowledge />}

                    />


                </Routes>



            </main>



        </BrowserRouter>


    );

}



export default App;