import { useNavigate } from "react-router-dom";
import { React, useState } from "react";
import axios from "axios";

function Scan() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);

  function handleChange(event) {
    setSelectedFile(event.target.files[0]);
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("selectedFile", selectedFile);
    formData.append("filename", selectedFile.name);
    try {
      const response = await axios({
        method: "post",
        url: "http://localhost:5000/upload",
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
      });
      var query = `?imgUrl=${response.data.imgUrl}&name=${response.data.name}&date=${response.data.date}&amt=${response.data.amt}&accNo=${response.data.accNo}`;
      navigate("/Upload" + query);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h1>Scan the cheque</h1>
        <h3>Please select the correct file</h3>
        <input type="file" className="upload-input" onChange={handleChange} />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}
export default Scan;
