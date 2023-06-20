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

  console.log(d);
  apiResponse["result"].forEach((element) => {
    try {
      d[parseInt(element["ma"]) - 3][parseInt(element["std"]) - 3] =
        // element["df_analysis_json"][6]["value"];

        parseFloat(
          element[props.table].filter(
            (data) => data["analysis"] == props.parameter
          )[0]["value"]
        );
    } catch (err) {
      console.log(err);
    }
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

      "total strategy return net pnl %": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "CAGR strategy return net pnl %": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "sharpe ratio": {
        pivot: 1,
        greaterStyle: 1 - (max - value) / (max - 1),
        lesserStyle: 1 - (min - value) / (min - 1),
      },
      "sortino ratio": {
        pivot: 1,
        greaterStyle: 1 - (max - value) / (max - 1),
        // lesserStyle: 1 - (1 - value) / (1 - min),
        lesserStyle: 1 - (min - value) / (min - 1),
      },
      "calmar ratio": {
        pivot: 1,
        greaterStyle: 1 - (max - value) / (max - 1),
        lesserStyle: 1 - (min - value) / (min - 1),
      },
      "strategy net cum pnl": {
        pivot: 0,
        greaterStyle: 1 - (max - value) / max,
        lesserStyle: 1 - (min - value) / min,
      },
      "strategy gross cum pnl": {
        pivot: 0,
        greaterStyle: 1 - (max - value) / max,
        lesserStyle: 1 - (min - value) / min,
      },
      "transaction costs gross pnl %": {
        pivot: (max + min) / 2,
        //1 - (max - value) / (max - min)
        greaterStyle: 1 - (max - value) / (max - (max + min) / 2),
        lesserStyle: ((max + min) / 2 - value) / ((max + min) / 2 - min),
      },
      "max draw down %": {
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
    window.open(
      "https://pair-trading-sdm-backtesting.onrender.com/details",
      "_blank"
    );
  };

  return (
    <div>
      <div className='heat-map-container'>
        <Title title={props.title} />
        <p style={{ textAlign: "center" }}>STD</p>
        <div style={{ display: "flex" }}>
          <p style={{ alignSelf: "center" }}>MA</p>
          <div style={{ flex: "1 0 auto" }}>
            <HeatMap
              xLabels={std}
              cellRender={(value) => value && `${value}`}
              yLabels={ma}
              data={d}
              cellStyle={(background, value, min, max, data, x, y) => {
                //if the cell > max/2->  1 - max-value/max- max/2
                //else                   1-  value -min /max/2-min
                let result = paramaterStyles(value, max, min);

                let pivotValue = result[props.parameter].pivot;
                let greater = result[props.parameter].greaterStyle;
                let lesser = result[props.parameter].lesserStyle;

                if (x == 0) {
                  styles = { ...styles, marginLeft: "1rem" };
                } else {
                  styles = { ...styles, marginLeft: "0" };
                }
                let red = 0;
                let green = 0;
                let blue = 0;

                return value > pivotValue
                  ? //for max drawdown the highest should be red and lowest should be green, else highest = green and lowest = red
                    props.parameter == "max draw down %"
                    ? {
                        background: `rgba(220,20,60, ${greater})`,
                        ...styles,
                      }
                    : {
                        background: `rgba(0,128,0, ${greater})`,
                        ...styles,
                      }
                  : props.parameter == "max draw down %"
                  ? {
                      background: `rgba(0,128,0, ${lesser})`,
                      ...styles,
                    }
                  : {
                      background: `rgba(220,20,60, ${lesser})`,
                      ...styles,
                    };

                // {
                //     background: `rgba(220,20,60, ${lesser})`,
                //     ...styles,
                //   }
              }}
              onClick={(x, y) => onCellClick(x + 3, y + 3)}
              title={(value, unit) => `${value}`}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeatMapContainer;
