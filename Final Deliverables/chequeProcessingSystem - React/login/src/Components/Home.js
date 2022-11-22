import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function fileScan() {
  <Link to="/Scan" />;
}

function Home() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const options = {
      headers: { "Content-type": "application/x-www-form-urlencoded" },
    };

    fetch(
      `http://localhost:5000/getDetails?username=${localStorage.getItem(
        "name"
      )}`,
      options
    )
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div>
      <nav className="side">
        <div className="logo-name">
          <div className="logo-image"></div>
          <span className="logo_name">Welcome</span>
        </div>

        <div className="menu-items">
          <ul className="nav-links">
            <li>
              <a href="/Home">
                <i className="uil uil-estate"></i>
                <span className="link-name">Dashboard</span>
              </a>
            </li>
            <li>
              <a href="/Scan">
                <i className="uil uil-files-landscapes"></i>
                <span onClick={fileScan()} className="link-name">
                  Scan a cheque
                </span>
              </a>
            </li>
          </ul>
        </div>
      </nav>
      <div className="dashboard">
        <div className="top">
          <nav className=" navbar navbar-expand-lg navbar-dark bg-dark">
            <i className=" icon fa-brands fa-neos fa-xl"></i>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarSupportedContent"
              aria-controls="navbarSupportedContent"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div
              className="collapse navbar-collapse "
              id="navbarSupportedContent"
            >
              <ul className="navbar-nav ml-auto mb-1 mt-1 px-5">
                <li className="nav-item ms-auto ">
                  <a className="nav-link logout" href="/">
                    Logout
                  </a>
                </li>
              </ul>
            </div>
          </nav>
        </div>
      </div>
      <h1>Previously Scanned Cheques</h1>
      {data.length === 0 ? (
        <h3>No Cheques scanned so far...</h3>
      ) : (
        <table className="table table-bordered table1">
          <thead>
            <tr>
              <th scope="col">S.No</th>
              <th scope="col">Pay To</th>
              <th scope="col">Account Number</th>
              <th scope="col">Date</th>
              <th scope="col">Amount</th>
              <th scope="col">Amount in words</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => {
              return (
                <tr key={item.sNo}>
                  <th scope="row">{item.sNo + 1}</th>
                  <td>{item.name}</td>
                  <td>{item.accNo}</td>
                  <td>{item.date}</td>
                  <td>{item.amt}</td>
                  <td>{item.amtWord}</td>
                </tr>
              );
            })}
            {/* <th scope="row">1</th>
            <td>Narayanan</td>
            <td>5</td>
            <td>@Front end</td>
            <td>1</td>
            <td>2</td> */}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Home;
