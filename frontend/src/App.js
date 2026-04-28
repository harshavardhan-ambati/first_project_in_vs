// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <h1>Hello Welcome to VedhaShree Technologies solutions</h1>
//       </header>
//     </div>
//   );
// }

// export default App;


// import data from './data.json';

// function App() {
//   return (
//     <div>
//       {data.map((item, index) => (
//         <div key={index}>
//           <h1>{item.name}</h1>
//           <p>{item.course}</p>

//           <ul>
//             {item.skills.map((skill, i) => (
//               <li key={i}>{skill}</li>
//             ))}
//           </ul>
//         </div>
//       ))}
//     </div>
//   );
// }

// export default App;


// 


// 



import axios from "axios";
import { useEffect, useState } from "react";
import "./App.css";
const API = "http://10.20.32.13:8000";

function App() {
  const [data, setData] = useState([]);
  const hasUnsavedUser = data.some(user => !user.id);
  const editingUser = data.find(user => !user.id);

  useEffect(() => {
    axios.get(API).then(res => setData(res.data));
  }, []);

  const addUser = () => {
    if (hasUnsavedUser) return;

    const newUser = {
      name: "",
      course: "",
      skills: []
    };
    setData(prev => [...prev, newUser]);
  };

  const saveUser = (user) => {
    if (user.id) {
      axios.patch(`${API}/${user.id}`, user).then(res => {
        setData(prev =>
          prev.map(u => (u.id === user.id ? res.data : u))
        );
      });
    } else {
      axios.post(API, user).then(res => {
        setData(prev =>
          prev.map(u => (u === user ? res.data : u))
        );
      });
    }
  };

  const deleteUser = (id) => {
    axios.delete(`${API}/${id}`).then(() => {
      setData(prev => prev.filter(user => user.id !== id));
    });
  };

  const handleChange = (e, id, field) => {
    const value = e.target.value;

    const updated = data.map(user =>
      user.id === id ? { ...user, [field]: value } : user
    );

    setData(updated);

    if (id) {
      axios.patch(`${API}/${id}`, { [field]: value });
    }
  };

  const handleSkillsChange = (e, id) => {
    const skillsArray = e.target.value
      .split(",")
      .map(s => s.trim());

    const updated = data.map(user =>
      user.id === id ? { ...user, skills: skillsArray } : user
    );

    setData(updated);

    if (id) {
      axios.patch(`${API}/${id}`, { skills: skillsArray });
    }
  };

  return (
    <div className="container">
      <h2>User Form</h2>

      <button className="add-btn" onClick={addUser} disabled={hasUnsavedUser}>
        + Add User
      </button>

      {data.map((user, index) => (
        <div className="form-row" key={user.id || index}>
          <input
            value={user.name}
            disabled={editingUser && editingUser !== user}
            onChange={(e) => handleChange(e, user.id, "name")}
            placeholder="Name"
          />

          <input
            value={user.course}
            disabled={editingUser && editingUser !== user}
            onChange={(e) => handleChange(e, user.id, "course")}
            placeholder="Course"
          />

          <input
            value={user.skills ? user.skills.join(", ") : ""}
            disabled={editingUser && editingUser !== user}
            onChange={(e) => handleSkillsChange(e, user.id)}
            placeholder="Skills (comma separated)"
          />

          <button className="save-btn" onClick={() => saveUser(user)}>
            Save
          </button>

          {user.id && (
            <button
              className="delete-btn"
              style={{ visibility: user.id ? "visible" : "hidden" }}
              onClick={() => deleteUser(user.id)}
            >
              Delete
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

export default App;
