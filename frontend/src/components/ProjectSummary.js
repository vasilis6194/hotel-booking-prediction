import React from 'react';
import { Typography, Box, Grid, Paper } from '@mui/material';
import hotelImage from "../assets/hotel.jpg"; // ✅ Import the hotel image

export default function ProjectSummary() {
  return (
    <Paper
      elevation={3}
      sx={{
        p: 3,
        backgroundImage: `url(${hotelImage})`, // ✅ Background image
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        position: "relative",
        color: "white", // Ensure text is visible
        textShadow: "1px 1px 4px rgba(0,0,0,0.6)", // Slight shadow for contrast
        minHeight: "90vh", // Ensures full coverage
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1,
      }}
    >
      {/* Overlay to make text more readable */}
      <Box
        sx={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          backgroundColor: "rgba(0, 0, 0, 0.5)", // Dark overlay (adjust opacity as needed)
          zIndex: -1,
        }}
      />

      <Typography variant="h4" gutterBottom align="center">
        📖 Overview
      </Typography>

      <Typography variant="body1" paragraph>
        This project builds an <strong>end-to-end predictive analytics pipeline</strong> for the hospitality industry, focusing on two critical tasks:
      </Typography>

      <Typography variant="body1" paragraph>
        <strong>1. Booking Cancellation Prediction (Classification)</strong>: Predict whether a hotel booking will be canceled.
      </Typography>

      <Typography variant="body1" paragraph>
        <strong>2. Average Daily Rate (ADR) Prediction (Regression)</strong>: Forecast the price per night for a booking.
      </Typography>

      <Typography variant="body1" paragraph>
        The solution is <strong>production-ready</strong>, providing <strong>real-time predictions</strong> through an API built with <strong>FastAPI</strong>, a frontend built with <strong>React</strong>, and containerized with <strong>Docker</strong> for easy deployment.
      </Typography>

      <Box mt={3}>
        <Typography variant="h5" gutterBottom align="center">
          🎯 Project Goals
        </Typography>

        <Grid container spacing={2} sx={{ maxWidth: "800px" }}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body1">✔️ <strong>Predict Booking Cancellations</strong> – Optimize hotel management and reduce lost revenue.</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body1">✔️ <strong>Forecast ADR</strong> – Improve dynamic pricing strategies for hotels.</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body1">✔️ <strong>Deployment-Ready</strong> – Serve predictions via API & Docker for scalability.</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body1">✔️ <strong>Model Optimization</strong> – Use feature engineering, Optuna-based hyperparameter tuning, and outlier handling.</Typography>
          </Grid>
        </Grid>
      </Box>
    </Paper>
  );
}
