package com.ashutosh.backend.dto.request;

import jakarta.validation.constraints.FutureOrPresent;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.time.LocalDate;

/**
 * Data Transfer Object for capturing vehicle booking requests.
 * Transports necessary reservation details from the client to the service layer
 * while enforcing basic input validation rules.
 */
@Data
public class BookingRequestDTO {

    /**
     * The unique identifier of the vehicle selected for rental.
     */
    @NotNull(message = "Vehicle ID is required")
    private Long vehicleId;

    /**
     * The scheduled start date for the rental period.
     * Must be today or a future date to prevent invalid past reservations.
     */
    @NotNull(message = "Start date is required")
    @FutureOrPresent(message = "Start date cannot be in the past")
    private LocalDate startDate;

    /**
     * The scheduled end date for the rental period.
     */
    @NotNull(message = "End date is required")
    private LocalDate endDate;
}