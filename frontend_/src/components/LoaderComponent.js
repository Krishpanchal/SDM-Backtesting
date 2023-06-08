import React from "react";
import { Bars } from "react-loader-spinner";
const LoaderComponent = () => {
  return (
    <div
      style={{
        height: "30rem",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Bars
        height="100"
        width="100"
        color="#4fa94d"
        ariaLabel="bars-loading"
        wrapperStyle={{}}
        wrapperClass=""
        visible={true}
      />
    </div>
  );
};

export default LoaderComponent;
