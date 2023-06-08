import { Chart } from "chart.js";
import { Line, Chart as Rechart } from "react-chartjs-2";
import React, { useState } from "react";
import zoomPlugin from "chartjs-plugin-zoom";
import "./LineChartComponentModal.css";
import { FiMaximize2 } from "react-icons/fi";
import { Chart as ChartC } from "chart.js/auto";
import Modal from "react-modal";
import Title from "./Title";
// import Modal from 'react-modal';
Chart.register(zoomPlugin); // REGISTER PLUGIN

const DualAxisLineChart = (props) => {
  const [modalIsOpen, setIsOpen] = React.useState(false);

  Modal.setAppElement("#root");

  const customStyles = {
    content: {
      top: "50%",
      left: "50%",
      right: "auto",
      bottom: "auto",
      zIndex: "999",
      marginRight: "-50%",
      transform: "translate(-50%, -50%)",
    },
  };
  let largest = {};
  let lowest = {};
  let keys = [];

  function openModal() {
    setIsOpen(true);
  }
  let subtitle;
  function afterOpenModal() {
    // references are now sync'd and can be accessed.
    subtitle.style.color = "#f00";
  }

  function closeModal() {
    setIsOpen(false);
  }

  const data = {
    title: "ee",
    labels: props.items.map((element) => {
      return element.Date;
    }),
    datasets: [
      ...props.entities.map((entity) => {
        const key = Object.keys(entity)[0];
        console.log(entity[key]);
        largest[key] = 0;
        lowest[key] = 0;
        keys.push(key);
        return {
          label: key,
          yAxisID: key,
          data: props.items.map((element) => {
            if (element[key] > largest[key]) {
              largest[key] = element[key];
            }
            if (element[key] < lowest[key]) {
              lowest[key] = element[key];
            }
            return element[key];
          }),
          borderColor: entity[key],
          borderWidth: 3.5,
          borderColor: entity[key],
          tension: 0.5,
          pointRadius: 1,
          pointHoverRadius: 5,
        };
      }),
    ],
  };

  let options = {
    animation: false,
    scales: {
      [keys[0]]: {
        type: "linear",
        position: "left",
      },
      [keys[1]]: {
        type: "linear",
        position: "right",
        // ticks: {
        //   max: 1,
        //   min: 0,
        // },
      },
    },
    maintainAspectRatio: false,
    responsive: true,
    elements: {
      point: {
        radius: 1,
      },
      line: {
        borderWidth: 1.5,
      },
    },
  };

  return (
    <div>
      <Title title={props.title} />
      <div
        className="line-chart-container"
        // style={{ width: props.width, height: props.height }}
        style={{ width: "40vw", height: "50vh" }}
      >
        <Line type="line" data={data} options={options} />;
        <div className="btn" onClick={openModal}>
          <FiMaximize2 />
        </div>
      </div>
      <Modal
        isOpen={modalIsOpen}
        onAfterOpen={afterOpenModal}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Example Modal"
        overlayClassName="myoverlay"
      >
        <div
          className="line-chart-container"
          style={{ width: "90vw", height: "90vh" }}
        >
          <Line type="line" data={data} options={options} />
          <div className="btn" onClick={closeModal}>
            <FiMaximize2 />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default DualAxisLineChart;

//plugins for zoom to be added in options
// plugins: {
//   zoom: {
//     limits: {
//       y: {
//         min: lowestA - 10,
//         max: largestA + 10,
//       },
//       y2: {
//         min: lowestB - 10,
//         max: largestB + 10,
//       },
//       //   A: {
//       //     min: Math.min(lowestA, lowestB) - 10,
//       //     max: Math.max(largestA, largestB) + 10,
//       //   },
//       //   B: {
//       //   min: Math.min(lowestA, lowestB) - 10,
//       //   max: Math.max(largestA, largestB) + 10,
//       //   },
//     },
//     zoom: {
//       wheel: {
//         enabled: true,
//       },
//       mode: "xy",
//     },
//     pinch: {
//       enabled: true,
//     },
//     pan: {
//       enabled: true,
//       mode: "xy",
//     },
//   },
// },

//    scales:{

//        y: {
//             min: lowestA - 10,
//             max: largestA + 10,
//           },
//           y2: {
//             position: "right",
//             min: lowestB - 10,
//             max: largestB + 10,
//           },
//    } ,
