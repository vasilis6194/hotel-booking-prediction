import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import ADRPredictionForm from "./components/ADRPredictionForm";
import CancellationPredictionForm from "./components/CancellationPredictionForm";
import ProjectSummary from "./components/ProjectSummary";
import { Box, CssBaseline } from "@mui/material";

const App = () => {
  return (
    <Router>
      <CssBaseline />
      <Box sx={{ display: "flex", height: "100vh" }}>
        {/* Sidebar on the left */}
        <Sidebar />

        {/* Main Content Area */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3, // Padding for spacing
            width: "calc(100% - 250px)", // Ensures proper width
            overflowY: "auto", // Enables scrolling if needed
          }}
        >
          <Routes>
            <Route path="/" element={<ProjectSummary />} />
            <Route path="/predict-adr" element={<ADRPredictionForm />} />
            <Route path="/predict-cancellation" element={<CancellationPredictionForm />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
};

export default App;
