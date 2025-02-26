import React, { useState } from 'react';
import { TextField, Button, MenuItem, Grid, Typography } from '@mui/material';
import axios from 'axios';
import dayjs from 'dayjs'; // For date validation

export default function ADRPredictionForm() {
  const today = dayjs().format('YYYY-MM-DD'); // Get today's date

  // Define state for inputs and errors
  const [inputs, setInputs] = useState({
    lead_time: '',
    arrival_date_year: '',
    arrival_date_month: '',
    arrival_date_week_number: '',
    arrival_date_day_of_month: '',
    stays_in_weekend_nights: '',
    stays_in_week_nights: '',
    adults: '',
    children: '',
    babies: '',
    is_repeated_guest: '',
    previous_cancellations: '',
    previous_bookings_not_canceled: '',
    required_car_parking_spaces: '',
    total_of_special_requests: '',
    reservation_status_date: today, // Default to today
    hotel: '',
    meal: '',
    country: '',
    market_segment: '',
    distribution_channel: '',
    reserved_room_type: '',
    customer_type: '',
    deposit_type: ''
  });

  const [errors, setErrors] = useState({});
  const [prediction, setPrediction] = useState(null);

  // Handle input changes
  const handleChange = (e) => {
    setInputs({ ...inputs, [e.target.name]: e.target.value });
  };

  // Validate numeric fields (must be non-negative and within range)
  const numericFields = {
    lead_time: { min: 0, max: 730 },
    arrival_date_year: { min: 2020, max: 2100 },
    arrival_date_week_number: { min: 1, max: 53 },
    arrival_date_day_of_month: { min: 1, max: 31 },
    stays_in_weekend_nights: { min: 0, max: 10 },
    stays_in_week_nights: { min: 0, max: 30 },
    adults: { min: 1, max: 10 },
    children: { min: 0, max: 5 },
    babies: { min: 0, max: 3 },
    previous_cancellations: { min: 0, max: 5 },
    previous_bookings_not_canceled: { min: 0, max: 10 },
    required_car_parking_spaces: { min: 0, max: 5 },
    total_of_special_requests: { min: 0, max: 5 }
  };

  // Validate before submission
  const validateInputs = () => {
    let newErrors = {};

    

    Object.keys(numericFields).forEach((field) => {
      const value = parseInt(inputs[field], 10);
      if (isNaN(value) || value < numericFields[field].min || value > numericFields[field].max) {
        newErrors[field] = `Value must be between ${numericFields[field].min} and ${numericFields[field].max}`;
      }
    });

    // Validate date (cannot be in the future)
    if (inputs.reservation_status_date > today) {
      newErrors.reservation_status_date = 'Reservation date cannot be in the future';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0; // Return true if no errors
  };

  // Submit handler for ADR Prediction
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateInputs()) return;

    try {
      const response = await axios.post('http://localhost:8000/predict/adr', { features: inputs });
      setPrediction(response.data.predicted_adr);
    } catch (error) {
      console.error("Error predicting ADR:", error.response ? error.response.data : error);
    }
  };

  // Dropdown options
  const monthOptions = [...Array(12)].map((_, i) => ({
    value: dayjs().month(i).format("MMMM"),
    label: dayjs().month(i).format("MMMM")
  }));

  const hotelOptions = ["City Hotel", "Resort Hotel"].map((v) => ({ value: v, label: v }));
  const mealOptions = ["BB", "HB", "SC", "Other"].map((v) => ({ value: v, label: v }));
  const marketSegmentOptions = ["Online TA", "Offline TA/TO", "Corporate", "Groups", "Complementary", "Other"].map((v) => ({ value: v, label: v }));
  const distributionChannelOptions = ["Direct", "TA/TO", "Corporate", "Other"].map((v) => ({ value: v, label: v }));
  const reservedRoomTypeOptions = ["A", "B", "C", "D", "E", "F", "G", "H", "L"].map((v) => ({ value: v, label: v }));
  const depositTypeOptions = ["No Deposit", "Non Refund", "Refundable"].map((v) => ({ value: v, label: v }));
  const customerTypeOptions = ["Transient", "Contract", "Transient-Party", "Group"].map((v) => ({ value: v, label: v }));

  return (
    <form onSubmit={handleSubmit}>
      <Typography variant="h5" gutterBottom>
        ADR Prediction
      </Typography>
      <Grid container spacing={2}>
        {Object.keys(numericFields).map((field) => (
          <Grid item xs={12} sm={6} key={field}>
            <TextField
              label={field.replace(/_/g, ' ')}
              name={field}
              type="number"
              value={inputs[field]}
              onChange={handleChange}
              fullWidth
              error={!!errors[field]}
              helperText={errors[field] || ''}
            />
          </Grid>
        ))}
        {/* Date Picker for Reservation Status Date */}
        <Grid item xs={12} sm={6}>
          <TextField
            label="Reservation Status Date"
            name="reservation_status_date"
            type="date"
            value={inputs.reservation_status_date}
            onChange={handleChange}
            fullWidth
            error={!!errors.reservation_status_date}
            helperText={errors.reservation_status_date || ''}
            InputLabelProps={{ shrink: true }}
          />
        </Grid>
        {/* Dropdown fields */}
        {[{ name: 'arrival_date_month', options: monthOptions },
          { name: 'hotel', options: hotelOptions },
          { name: 'meal', options: mealOptions },
          { name: 'market_segment', options: marketSegmentOptions },
          { name: 'distribution_channel', options: distributionChannelOptions },
          { name: 'reserved_room_type', options: reservedRoomTypeOptions },
          { name: 'deposit_type', options: depositTypeOptions },
          { name: 'customer_type', options: customerTypeOptions }]
          .map(({ name, options }) => (
            <Grid item xs={12} sm={6} key={name}>
              <TextField
                select
                label={name.replace(/_/g, ' ')}
                name={name}
                value={inputs[name]}
                onChange={handleChange}
                fullWidth
              >
                {options.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
          ))}
      </Grid>
      <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
        Predict ADR
      </Button>
      {prediction && <Typography variant="h6" sx={{ mt: 2 }}>Predicted ADR: €{prediction.toFixed(2)}</Typography>}
    </form>
  );
}
