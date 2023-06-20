import { Chart } from "chart.js";
import {
  Bar,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "react-chartjs-2";
import React from "react";
import zoomPlugin from "chartjs-plugin-zoom";
import "./LineChartComponentModal.css";
import { FiMaximize2, FiMinimize2 } from "react-icons/fi";
import { Chart as ChartC } from "chart.js/auto";
import Modal from "react-modal";
import Title from "./Title";

Chart.register(zoomPlugin); // REGISTER PLUGIN
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

const BarChartComponent = (props) => {
  const [modalIsOpen, setIsOpen] = React.useState(false);
  let largest = 0;
  let lowest = 0;
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
    labels: props.items.Date,
    datasets: [
      ...props.entities.map((entity) => {
        const key = Object.keys(entity)[0];
        console.log(entity[key]);
        return {
          label: key,
          data: props.items.map((element) => {
            if (element[key] > largest) {
              largest = element[key];
            }
            if (element[key] < lowest) {
              lowest = element[key];
            }
            return element[key];
          }),
          borderColor: entity[key],
          borderWidth: 3.5,
          //   borderColor: "#D6B4B4",
          borderColor: entity[key],
          tension: 0.4,
          pointRadius: 0.8,
          pointHoverRadius: 6,
        };
      }),
    ],
  };
  console.log(data);

  const options = {
    animation: false,
    responsive: true,
    borderWidth: 10,
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

    plugins: {
      zoom: {
        limits: {
          y: {
            min: lowest,
            max: largest + largest * 0.2,
          },
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          mode: "xy",
        },
        pinch: {
          enabled: true,
        },
        pan: {
          enabled: true,
          mode: "xy",
        },
      },
    },
  };

  // return <Line type="line" data={data} options={options} />;

  return (
    <div>
      <Title title={props.title} />
      <div
        className="line-chart-container"
        // style={{ width: props.width, height: props.height }}
        style={{ width: "40vw", height: "50vh" }}
      >
        <Bar>
          data={data} options={options}
        </Bar>
        {/* <div className="btn"> */}
        <div className="btn" onClick={openModal}>
          <FiMaximize2 />
        </div>
        {/* </div> */}
      </div>
      <Modal
        isOpen={modalIsOpen}
        onAfterOpen={afterOpenModal}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Example Modal"
        overlayClassName="myoverlay"
      >
        <Title title={props.title} />
        <div
          className="line-chart-container"
          style={{ width: "90vw", height: "90vh" }}
        >
          <Bar>
            data={data} options={options}
          </Bar>
          {/* <div className="btn"> */}
          <div className="btn" onClick={closeModal}>
            <FiMinimize2 />
          </div>
          {/* </div> */}
        </div>
      </Modal>
    </div>
  );
};

export default BarChartComponent;
