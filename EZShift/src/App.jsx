import React, { useState } from 'react';

function App() {
  // Employee information
  const [employees, setEmployees] = useState([
    { id: 1, name: 'Alex', role: 'Barista' },
    { id: 2, name: 'Sam', role: 'Waiter' },
  ]);

  const [name, setName] = useState('');
  const [role, setRole] = useState('');

  // Shift information
  const [shifts, setShifts] = useState([]);
  const [employeeId, setEmployeeId] = useState('');
  const [shiftDate, setShiftDate] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [message, setMessage] = useState('');

  function addEmployee(event) {
    event.preventDefault();

    if (!name.trim() || !role.trim()) return;

    const employee = {
      id: Date.now(),
      name: name.trim(),
      role: role.trim(),
    };

    setEmployees([...employees, employee]);
    setName('');
    setRole('');
  }

  function deleteEmployee(id) {
    setEmployees(employees.filter((employee) => employee.id !== id));
  }

  function editEmployee(id) {
    const employee = employees.find((emp) => emp.id === id);

    const newName = prompt('Enter new name:', employee.name);
    if (newName === null || !newName.trim()) return;

    const newRole = prompt('Enter new role:', employee.role);
    if (newRole === null || !newRole.trim()) return;

    setEmployees(
      employees.map((emp) =>
        emp.id === id
          ? { ...emp, name: newName.trim(), role: newRole.trim() }
          : emp
      )
    );
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
