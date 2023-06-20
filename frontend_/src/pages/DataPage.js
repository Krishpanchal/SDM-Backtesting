import React from "react";
import DataTable from "../components/DataTable";
import "./DataPage.css";
import DualAxisLineChart from "../components/DualAxisLineChart";
import LineChartComponentModal from "../components/LineChartComponentModal";
import DetailsDataTableF from "../components/DetailsDataTableF";
import BarChartComponent from "../components/BarcChartComponent";
import { BarChartDemo } from "../components/BarChartDemo";

const DataPage = () => {
  const items = JSON.parse(localStorage.getItem("data"));
  console.log(items.df_analysis_json);

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          flexDirection: "column",
          alignItems: "center",
          margin: "1rem",
          padding: "1.5rem",
          backgroundColor: "#262424",
          color: "white",
          borderRadius: "1rem",
          fontWeight: "700",
        }}
      >
        {/* {items.std} : {items.ma} {Object.keys(items.df_json[0])[1]}{" "}
        {Object.keys(items.df_json[0])[2]} */}
        <h2>
          {" "}
          Created at {new Date().toLocaleString()} |{" "}
          {Object.keys(items.df_json[0])[1]} :{" "}
          {Object.keys(items.df_json[0])[2]}
        </h2>
        <table>
          <tr>
            <th>Start Date</th>
            <td> {items.df_json[0].Date}</td>

            <th>Moving Average</th>
            <td>{items.ma}</td>
          </tr>
          <tr>
            <th>End Date</th>
            <td>{items.df_json[items.df_json.length - 1].Date}</td>

            <th>Standard Deviation</th>
            <td>{items.std}</td>
          </tr>
          <tr>
            <th># of bars</th>
            <td>{items.df_json.length}</td>
            <th>Starting Capital</th>
            <td>{items.df_json.initial_investment}</td>
          </tr>
          <tr>
            <th>Max Position</th>
            <td>{items.max_position}</td>
          </tr>
        </table>
      </div>
      <div className="data-container">
        <LineChartComponentModal
          title="Strategy Net Cum PNL & Strategy Gross Cum PNL  "
          items={items.df_json}
          entities={[
            { strategy_net_cum_pnl: "#595954" },
            { strategy_gross_cum_pnl: "#4682B4" },
          ]}
          width={"650px"}
          height={"350px"}
        />

        <LineChartComponentModal
          title=" Sharpe Ratio "
          items={items.df_json}
          entities={[{ sharpe_ratio_net_pnl: "#595954" }]}
          width={"650px"}
          height={"350px"}
        />

        <BarChartDemo
          title=" Strategy Day Gross PNL "
          items={items.df_json}
          entities={[{ strategy_day_gross_pnl: "	#28282B" }]}
          width={"650px"}
          height={"350px"}
        />

        <DataTable title="Anlaysis Table" items={items.df_analysis_json} />
        <DetailsDataTableF title="Details Table" items={items.df_json} />
      </div>
    </div>
  );
};

export default DataPage;

//import { FiMaximize2 } from "react-icons/fi";
// import LineChartComponent from "../components/LineChartComponent";
// import { useState } from "react";
// import Modal from "../components/Modal";
// import DetailsDataTable from "../components/DetailsDataTable";
// {/* </div> */}
// {/* <DataTable items={items.df_json} /> */}
// {/* <DetailsDataTable /> */}
