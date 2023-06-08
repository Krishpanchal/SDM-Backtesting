// import { Chart } from "chart.js";
// import { Line, Chart as Rechart } from "react-chartjs-2";
// import React, { useState } from "react";
// import zoomPlugin from "chartjs-plugin-zoom";
// import "./LineChartComponent.css";
// import { FiMaximize2 } from "react-icons/fi";
// import { Chart as ChartC } from "chart.js/auto";
// import Modal from "./Modal";
// // import Modal from 'react-modal';
// Chart.register(zoomPlugin); // REGISTER PLUGIN
// //strategy cum pnl , spred lower bound upper bound  ,spread-cumulative dual
// const LineChartComponent = (props) => {
//   const [showModal, setShowModal] = useState(false);

//   const handleExpansionClick = () => {
//     setShowModal((prev) => {
//       return !prev;
//     });
//   };
//   let largest = 0;
//   let lowest = 0;
//   const data = {
//     title: "ee",
//     labels: props.items.map((element) => {
//       return element.Date;
//     }),
//     datasets: [
//       ...props.entities.map((entity) => {
//         const key = Object.keys(entity)[0];
//         console.log(entity[key]);
//         return {
//           label: key,
//           data: props.items.map((element) => {
//             if (element[key] > largest) {
//               largest = element[key];
//             }
//             if (element[key] < lowest) {
//               lowest = element[key];
//             }
//             return element[key];
//           }),
//           borderColor: entity[key],
//         };
//       }),
//     ],
//   };

//   const options = {
//     animation: false,
//     // interaction: {
//     //   mode: "index",
//     //   intersect: false,
//     // },
//     // scales: {
//     //   yAxes: [
//     //     {
//     //       ticks: {
//     //         max: 10,
//     //         min: 0,
//     //         stepSize: 5,
//     //       },
//     //     },
//     //   ],
//     // },
//     maintainAspectRatio: false,
//     responsive: true,
//     elements: {
//       point: {
//         radius: 0,
//       },
//       line: {
//         borderWidth: 2.5,
//       },
//     },

//     plugins: {
//       zoom: {
//         limits: {
//           y: {
//             min: lowest + 10,
//             max: largest + 100,
//           },
//         },
//         zoom: {
//           wheel: {
//             enabled: true,
//           },
//           mode: "xy",
//         },
//         pinch: {
//           enabled: true,
//         },
//         pan: {
//           enabled: true,
//           mode: "xy",
//         },
//       },
//     },
//   };

//   // return <Line type="line" data={data} options={options} />;
//   // if (showModal){

//   // }
//   return (
//     <>
//       {showModal && (
//         <Modal
//           content={
//             <div
//               className="line-chart-container"
//               style={{ width: "1400px", height: "700px" }}
//             >
//               <Line type="line" data={data} options={options} />;
//               <div className="btn">
//                 <button onClick={handleExpansionClick}>
//                   <FiMaximize2 />
//                 </button>
//               </div>
//             </div>
//           }
//         />
//       )}

//       {!showModal && (
//         <div
//           className="line-chart-container"
//           style={{ width: props.width, height: props.height }}
//         >
//           <Line type="line" data={data} options={options} />;
//           <div className="btn">
//             <button onClick={handleExpansionClick}>
//               <FiMaximize2 />
//             </button>
//           </div>
//         </div>
//       )}
//     </>
//   );
// };

// export default LineChartComponent;
