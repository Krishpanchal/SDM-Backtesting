import React from "react";
import { useState } from "react";
import Modal from "./Modal";
import "./DataTable.css";
import { FiMaximize2 } from "react-icons/fi";
import Title from "./Title";
const DataTable = (props) => {
  const getKeys = function () {
    return Object.keys(props.items[0]);
  };

  const getHeader = function () {
    var keys = getKeys();
    console.log(props.items[1]);
    return keys.map((key, index) => {
      return <th key={key}>{key.toUpperCase()}</th>;
    });
  };

  const RenderRow = (props) => {
    return props.keys.map((key, index) => {
      return <td key={props.data[key]}>{props.data[key]}</td>;
    });
  };

  const getRowsData = function () {
    var items = props.items;
    var keys = getKeys();
    return items.map((row, index) => {
      return (
        <tr
          key={
            index +
            Math.floor(Math.random() * 1000) +
            Math.floor(Date.now() / 1000)
          }
        >
          {keys.map((key, index) => {
            return (
              <td
                key={
                  row[key] +
                  Math.floor(
                    Math.random() * 1000 + Math.floor(Date.now() / 1000)
                  )
                }
              >
                {row[key]}
              </td>
            );
          })}
          {/* <RenderRow key={index} data={row} keys={keys} /> */}
        </tr>
      );
    });
  };

  return (
    <div>
      <Title title={props.title} />
      <div className="table-container">
        <div className="table-data-container">
          <table>
            <thead>
              <tr>{getHeader()}</tr>
            </thead>
            <tbody>{getRowsData()}</tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
export default DataTable;
