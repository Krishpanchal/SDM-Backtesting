import React, { useState } from "react";
import { useContext } from "react";

import apiResponseContext from "../context/apiResponseContext";
import "./InputForm.css";

const InputForm = (props) => {
  const context = useContext(apiResponseContext);
  const [symbol1, setSymbol1] = useState("BAJAJELEC.NS");
  const [symbol2, setSymbol2] = useState("BLUESTARCO.NS");
  const [startDate, setStartDate] = useState("2020-10-05");
  const [endDate, setEndState] = useState("2022-10-05");
  const [maxPosition, setMaxPosition] = useState("10");
  const [riskFree, setRiskFree] = useState("5");
  const [ma, setMa] = useState("6");
  const [std, setStd] = useState("6");
  const { getData } = context;
  const onFormSubmit = (e) => {
    e.preventDefault();
    if (
      // symbol1 !== "" &&
      // symbol2 !== "" &&
      // startDate !== "" &&
      // endDate !== "" &&
      // maxPosition !== ""
      true
    ) {
      getData(
        symbol1,
        symbol2,
        startDate,
        endDate,
        maxPosition,
        std,
        ma,
        riskFree
      );
    }
  };

  return (
    <form onSubmit={onFormSubmit} className="input-form">
      <input
        style={{ width: "9rem" }}
        value={symbol1}
        type="text"
        onChange={(e) => {
          setSymbol1(e.target.value);
        }}
        placeholder="Stock Symbol 1"
      />
      <input
        style={{ width: "9rem" }}
        value={symbol2}
        type="text"
        onChange={(e) => {
          setSymbol2(e.target.value);
        }}
        placeholder="Stock Symbol 2"
      />
      <input
        value={startDate}
        type="date"
        onChange={(e) => setStartDate(e.target.value)}
        placeholder="Start Date"
      />
      <input
        value={endDate}
        type="date"
        onChange={(e) => {
          setEndState(e.target.value);
        }}
        placeholder="End Date"
      />
      <input
        style={{ width: "7rem" }}
        value={maxPosition}
        type="text"
        onChange={(e) => setMaxPosition(e.target.value)}
        placeholder="Max Position"
      />
      <input
        style={{ width: "7rem" }}
        value={ma}
        type="text"
        onChange={(e) => setMa(e.target.value)}
        placeholder="Moving Average"
      />
      <input
        style={{ width: "7rem" }}
        value={std}
        type="text"
        onChange={(e) => setStd(e.target.value)}
        placeholder="Standard Deviation"
      />
      <input
        style={{ width: "7rem" }}
        value={riskFree}
        type="text"
        onChange={(e) => setRiskFree(e.target.value)}
        placeholder="Assumed Risk Free %"
      />
      <button className="submit-button">Submit</button>
    </form>
  );
};

export default InputForm;
