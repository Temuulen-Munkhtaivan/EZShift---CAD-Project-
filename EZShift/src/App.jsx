import React, { useState, useEffect } from 'react';

function App() {
  // Employee information
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/employees')
      .then((response) => response.json())
      .then((data) => setEmployees(data))
      .catch((error) => console.error('Error loading employees:', error));
  }, []);

  const [name, setName] = useState('');
  const [role, setRole] = useState('');

  // Shift information
  const [shifts, setShifts] = useState([]);
  const [employeeId, setEmployeeId] = useState('');
  const [shiftDate, setShiftDate] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [message, setMessage] = useState('');

  async function addEmployee(event) {
    event.preventDefault();

    if (!name.trim() || !role.trim()) return;

    try {
      const response = await fetch('http://127.0.0.1:8000/employees', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: name.trim(),
          role: role.trim()
        })
      });

      if (!response.ok) {
        throw new Error('Failed to add employee');
      }

      const newEmployee = await response.json();

      setEmployees((currentEmployees) => [...currentEmployees, newEmployee]);

      setName('');
      setRole('');

    } catch (error) {
      console.error('Error adding employee:', error);
      alert('Could not add employee. Make sure the backend is running.');
    }
  }

  function deleteEmployee(id) {
    setEmployees(employees.filter((employee) => employee.id !== id));
  }

  async function editEmployee(id) {
    const employee = employees.find((emp) => emp.id === id);

    if (!employee) return;

    const newName = prompt('Enter new name:', employee.name);
    if (newName === null || !newName.trim()) return;

    const newRole = prompt('Enter new role:', employee.role);
    if (newRole === null || !newRole.trim()) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/employees/${id}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: newName.trim(),
            role: newRole.trim()
          })
        }
      );

      if (!response.ok) {
        throw new Error('Failed to update employee');
      }

      const updatedEmployee = await response.json();

      setEmployees((currentEmployees) =>
        currentEmployees.map((emp) =>
          emp.id === id ? updatedEmployee : emp
        )
      );

    } catch (error) {
      console.error('Error updating employee:', error);
      alert('Could not update employee. Make sure the backend is running.');
    }
  }

  function addShift(event) {
    event.preventDefault();

    if (!employeeId || !shiftDate || !startTime || !endTime) {
      return;
    }

    if (endTime <= startTime) {
      setMessage('End time must be after start time.');
      return;
    }

    const conflict = shifts.some((shift) => {
      return (
        shift.employeeId === Number(employeeId) &&
        shift.date === shiftDate &&
        startTime < shift.endTime &&
        endTime > shift.startTime
      );
    });

    if (conflict) {
      setMessage('Shift conflict! Employee already has a shift during this time.');
      return;
    }

    const newShift = {
      id: Date.now(),
      employeeId: Number(employeeId),
      date: shiftDate,
      startTime: startTime,
      endTime: endTime,
    };

    setShifts([...shifts, newShift]);

    // Clear the form
    setEmployeeId('');
    setShiftDate('');
    setStartTime('');
    setEndTime('');

    setMessage('Shift added successfully!');
  }

  return (
    <main className="container">
      <header>
        <h1>EZShift</h1>
        <p>A simple way to manage employees and work shifts.</p>
      </header>

      <section className="panel add-employee-panel">
        <h2>Add an employee</h2>

        <form onSubmit={addEmployee}>
          <input
            placeholder="Employee name"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />

          <input
            placeholder="Role (e.g. Barista)"
            value={role}
            onChange={(event) => setRole(event.target.value)}
          />

          <button type="submit">Add employee</button>
        </form>
      </section>

      <section className="panel employee-list-panel">
        <h2>Employees ({employees.length})</h2>

        <ul>
          {employees.map((employee) => (
            <li key={employee.id}>
              <span>{employee.name}</span>
              <small>{employee.role}</small>

              <div className="actions">
                <button onClick={() => editEmployee(employee.id)}>
                  Edit
                </button>

                <button onClick={() => deleteEmployee(employee.id)}>
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      </section>

      <section className="panel add-shift-panel">
        <h2>Add a Shift</h2>

        <form onSubmit={addShift}>
          <select
            value={employeeId}
            onChange={(e) => setEmployeeId(e.target.value)}
            required
          >
            <option value="">Select Employee</option>

            {employees.map((employee) => (
              <option key={employee.id} value={employee.id}>
                {employee.name}
              </option>
            ))}
          </select>

          <input
            type="date"
            value={shiftDate}
            onChange={(e) => setShiftDate(e.target.value)}
            required
          />

          <input
            type="time"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            required
          />

          <input
            type="time"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
            required
          />

          <button type="submit">Add Shift</button>
        </form>

        <p>{message}</p>
        <p>Total shifts: {shifts.length}</p>
      </section>


      <section className="panel assigned-shifts-panel">
        <h2>Assigned Shifts ({shifts.length})</h2>

        {shifts.length === 0 ? (
          <p>No shifts added yet.</p>
        ) : (
          <ul>
            {shifts.map((shift) => {
              const employee = employees.find(
                (emp) => emp.id === shift.employeeId
              );

              return (
                <li key={shift.id}>
                  <span>
                    {employee ? employee.name : 'Deleted employee'}
                  </span>

                  <small>
                    {shift.date} | {shift.startTime} - {shift.endTime}
                  </small>
                </li>
              );
            })}
          </ul>
        )}
      </section>

    </main>
  );
}

export default App;
