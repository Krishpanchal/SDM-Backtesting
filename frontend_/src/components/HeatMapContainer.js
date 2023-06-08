import React from "react";
import HeatMap from "react-heatmap-grid";
import apiResponseContext from "../context/apiResponseContext";
import { useContext } from "react";
import "./HeatMapContainer.css";
import { Link, useNavigate, Navigate } from "react-router-dom";
import Title from "./Title";

const HeatMapContainer = (props) => {
  const navigate = useNavigate();
  const context = useContext(apiResponseContext);
  const { apiResponse, stdInput, maInput, cellClickHandler, selectedCell } =
    context;
  console.log(props.parameter);
  console.log(apiResponse["result"]);
  console.log(stdInput);
  let std = [];
  let ma = [];
  let d = [];

  for (let i = 3; i <= parseInt(stdInput); i++) {
    std.push(i);
  }
  for (let i = 3; i <= parseInt(maInput); i++) {
    ma.push(i);
  }
  console.log();
  for (let i = 3; i <= parseInt(maInput); i++) {
    let arr = new Array(parseInt(stdInput - 3)).fill(0);
    d.push([arr]);
    console.log(`arr->${arr} d->${d.length}`);
  }
  // std = [3, 4, 5];
  // ma = [3, 4, 5, 6, 7];
  // d = [
  //   [0, 0, 0],
  //   [0, 0, 0],
  //   [0, 0, 0],
  //   [0, 0, 0],
  //   [0, 0, 0],
  // ];
  console.log(d);
  apiResponse["result"].forEach((element) => {
    d[parseInt(element["ma"]) - 3][parseInt(element["std"]) - 3] =
      // element["df_analysis_json"][6]["value"];

      props.isGlobal
        ? parseFloat(element[props.parameter])
        : props.table == "df_summary_json"
        ? parseFloat(
            element[props.table].filter(
              (data) => data["Output"] == props.parameter
            )[0]["total"]
          )
        : parseFloat(
            element[props.table].filter(
              (data) => data["analysis"] == props.parameter
            )[0]["value"]
          );

    // element["df_summary_json"][9]["total"];
  });

  let styles = {
    padding: "0.2rem",
    fontSize: "15px",
    fontWeight: "bold",
    borderRadius: "0.3rem",
    margin: "0.1rem",
  };

  // total pnl round down to a nearest whole number, pivot to 0
  // profit factor, pivot to 1, below 1 red, above 1 green, two decimal display
  // trades - self table range mid-point.. below mid point red, above mid point green
  // % win - pivot to 50. Below 50 red, above 50 green, one decimal display
  // i. Avg win - show as nearest whole number, pivot to 0, below 0 red, above zero green
  // ii. Avg lose - show as nearest whole number, pivot to 0, below 0 red, above zero green
  //prev color caclucation : for midpoint
  // pivot: (max + min) / 2,
  // //1 - (max - value) / (max - min)
  // greaterStyle: 1 - (max - value) / (max * 0.5),
  // lesserStyle: 1 - (value - min) / (value * 0.8),
  let paramaterStyles = (value, max, min) => {
    return {
      "total pnl": {
        pivot: 0,
        greaterStyle: 1 - (max - value) / max,
        lesserStyle: 1 - (min - value) / min,
      },
      "profit factor": {
        pivot: 1,
        greaterStyle: 1 - (max - value) / (max - 1),
        lesserStyle: 1 - (1 - value) / (1 - min),
      },
      trades: {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "% win": {
        pivot: 50,
        greaterStyle: 1 - (max - value) / (max - 50),
        lesserStyle: 1 - (50 - value) / (50 - min),
      },
      "avg win": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "avg lose": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      strategy_peak_count: {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "gross pnl per trade": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },

      "total_strategy_return_gross_pnl %": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "CAGR strategt return gross pnl %": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "sharpe ratio": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "sortino ratio": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "calmar ratio": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
    };
  };
  const onCellClick = (stdCellIndex, maCellIndex) => {
    let selectedData;
    for (let index = 0; index < apiResponse["result"].length; index++) {
      if (
        apiResponse["result"][index].std === stdCellIndex &&
        apiResponse["result"][index].ma === maCellIndex
      ) {
        selectedData = apiResponse["result"][index];
      }
    }
    localStorage.setItem("data", JSON.stringify(selectedData));

    // navigate("/details");
    window.open("http://localhost:3000/details", "_blank");
  };

  return (
    <div>
      <div className="heat-map-container">
        <Title title={props.parameter} />
        <HeatMap
          xLabels={std}
          cellRender={(value) => value && `${value}`}
          yLabels={ma}
          data={d}
          // xLabels={[1, 2, 3,4,5]}
          // cellRender={(value) => value && `${value}`}
          // yLabels={[1, 2, 3,4,5]}
          // data={[
          //   [18, 19, 20],
          //   [11, 13, 14],
          //   [10, 15, 12],
          //   [13, 11, 12],
          //   [10, 16, 17],
          // ]}
          cellStyle={(background, value, min, max, data, x, y) => {
            //if the cell > max/2->  1 - max-value/max- max/2
            //else                   1-  value -min /max/2-min
            let result = paramaterStyles(value, max, min);

            let pivotValue = result[props.parameter].pivot;
            let greater = result[props.parameter].greaterStyle;
            let lesser = result[props.parameter].lesserStyle;
            if (props.parameter == "profit factor") {
              console.log(
                // `${props.parameter}->${lesser} -> ${min} - ${value} / ${min}`
                `${props.parameter} ${value} ->${lesser}`
              );
            }
            if (x == 0) {
              styles = { ...styles, marginLeft: "1rem" };
            } else {
              styles = { ...styles, marginLeft: "0" };
            }
            return value > pivotValue
              ? {
                  background: `rgba(0,128,0, ${greater})`,
                  ...styles,
                }
              : {
                  background: `rgba(220,20,60, ${lesser})`,
                  ...styles,
                };

            // return {
            //   background: `rgba(0,128,0, ${1 - (max - value) / (max - min)})`,
            //   padding: "0.2rem",
            //   fontSize: "15px",
            //   fontWeight: "bold",
            // };
          }}
          onClick={(x, y) => onCellClick(x + 3, y + 3)}
          title={(value, unit) => `${value}`}
        />
      </div>
    </div>
  );
};

export default HeatMapContainer;
