import React from "react";
import _ from "lodash";
import { faker } from "@faker-js/faker";
import { Table } from "react-fluid-table";
import { FiMaximize2 } from "react-icons/fi";
import Modal from "react-modal";
import Title from "./Title";
import "./DetailsDataTableF.css";
Modal.setAppElement("#root");

const customStyles = {
  content: {
    top: "50%",
    left: "50%",
    right: "auto",
    bottom: "auto",
    marginRight: "-50%",
    transform: "translate(-50%, -50%)",
  },
};

const DetailsDataTableF = (props) => {
  const [modalIsOpen, setIsOpen] = React.useState(false);
  const data = props.items;

  const columns = [
    ...Object.keys(props.items[0]).map((key) => {
      console.log(key);

      return {
        key: key,
        header: key,
        // (props) => {
        //   return (
        //     <div
        //       className="title"
        //       style={{ width: "180px", overflowX: "auto", ...props.style }}
        //     >
        //       {key}
        //     </div>
        //   );
        // },
        width: 180,
        content: ({ row }) => {
          if (!isNaN(row[key])) {
            return (
              <div style={row[key] < 0 ? { color: "red" } : {}}>{row[key]}</div>
            );
          } else {
            return <div> {row[key]}</div>;
          }
        },
      };
    }),
  ];
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

  return (
    <div>
      <Title title={props.title} />
      <div
        style={{
          margin: "1rem",
          // width: "40rem",
          height: "32rem",
          position: "relative",

          borderRadius: "0.5rem",
          boxShadow: " 0 3px 15px rgba(10, 9, 9, 0.2)",
        }}
      >
        <Table width="35rem" data={data} columns={columns} />
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
      >
        <Title title={props.title} />
        <div
          style={{
            margin: "1rem",
            width: "95vw",
            height: "90vh",
            position: "relative",
            border: "0.2rem solid black",
            borderRadius: "0.5rem",
          }}
        >
          <Table width="95vw" data={data} columns={columns} />
          <div className="btn" onClick={closeModal}>
            <FiMaximize2 />
          </div>
        </div>
      </Modal>
    </div>
  );
};
export default DetailsDataTableF;
