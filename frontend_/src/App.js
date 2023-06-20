import InputForm from "./components/InputForm";
import HeatMapContainer from "./components/HeatMapContainer";
import "./App.css";
import apiResponseContext from "./context/apiResponseContext";
import { useContext } from "react";
import DataPage from "./pages/DataPage";

import HomePage from "./pages/HomePage";
import { Route, Routes } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/details" element={<DataPage />} />
    </Routes>
  );
}

export default App;
