import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Components/Home";
import Login from "./Components/Login";
import "./App.css";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import Registration from "./Components/Registeration";
import Scan from "./Components/Scan";
import Upload from "./Components/Upload";

function App() {
  return (
    <div className="App">
      <div className="outer">
        <div className="inner">
          <BrowserRouter>
            <Routes>
              <Route path="/register" element={<Registration />} />
              <Route exact path="/" element={<Login />} />
              <Route path="/Home" element={<Home />} />
              <Route path="/Scan" element={<Scan />} />
              <Route path="/Upload" element={<Upload />} />
            </Routes>
          </BrowserRouter>
        </div>
      </div>
    </div>
  );
}

export default App;
