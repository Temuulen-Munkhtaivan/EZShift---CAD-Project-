# EZShift

A simple web app for managing employees and work shifts. This project is being developed for my Cloud Application Development module.

## What works so far
- View, add, edit and delete employees
- Create and display employee shifts
- Detect overlapping shifts
- Basic input validation
- Automatic frontend build checks using GitHub Actions

The data is stored in React state for now, so refreshing the page resets it.

## Technologies
- React, JavaScript and CSS
- Vite
- GitHub Actions (CI)

## Run the project
1. Install Node.js if needed.
2. Open the project in VS Code.
3. Navigate to the `EZShift` folder.
4. Run:

```bash
npm install
npm run dev
```

5. Open the local address shown in the terminal.

## Next steps
- Build a separate REST API using FastAPI
- Connect a database
- Add automated tests
- Deploy the application to the cloud