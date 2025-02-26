import React from "react";
import { Typography, Paper, Box } from "@mui/material";
import hotelImage from "../assets/hotel.jpg"; // ✅ Import the hotel image

export default function ProjectSummary() {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Project Summary
      </Typography>
      <Typography variant="body1" sx={{ mb: 2 }}>
        Welcome to our hospitality analytics project! This tool helps predict **ADR (Average Daily Rate)** 
        and **Booking Cancellations** using machine learning models trained on historical data. Users can 
        enter booking details and receive real-time predictions.
      </Typography>
      <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
        <img src={hotelImage} alt="Hotel" style={{ width: "100%", maxWidth: "600px", borderRadius: "10px" }} />
      </Box>
    </Paper>
  );
}
