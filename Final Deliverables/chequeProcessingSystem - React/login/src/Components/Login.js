import React, { useState } from "react";
import { Alert } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import Home from "./Home";

function Login() {
  const [emaillog, setEmaillog] = useState(" ");
  const [passwordlog, setPasswordlog] = useState(" ");
  const navigate = useNavigate();

  const [flag, setFlag] = useState(false);

  const [home, setHome] = useState(true);

  function handleRegister(e) {
    navigate("/Register");
  }

  function handleLogin(e) {
    e.preventDefault();

    if (emaillog === "" || passwordlog === "") {
      console.log("Enter the values");
    } else {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
          if (xhttp.responseText === "Successful") {
            localStorage.setItem("name", emaillog);
            navigate("/home");
          } else {
            console.log(xhttp.responseText);
          }
        }
      };
      var url = "http://localhost:5000/login";
      xhttp.open("POST", url);
      xhttp.setRequestHeader(
        "Content-type",
        "application/x-www-form-urlencoded"
      );
      xhttp.send("mail=" + emaillog + "&pass=" + passwordlog);
    }
  }

  return (
    <div>
      {home ? (
        <form onSubmit={handleLogin}>
          <h2>LogIn</h2>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              className="form-control"
              placeholder="Enter email"
              onChange={(event) => setEmaillog(event.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              className="form-control"
              placeholder="Enter password"
              onChange={(event) => setPasswordlog(event.target.value)}
            />
          </div>

          <button
            type="submit"
            className="btn btn-dark btn-lg btn-block button1"
          >
            Login
          </button>

          {flag && (
            <Alert color="primary" variant="warning">
              Fill correct Info else keep trying.
            </Alert>
          )}
          <p onClick={handleRegister} className="forgot-password text-right">
            Don't have an Account?
          </p>
        </form>
      ) : (
        <Home />
      )}
    </div>
  );
}

export default Login;
