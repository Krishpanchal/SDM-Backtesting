// import Chart from "chart.js/auto";
// import { Chart as RChart } from "chart.js";
// import { Line, Chart as ReChart } from "react-chartjs-2";
// import React from "react";
// import { CategoryScale } from "chart.js";
// import zoomPlugin from "chartjs-plugin-zoom";
// RChart.register(zoomPlugin); // REGISTER PLUGIN
// export default function LineChartComponentR(props) {
//   const options = {
//     plugins: {
//       zoom: {
//         zoom: {
//           rangeMax: {
//             x: "2022-09-13",
//             y: "2000",
//           },
//           wheel: {
//             enabled: true, // SET SCROOL ZOOM TO TRUE
//           },
//           mode: "xy",
//           speed: 5,
//         },
//         pan: {
//           enabled: true,
//           mode: "x",
//           speed: 5,
//         },
//         drag: {
//           enabled: true,
//         },
//       },
//     },
//   };

//   const data = {
//     title: props.title,
//     labels: props.items.map((element) => {
//       return element.Date;
//     }),
//     datasets: [
//       {
//         data: props.items.map((element) => {
//           return element.cumulative_pnl;
//         }),

//         borderColor: "red",
//       },
//     ],
//   };

//   return (
//     <div>
//       <Line
//         type="line"
//         data={data}
//         options={options}
//         width={900}
//         height={450}
//       />
//     </div>
//   );
// }

// //---------------------------
// // import Chart from "chart.js/auto";
// // import { Chart as RChart } from "chart.js";
// // import { Line, Chart as ReChart } from "react-chartjs-2";
// // import React from "react";
// // import { CategoryScale } from "chart.js";
// // import zoomPlugin from "chartjs-plugin-zoom";

// // RChart.register(zoomPlugin); // REGISTER PLUGIN

// // const LineChartComponentR = (props) => {
// //   const data = {
// //     title: props.title,
// //     labels: props.items.map((element) => {
// //       return element.Date;
// //     }),
// //     datasets: [
// //       {
// //         data: props.items.map((element) => {
// //           return element.cumulative_pnl;
// //         }),

// //         borderColor: "red",
// //       },
// //     ],
// //   };

// //   const options = {
// //     maintainAspectRatio: false,
// //     responsive: true,
// //     elements: {
// //       point: {
// //         radius: 0,
// //       },
// //       line: {
// //         borderWidth: 1.5,
// //       },
// //     },

// //     plugins: {
// //       zoom: {
// //         zoom: {
// //           wheel: {
// //             enabled: true, // SET SCROOL ZOOM TO TRUE
// //           },
// //           mode: "xy",
// //           speed: 100,
// //         },
// //         pan: {
// //           enabled: true,
// //           mode: "xy",
// //           speed: 100,
// //         },
// //       },
// //     },
// //   };

// //   return (
// //     <div>
// //       <Line
// //         type="line"
// //         data={data}
// //         options={options}
// //         width={900}
// //         height={450}
// //       />
// //     </div>
// //   );
// // };

// // export default LineChartComponentR;
