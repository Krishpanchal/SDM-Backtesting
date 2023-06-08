// import React from "react";
// import ReactDOM from "react-dom";
// import { Column, Table, SortDirection, AutoSizer } from "react-virtualized";
// import "react-virtualized/styles.css";
// import _ from "lodash";
// import "react-virtualized/styles.css";
// import styled from "styled-components";

// const DetailsDataTable = (props) => {
//   let data = JSON.parse(localStorage.getItem("data")).df_json;
//   console.log(data[0]);
//   Object.keys(data[0]).map((e) => console.log(e));
//   let columns = Object.keys(data[0]).map((element) => {
//     return (
//       <Column
//         className="column"
//         label={element.toUpperCase()}
//         dataKey={element}
//         width={120}
//       />
//     );
//   });

//   const TableWrapper = styled.div`
//     .ReactVirtualized__Grid__innerScrollContainer {
//       overflow: visible !important;
//     }
//     ReactVirtualized__Table .ReactVirtualized__Table__headerTruncatedText {
//       display: inline-block;
//       max-width: 100%;
//       white-space: normal;
//       overflow: visible;
//     }

//     .ReactVirtualized__Table__row {
//       overflow: visible !important;
//     }
//     .column {
//       overflow: visible !important;
//     }
//     .ReactVirtualized__Table__headerColumn {
//       color: blue;
//     }

//     .ReactVirtualized__Table__headerRow {
//       border: 1px solid gray;
//       font-size: 12px;
//       font-weight: 700;
//     }
//     .rt-td {
//       overflow-y: visible !important;
//     }
//     .ReactVirtualized__Table__row {
//       background: papayawhip;
//       border-right: 1px solid gray;
//       border-left: 1px solid gray;
//       border-bottom: 1px solid gray;
//     }
//   `;

//   return (
//     <TableWrapper>
//       <div style={{ overflowX: "auto" }}>
//         <div style={{ height: 200, width: 1000 }}>
//           <AutoSizer>
//             {({ height, width }) => (
//               <Table
//                 width={5500}
//                 height={height}
//                 headerHeight={20}
//                 rowHeight={30}
//                 rowCount={data.length}
//                 rowGetter={({ index }) => data[index]}
//                 flexGrow={1}
//               >
//                 {columns}
//                 {/* <Column label="Name" dataKey="name" width={200} />
//                 <Column width={300} label="Description" dataKey="description" />
//                 <Column width={300} label="Age" dataKey="age" />
//                 <Column width={300} label="Location" dataKey="location" /> */}
//               </Table>
//             )}
//           </AutoSizer>
//         </div>
//       </div>
//     </TableWrapper>
//   );
// };

// export default DetailsDataTable;
