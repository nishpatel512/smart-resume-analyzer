import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import MatchedJobs from './components/MatchedJobs';
import axios from 'axios';

function App() {
  //useState lets me create reactive variables
  //parseData stores infor from uploaded resume
  //matchedJobs stores job matches returned from backend
  const [parsedData, setParsedData] = useState(null);
  const [matchedJobs, setMatchedJobs] = useState([]);

  //this func is triggered by UploadForm.js when upload is success
  //makes a get request to FastAPI with resume_id
  const handleUploadSuccess = async (data) => {
    setParsedData(data.parsed_data);
    try {
      const res = await axios.get(`http://localhost:8000/match-jobs/${data.resume_id}`);
      setMatchedJobs(res.data.matched_jobs);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Smart Resume Analyzer</h1>
      <UploadForm onUploadSuccess={handleUploadSuccess} />
      {matchedJobs.length > 0 && <MatchedJobs jobs={matchedJobs} />}
    </div>
  );
}

export default App;