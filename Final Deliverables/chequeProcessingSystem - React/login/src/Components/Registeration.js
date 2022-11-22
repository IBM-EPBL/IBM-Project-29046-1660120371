import React, { useState } from "react";
import { Alert } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import Login from "./Login";

function Registration() {
  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [flag, setFlag] = useState(false);
  const [login, setLogin] = useState(true);
  const navigate = useNavigate();

  function handleFormSubmit(e) {
    e.preventDefault();
    if (!name || !email || !password || !username) {
      setFlag(true);
    } else {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
          if (xhttp.responseText === "Successful") {
            navigate("/");
          } else {
            console.log(xhttp.responseText);
          }
        }
      };
      var url = "http://localhost:5000/register";
      xhttp.open("POST", url);
      xhttp.setRequestHeader(
        "Content-type",
        "application/x-www-form-urlencoded"
      );
      xhttp.send(
        "name=" +
          name +
          "&username=" +
          username +
          "&mail=" +
          email +
          "&pass=" +
          password
      );
      // setLogin(!login);
    }
  }

  function handleClick() {
    setLogin(!login);
  }

  return (
    <>
      <div>
        {" "}
        {login ? (
          <form onSubmit={handleFormSubmit}>
            <h2>Register</h2>

            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                className="form-control"
                placeholder="Enter Full Name"
                name="name"
                onChange={(event) => setName(event.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                className="form-control"
                placeholder="Enter your Username"
                onChange={(event) => setUsername(event.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                className="form-control"
                placeholder="Enter your email"
                onChange={(event) => setEmail(event.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                className="form-control"
                placeholder="Enter your password"
                onChange={(event) => setPassword(event.target.value)}
              />
            </div>

            <button
              type="submit"
              className="btn btn-dark btn-lg btn-block button1"
            >
              Register
            </button>
            <p onClick={handleClick} className="forgot-password text-right">
              Already registered log in?
            </p>
            {flag && (
              <Alert color="primary" variant="danger">
                I've got it that you are in hurry! But every Field is
                important...
              </Alert>
            )}
          </form>
        ) : (
          <Login />
        )}
      </div>
    </>
  );
}

export default Registration;
