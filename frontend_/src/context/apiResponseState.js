import apiResponseContext from "./apiResponseContext";
import { useState } from "react";

const ApiResponseState = (props) => {
  const url = "http://127.0.0.1:5000/sdm";
  const [apiResponse, setApiResponse] = useState(0);
  const [stdInput, setStdInput] = useState(0);
  const [maInput, setMaInput] = useState(0);
  const [selectedCell, setSelectedCell] = useState({ std: 0, ma: 0 });
  const [isLoading, setIsLoading] = useState(false);
  // const [isLoading,setIsLoading]=

  const cellClickHandler = (stdCellIndex, maCellIndex) => {
    setSelectedCell({ ...selectedCell, std: stdCellIndex, ma: maCellIndex });
  };

  const getData = async (
    symbol1,
    symbol2,
    startDate,
    endDate,
    maxPosition,
    std,
    ma,
    riskFree
  ) => {
    setIsLoading(true);
    console.log(":heya");
    console.log(maxPosition, symbol1, symbol2, startDate, endDate);
    const response = await fetch(
      `https://pair-trading-sdm-backtesting.onrender.com/sdm?symbol1=${symbol1}&symbol2=${symbol2}&start_date=${startDate}&end_date=${endDate}&max_position=${maxPosition}&standard_deviation_limit=${std}&moving_average_limit=${ma}&risk_free=${riskFree}`,
      {}
    );

    // const response = await fetch("./response.json", {
    //   headers: {
    //     "Content-Type": "application/json",
    //     Accept: "application/json",
    //   },
    // });

    const json = await response.json();
    console.log(json);
    setApiResponse(json);
    setMaInput(ma);
    setStdInput(std);
    setIsLoading(false);
  };
  return (
    <apiResponseContext.Provider
      value={{
        getData,
        apiResponse,
        stdInput,
        maInput,
        cellClickHandler,
        selectedCell,
        isLoading,
      }}>
      {props.children}
    </apiResponseContext.Provider>
  );
};
export default ApiResponseState;
