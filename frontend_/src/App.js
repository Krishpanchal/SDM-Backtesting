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

// function App() {
//   const context = useContext(apiResponseContext);
//   const { apiResponse } = context;
//   return (
//     <div>
//       <InputForm />
//       {apiResponse === 0 ? "" : <HeatMapContainer />}

//       {/* <div>{apiResponse === 0 ? "loading" : <DataTable />}</div> */}
//     </div>
//   );
// }

export default App;
