import React from 'react';

function MatchedJobs({ jobs }) {
//Array.map() is used to render a list of jobs dynamically.
//Each item in a React list should have a unique key (idx in this case).
  return (
    <div>
      <h3>Matched Jobs:</h3>
      <ul>
        {jobs.map((job, idx) => (
          <li key={idx}>
            <strong>{job.title}</strong> ({job.match_score}% match)<br />
            Required: {job.required_skills.join(', ')}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MatchedJobs;