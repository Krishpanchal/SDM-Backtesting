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
                parameter="sharpe ratio"
                table="df_analysis_json"
              />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer parameter="total pnl" table="df_summary_json" />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                parameter="profit factor"
                table="df_summary_json"
              />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer parameter="trades" table="df_summary_json" />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer parameter="% win" table="df_summary_json" />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer parameter="avg win" table="df_summary_json" />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer parameter="avg lose" table="df_summary_json" />
            )}
            {/* {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer parameter="biggest win" />
            )} */}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                parameter="strategy_peak_count"
                isGlobal={true}
                table="global"
              />
            )}
            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                parameter="gross pnl per trade"
                table="df_analysis_json"
              />
            )}

            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                parameter="total_strategy_return_gross_pnl %"
                table="df_analysis_json"
              />
            )}

            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                parameter="CAGR strategt return gross pnl %"
                table="df_analysis_json"
              />
            )}

            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                parameter="sortino ratio"
                table="df_analysis_json"
              />
            )}

            {apiResponse === 0 ? (
              ""
            ) : (
              <HeatMapContainer
                parameter="calmar ratio"
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
