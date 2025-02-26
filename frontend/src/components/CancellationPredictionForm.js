import React, { useState } from "react";
import {
  TextField,
  Button,
  MenuItem,
  Grid,
  Typography,
  Paper,
} from "@mui/material";
import axios from "axios";

export default function CancellationPredictionForm() {
  // Define state for each input field
  const [inputs, setInputs] = useState({
    lead_time: "",
    arrival_date_year: "",
    arrival_date_day_of_month: "",
    stays_in_weekend_nights: "",
    stays_in_week_nights: "",
    adults: "",
    children: "",
    babies: "",
    is_repeated_guest: "",
    previous_cancellations: "",
    previous_bookings_not_canceled: "",
    required_car_parking_spaces: "",
    total_of_special_requests: "",
    hotel: "",
    meal: "",
    market_segment: "",
    distribution_channel: "",
    reserved_room_type: "",
    deposit_type: "",
    customer_type: "",
  });

  const [prediction, setPrediction] = useState(null);

  // Handle input changes and ensure correct value types
  const handleChange = (e) => {
    let value = e.target.value;

    // Convert numeric fields to numbers
    if (["lead_time", "arrival_date_year", "arrival_date_day_of_month", "stays_in_weekend_nights",
        "stays_in_week_nights", "adults", "children", "babies", "previous_cancellations",
        "previous_bookings_not_canceled", "required_car_parking_spaces", "total_of_special_requests"
    ].includes(e.target.name)) {
      value = value === "" ? "" : Number(value);
    }

    setInputs({ ...inputs, [e.target.name]: value });
  };

  // Submit handler for Cancellation Prediction
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Ensure empty values are replaced with appropriate defaults
      const formattedInputs = Object.fromEntries(
        Object.entries(inputs).map(([key, value]) => [
          key,
          value === "" ? (isNaN(value) ? "Unknown" : 0) : value, // Default unknown for categorical, 0 for numeric
        ])
      );

      const response = await axios.post("http://localhost:8001/predict/cancellation", {
        features: formattedInputs,
      });

      setPrediction(response.data);
    } catch (error) {
      console.error(
        "Error predicting cancellation:",
        error.response ? error.response.data : error
      );
    }
  };

  // Dropdown options
  const yesNoOptions = [
    { value: 1, label: "Yes" },
    { value: 0, label: "No" },
  ];

  const hotelOptions = [
    { value: "City Hotel", label: "City Hotel" },
    { value: "Resort Hotel", label: "Resort Hotel" },
  ];

  const mealOptions = ["BB", "HB", "SC", "FB", "Undefined"].map((m) => ({
    value: m,
    label: m,
  }));
  const marketSegmentOptions = [
    "Online TA",
    "Corporate",
    "Groups",
    "Direct",
    "Offline TA/TO",
    "Complementary",
  ].map((m) => ({ value: m, label: m }));
  const distributionChannelOptions = [
    "Direct",
    "TA/TO",
    "Corporate",
    "GDS",
  ].map((d) => ({ value: d, label: d }));
  const reservedRoomTypeOptions = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "L",
  ].map((r) => ({ value: r, label: r }));
  const depositTypeOptions = ["No Deposit", "Non Refund", "Refundable"].map(
    (d) => ({ value: d, label: d })
  );
  const customerTypeOptions = [
    "Transient",
    "Contract",
    "Group",
    "Transient-Party",
  ].map((c) => ({ value: c, label: c }));

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Cancellation Prediction
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          {/* Numeric fields with constraints */}
          {[
            { name: "lead_time", label: "Lead Time", min: 0, max: 500 },
            { name: "arrival_date_year", label: "Arrival Year", min: 2000, max: 2100 },
            { name: "arrival_date_day_of_month", label: "Arrival Day", min: 1, max: 31 },
            { name: "stays_in_weekend_nights", label: "Stays in Weekend Nights", min: 0, max: 10 },
            { name: "stays_in_week_nights", label: "Stays in Week Nights", min: 0, max: 30 },
            { name: "adults", label: "Adults", min: 1, max: 10 },
            { name: "children", label: "Children", min: 0, max: 10 },
            { name: "babies", label: "Babies", min: 0, max: 5 },
            { name: "previous_cancellations", label: "Previous Cancellations", min: 0, max: 20 },
            { name: "previous_bookings_not_canceled", label: "Previous Bookings Not Canceled", min: 0, max: 50 },
            { name: "required_car_parking_spaces", label: "Required Car Parking Spaces", min: 0, max: 5 },
            { name: "total_of_special_requests", label: "Total Special Requests", min: 0, max: 10 },
          ].map((field) => (
            <Grid item xs={12} sm={6} key={field.name}>
              <TextField
                label={field.label}
                name={field.name}
                type="number"
                value={inputs[field.name]}
                onChange={handleChange}
                fullWidth
                inputProps={{ min: field.min, max: field.max }}
              />
            </Grid>
          ))}

          {/* Dropdowns */}
          {[
            { name: "is_repeated_guest", label: "Is Repeated Guest", options: yesNoOptions },
            { name: "hotel", label: "Hotel Type", options: hotelOptions },
            { name: "meal", label: "Meal Type", options: mealOptions },
            { name: "market_segment", label: "Market Segment", options: marketSegmentOptions },
            { name: "distribution_channel", label: "Distribution Channel", options: distributionChannelOptions },
            { name: "reserved_room_type", label: "Reserved Room Type", options: reservedRoomTypeOptions },
            { name: "deposit_type", label: "Deposit Type", options: depositTypeOptions },
            { name: "customer_type", label: "Customer Type", options: customerTypeOptions },
          ].map((field) => (
            <Grid item xs={12} sm={6} key={field.name}>
              <TextField
                select
                label={field.label}
                name={field.name}
                value={inputs[field.name]}
                onChange={handleChange}
                fullWidth
              >
                {field.options.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
          ))}
        </Grid>
        <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
          Predict Cancellation
        </Button>
        {prediction && (
          <Typography variant="h6" sx={{ mt: 2 }}>
            Predicted Class: {prediction.predicted_class}, Cancellation Probability: {prediction.cancellation_probability.toFixed(2)}%
          </Typography>
        )}
      </form>
    </Paper>
  );
}
