import React from "react";
import DataTable from "../components/DataTable";
import "./DataPage.css";
import DualAxisLineChart from "../components/DualAxisLineChart";
import LineChartComponentModal from "../components/LineChartComponentModal";
import DetailsDataTableF from "../components/DetailsDataTableF";

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
        <h2> Created at {new Date().toLocaleString()}</h2>
        <table>
          <tr>
            <th>Start Date</th>
            <td> {items.df_json[0].Date}</td>
            <th>{Object.keys(items.df_json[0])[1]}</th>
            <td>{items.ratio_data[Object.keys(items.df_json[0])[1]]}</td>
            <th>Moving Average</th>
            <td>{items.ma}</td>
          </tr>
          <tr>
            <th>End Date</th>
            <td>{items.df_json[items.df_json.length - 1].Date}</td>
            <th>{Object.keys(items.df_json[0])[2]}</th>
            <td>{items.ratio_data[Object.keys(items.df_json[0])[2]]}</td>
            <th>Standard Deviation</th>
            <td>{items.std}</td>
          </tr>
          <tr>
            <th># of bars</th>
            <td>{items.df_json.length}</td>
            <th>Starting Capital</th>
            <td>{items.df_json[0].starting_capital_plus_strategy_cum_pnl}</td>
            <th>Max Position</th>
            <td>{items.max_position}</td>
          </tr>
        </table>
      </div>
      <div className="data-container">
        <LineChartComponentModal
          title="Cumulative Pnl"
          items={items.df_json}
          entities={[{ cumulative_pnl: "##595954" }]}
          width={"650px"}
          height={"350px"}
        />
        <LineChartComponentModal
          title="Spread, LowerBound, UpperBound "
          items={items.df_json}
          entities={[
            { spread: "#595954" },
            { lower_bound: "#AC9999" },
            { upper_bound: "#AC9999" },
          ]}
          width={"650px"}
          height={"350px"}
        />
        <DualAxisLineChart
          title="Spread, Cumulative Pnl"
          items={items.df_json}
          width={"650px"}
          height={"350px"}
          entities={[{ spread: "#4054B2" }, { cumulative_pnl: "#ed670e" }]}
        />
        <LineChartComponentModal
          title="B&H value"
          items={items.df_json}
          entities={[{ b_and_h_value: "#4054B2" }]}
          width={"650px"}
          height={"350px"}
        />

        <DataTable title="Anlaysis Table" items={items.df_analysis_json} />
        <DataTable title="Summary Table" items={items.df_summary_json} />
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
