import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useContext } from "react";
import apiResponseContext from "../context/apiResponseContext";
import InputForm from "../components/InputForm";
import HeatMapContainer from "../components/HeatMapContainer";
import LoaderComponent from "../components/LoaderComponent";
const HomePage = () => {
  const context = useContext(apiResponseContext);
  const { apiResponse, isLoading } = context;

  return (
    <div>
      <InputForm />
      <div>
        {isLoading ? (
          <LoaderComponent />
        ) : (
          <div>
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                title="Sharpe Ratio"
                parameter="sharpe ratio"
                table="df_analysis_json"
              />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                title="Strategy Net Cumulative PNL"
                parameter="strategy net cum pnl"
                table="df_analysis_json"
              />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                title="Strategy Gross Cumulative PNL"
                parameter="strategy gross cum pnl"
                table="df_analysis_json"
              />
            )}

            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                title="Transaction Costs Gross PNL"
                parameter="transaction costs gross pnl %"
                table="df_analysis_json"
              />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                title="Max Draw Down %"
                parameter="max draw down %"
                table="df_analysis_json"
              />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                title="Calmar Ratio"
                parameter="calmar ratio"
                table="df_analysis_json"
              />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                title="CAGR strategy return net PNL %"
                parameter="CAGR strategy return net pnl %"
                table="df_analysis_json"
              />
            )}

            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                title="Sortino Ratio"
                parameter="sortino ratio"
                table="df_analysis_json"
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
