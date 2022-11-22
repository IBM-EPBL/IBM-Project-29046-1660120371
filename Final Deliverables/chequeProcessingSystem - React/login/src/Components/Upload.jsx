import React, { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { numberToWords } from "amount-to-words";

function Upload() {
  function inWords(num) {
    var str = "";
    str = numberToWords(num) + " only";
    return str;
  }

  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [name, setName] = useState(searchParams.get("name"));
  const [amt, setAmt] = useState(searchParams.get("amt"));
  const [date, setDate] = useState(searchParams.get("date"));
  const [acc, setAcc] = useState(searchParams.get("accNo"));
  const [amtWord, setAmtWord] = useState(inWords(searchParams.get("amt")));

  function saveData() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
      navigate("/Home");
    };
    var fname = searchParams.get("imgUrl");
    var username = localStorage.getItem("name");
    xhttp.open("POST", "http://localhost:5000/saveDetails");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(
      `username=${username}&name=${name}&amt=${amt}&date=${date}&accNo=${acc}&amtWord=${amtWord}&file=${fname}`
    );
  }

  return (
    <div>
      <img
        src={require("../../../../chequeProcessor/fileUpload/procFile/" +
          searchParams.get("imgUrl"))}
        alt="cheque"
        width="600px"
        height="270px"
      />
      <form>
        <div className="form-group">
          <label>Name</label>
          <input
            type="text"
            className="form-control"
            placeholder="Enter Full Name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            name="name"
          />
        </div>

        <div className="form-group">
          <label>Amount</label>
          <input
            type="text"
            className="form-control"
            placeholder="Enter Amount"
            value={amt}
            onChange={(event) => {
              setAmt(event.target.value);
              setAmtWord(inWords(event.target.value));
            }}
          />
        </div>

        <div className="form-group">
          <label>Amount in words</label>
          <input
            disabled
            type="text"
            value={amtWord}
            className="form-control"
          />
        </div>

        <div className="form-group">
          <label>Date</label>
          <input
            type="text"
            className="form-control"
            placeholder="Enter Date"
            value={date}
            onChange={(event) => setDate(event.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Account Number</label>
          <input
            type="Phone"
            className="form-control"
            placeholder="Enter Accoune Number"
            value={acc}
            onChange={(event) => setAcc(event.target.value)}
          />
        </div>

        <button
          type="submit"
          className="btn btn-dark btn-lg btn-block button1 "
          onClick={saveData}
        >
          Submit
        </button>
      </form>
    </div>
  );
}

export default Upload;
